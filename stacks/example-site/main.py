#!/usr/bin/env python

"""
Example static site hosted on S3
"""

from constructs import Construct
from example_cdktf_env import ExampleApp, ExampleStack

from cdktf_cdktf_provider_aws import (
    AwsProvider,
    S3BucketWebsite,
    S3BucketObject
)

from cdktf import TerraformOutput

from example_s3 import ExampleS3Bucket


class MyStack(ExampleStack):

    def __init__(self, scope: Construct, ns: str):

        super().__init__(scope, ns, AwsProvider)

        bucket_name = "cdk-example-cmclaughlin"
        doc_name = "index.html"

        website = S3BucketWebsite(
            index_document=doc_name,
            error_document=doc_name
        )

        bucket = ExampleS3Bucket(
            self,
            bucket_name=bucket_name,
            block_public_access=False,
            acl="public-read",
            website=[website],
        )

        S3BucketObject(
            self,
            "upload",
            bucket=bucket_name,
            key=doc_name,
            source=f"../../../index.html",
            acl="public-read",
            content_type="text/html",
            depends_on=[bucket.bucket]
        )

        TerraformOutput(self, "endpoint", value=bucket.bucket.website_endpoint)


if __name__ == "__main__":
    app = ExampleApp()
    stack = MyStack(app, "example-site")
    app.synth()
