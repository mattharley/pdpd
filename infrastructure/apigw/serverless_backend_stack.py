from aws_cdk import (
    Stack,
    CfnParameter as cfnParameter,
    aws_cognito,
    aws_s3,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway, RemovalPolicy, aws_iam,
)
from constructs import Construct
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
LAMBDA_DIR = THIS_DIR.parent.parent / 'apis'
LAMBDA_LAYERS_DIR = THIS_DIR.parent / 'lambda_layers'


class ServerlessBackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        requests_pydantic_layer = aws_lambda.LayerVersion(
            self,
            "requests_pydantic_layer",
            code=aws_lambda.Code.from_asset(str(LAMBDA_LAYERS_DIR / 'layer_requests_pydantic.zip')),
            description='Requests and Pydantic',
            compatible_runtimes=[
                aws_lambda.Runtime.PYTHON_3_9
            ],
            removal_policy=RemovalPolicy.DESTROY
        )

        pythonwa_slack_invite_lambda = aws_lambda.Function(
            self,
            id="lambdafunction",
            function_name="pythonwa_slack_invite_lambda",
            description="PythonWA Slack Invite API handler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="lambda_handler.handler",
            code=aws_lambda.Code.from_asset(str(LAMBDA_DIR / 'slack_invite')),
            environment={"key": "value", },
            layers=[requests_pydantic_layer]
        )

        lambda_allow_ssm_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["ssm:GetParameters"],
            resources=["*"]
        )
        pythonwa_slack_invite_lambda.add_to_role_policy(lambda_allow_ssm_policy)

        pythonwa_api = aws_apigateway.LambdaRestApi(
            self, id="lambdaapi", rest_api_name="pythonwa_api", handler=pythonwa_slack_invite_lambda, proxy=True
        )
        post_data = pythonwa_api.root.add_resource("form")
        post_data.add_method(
            "POST"
        )  # POST images/files & metadata
