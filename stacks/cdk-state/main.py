#!/usr/bin/env python

"""
Manages state for CDKTF stacks.

Creates a S3 bucket for state files and DynamoDB table for locking.

There's a chicken/egg problem of sorts here... we need to create
the resources before using them for state management. Therefore,
this stack uses local state. After the initial creation, it can
be switched to inherit from ExampleStack and the previously/locally
created resources can be imported if desired. See the example-site
stack for an example of inheritance.
"""

from cdktf_cdktf_provider_aws import (
    AwsProvider,
    DynamodbTable,
    DynamodbTableAttribute,
    S3Bucket,
    S3BucketPublicAccessBlock,
    S3BucketVersioning,
)
from constructs import Construct

from cdktf import App

from example_cdktf_env.example_stack import STATE_NAME

from cdktf import TerraformStack


class MyStack(TerraformStack):
    """
    cdktf-state
    """

    def __init__(self, scope: Construct, ns: str):

        super().__init__(scope, ns)
        AwsProvider(self, "Aws", region="us-east-1")

        self.name = STATE_NAME

        self.s3()
        self.dynamodb()

    def s3(self):

        bucket = S3Bucket(
            self,
            id=self.name,
            bucket=self.name,
            acl="private",
            versioning=[S3BucketVersioning(enabled=True)],
        )

        S3BucketPublicAccessBlock(
            self,
            id=f"{self.name}-public-access-block",
            bucket=self.name,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True,
            depends_on=[bucket],
        )

    def dynamodb(self):

        attribute = [DynamodbTableAttribute(name="LockID", type="S")]
        DynamodbTable(
            self,
            id=f"{self.name}-table",
            name=self.name,
            attribute=attribute,
            hash_key="LockID",
            billing_mode="PAY_PER_REQUEST",
        )


if __name__ == "__main__":
    app = App()
    stack = MyStack(app, "cdk-state")
    app.synth()
