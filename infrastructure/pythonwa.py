#!/usr/bin/env python3
import aws_cdk as cdk

from apigw.serverless_backend_stack import ServerlessBackendStack
from redirect.redirect import RedirectStack

AWS_ACCOUNT = "155122333172"
AWS_REGION = "ap-southeast-2"
SITE_DOMAIN_NAME = "pythonwa.com"
DOMAIN_CERTIFICATE_ARN = "arn:aws:acm:us-east-1:155122333172:certificate/3bba3daa-5daf-4c47-9ce1-248feb820921"
HOSTED_ZONE_ID = "Z03934201M8O7YD4DTYVA"
HOSTED_ZONE_NAME = "pythonwa.com"

app = cdk.App()
RedirectStack(
    app,
    "RedirectStack",
    site_domain_name=SITE_DOMAIN_NAME,
    domain_certificate_arn=DOMAIN_CERTIFICATE_ARN,
    hosted_zone_id=HOSTED_ZONE_ID,
    hosted_zone_name=HOSTED_ZONE_NAME,
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */
    env=cdk.Environment(account=AWS_ACCOUNT, region=AWS_REGION),
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

ServerlessBackendStack(
    app,
    "ServerlessBackendStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */
    env=cdk.Environment(account=AWS_ACCOUNT, region=AWS_REGION),
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()
