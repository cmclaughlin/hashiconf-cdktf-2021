import json

import typing

from dataclasses import dataclass, field

from cdktf import TerraformStack


from cdktf_cdktf_provider_aws import (
    S3Bucket,
    S3BucketGrant,
    S3BucketLogging,
    S3BucketLifecycleRule,
    S3BucketPolicy,
    S3BucketPublicAccessBlock,
    S3BucketWebsite,
)


@dataclass
class ExampleS3Bucket:
    stack: TerraformStack
    bucket_name: str
    block_public_access: bool = True

    # Optional
    acl: typing.Optional[str] = None
    bucket_policy: typing.Optional[dict] = None
    lifecycle_rule: typing.Optional[typing.List[S3BucketLifecycleRule]] = None
    tags: typing.Dict[str, str] = field(default_factory=dict)
    logging: typing.Optional[S3BucketLogging] = None
    grant: typing.Optional[S3BucketGrant] = None
    website: typing.Optional[typing.List[S3BucketWebsite]] = None

    def create_s3_bucket(self):
        return S3Bucket(
            scope=self.stack,
            id=f"s3-{self.bucket_name}",
            acl=self.acl,
            bucket=self.bucket_name,
            lifecycle_rule=self.lifecycle_rule,
            tags=self.tags,
            logging=self.logging,
            grant=self.grant,
            website=self.website,
        )

    def block_bucket_public_access(self, bucket):
        S3BucketPublicAccessBlock(
            self.stack,
            id=f"s3-bpab-{self.bucket_name}",
            bucket=self.bucket_name,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True,
            depends_on=[bucket],
        )

    def update_bucket_policy(self, bucket):
        return S3BucketPolicy(
            self.stack,
            id=f"{self.bucket_name}-bucket-policy",
            bucket=self.bucket_name,
            policy=json.dumps(self.bucket_policy),
            depends_on=[bucket],
        )

    def __post_init__(self):
        msg = "Must provide ACL or Grant, but not both"
        acl_and_grant = [self.acl, self.grant]
        if all(acl_and_grant) or not any(acl_and_grant):
            raise Exception(msg)

        self.bucket = self.create_s3_bucket()

        if self.block_public_access:
            self.block_bucket_public_access(self.bucket)

        if self.bucket_policy:
            self.update_bucket_policy(self.bucket)
