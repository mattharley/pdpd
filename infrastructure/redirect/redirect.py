from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from common.static_site import StaticSitePublicS3, RedirectSitePublicS3


class RedirectStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            site_domain_name: str,
            domain_certificate_arn: str,
            hosted_zone_id: str,
            hosted_zone_name: str,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "TempQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        site = RedirectSitePublicS3(
            self,
            f"{site_domain_name}-construct",
            site_domain_name=site_domain_name,
            domain_certificate_arn=domain_certificate_arn,
            origin_referer_header_parameter_name="/prod/static-site/origin-custom-header/referer",
            hosted_zone_id=hosted_zone_id,
            hosted_zone_name=hosted_zone_name,
        )
