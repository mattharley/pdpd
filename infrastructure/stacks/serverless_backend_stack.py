import os
from pathlib import Path

from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_apigateway,
    aws_certificatemanager,
    aws_iam,
    aws_lambda,
    aws_route53,
    aws_route53_targets,
)
from constructs import Construct

PYTHON_WA_API_KEY = os.environ["PYTHON_WA_API_KEY"]

THIS_DIR = Path(__file__).resolve().parent
LAMBDA_DIR = THIS_DIR.parent.parent / "apis"
LAMBDA_LAYERS_DIR = THIS_DIR.parent / "lambda_layers"

CORS_ORIGINS = [
    "http://pythonwa.com",
    "https://pythonwa.com",
    "http://www.pythonwa.com",
    "https://www.pythonwa.com",
    "http://localhost:3000",
]


class ServerlessBackendStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_certificate_arn: str = None,
        hosted_zone_name: str = None,
        hosted_zone_id: str = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ###
        # API GATEWAY AND DOMAIN
        ###

        certificate = aws_certificatemanager.Certificate.from_certificate_arn(
            self,
            "site_certificate",
            certificate_arn=domain_certificate_arn,
        )

        domain_name_options = aws_apigateway.DomainNameOptions(
            domain_name="api.pythonwa.com",
            certificate=certificate,
            security_policy=aws_apigateway.SecurityPolicy.TLS_1_2,
            endpoint_type=aws_apigateway.EndpointType.EDGE,
        )

        api = aws_apigateway.RestApi(
            self,
            id="pythonwa_api",
            rest_api_name="pythonwa_api",
            domain_name=domain_name_options,
            deploy_options=aws_apigateway.StageOptions(
                throttling_rate_limit=10,
                throttling_burst_limit=10,
            ),
            default_cors_preflight_options=aws_apigateway.CorsOptions(
                allow_methods=aws_apigateway.Cors.ALL_METHODS,
                allow_origins=CORS_ORIGINS,
            ),
        )

        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            "hosted_zone",
            zone_name=hosted_zone_name,
            hosted_zone_id=hosted_zone_id,
        )

        aws_route53.ARecord(
            self,
            "ApiRecord",
            record_name="api",
            zone=hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGateway(api)),
        )

        ###
        # LAMBDA LAYERS
        ###

        requests_pydantic_layer = aws_lambda.LayerVersion(
            self,
            "requests_pydantic_layer",
            code=aws_lambda.Code.from_asset(str(LAMBDA_LAYERS_DIR / "requests_pydantic.zip")),
            description="Requests and Pydantic",
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            removal_policy=RemovalPolicy.DESTROY,
        )

        markdown_layer = aws_lambda.LayerVersion(
            self,
            "markdown_layer",
            code=aws_lambda.Code.from_asset(str(LAMBDA_LAYERS_DIR / "markdown.zip")),
            description="Markdown layer",
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            removal_policy=RemovalPolicy.DESTROY,
        )

        ###
        # LAMBDA HANDLERS
        ###

        lambda_allow_ssm_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["ssm:GetParameters", "ssm:GetParameter"],
            resources=["*"],
        )

        ###
        # SLACK INVITE
        ###

        pythonwa_slack_invite_lambda = aws_lambda.Function(
            self,
            id="lambdafunction",
            function_name="pythonwa_slack_invite_lambda",
            description="PythonWA Slack Invite API handler",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            code=aws_lambda.Code.from_asset(str(LAMBDA_DIR / "slack_invite")),
            environment={
                "key": "value",
            },
            layers=[
                requests_pydantic_layer,
            ],
        )

        pythonwa_slack_invite_lambda.add_to_role_policy(lambda_allow_ssm_policy)

        slack_invite_integration = aws_apigateway.LambdaIntegration(
            pythonwa_slack_invite_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        slack_resource = api.root.add_resource("slack")
        slack_method: aws_apigateway.Method = slack_resource.add_method(
            "POST",
            slack_invite_integration,
            api_key_required=True,
        )

        ###
        # EVENTS LIST
        ###

        events_list_lambda = aws_lambda.Function(
            self,
            id="event_list_lambdafunction",
            function_name="pythonwa_events_list_lambda",
            description="PythonWA Events List API handler",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            code=aws_lambda.Code.from_asset(str(LAMBDA_DIR / "events_list")),
            environment={
                "key": "value",
            },
            layers=[
                requests_pydantic_layer,
                markdown_layer,
            ],
        )

        events_list_integration = aws_apigateway.LambdaIntegration(
            events_list_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        events_list_resource = api.root.add_resource("events_list")
        events_list_method: aws_apigateway.Method = events_list_resource.add_method(
            "GET",
            events_list_integration,
            api_key_required=True,
        )

        ###
        # THROTTLE
        ###

        plan = api.add_usage_plan(
            "PythonWAUsagePlan",
            name="PythonWAUsagePlan",
            throttle=aws_apigateway.ThrottleSettings(
                rate_limit=5,
                burst_limit=5,
            ),
            description="PythonWA Usage Plan",
        )
        plan.add_api_stage(
            stage=api.deployment_stage,
            throttle=[
                aws_apigateway.ThrottlingPerMethod(
                    method=slack_method,
                    throttle=aws_apigateway.ThrottleSettings(
                        rate_limit=1,
                        burst_limit=1,
                    ),
                ),
                aws_apigateway.ThrottlingPerMethod(
                    method=events_list_method,
                    throttle=aws_apigateway.ThrottleSettings(
                        rate_limit=60,
                        burst_limit=60,
                    ),
                ),
            ],
        )
        api_key = aws_apigateway.ApiKey(self, "PythonWAPublic", value=PYTHON_WA_API_KEY)
        plan.add_api_key(api_key=api_key)
        # plan.add_api_stage(stage=api.deployment_stage, throttle=[slack_throttle, ])
