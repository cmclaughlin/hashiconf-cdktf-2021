import json as pyjson
import os
import sys
import typing
from dataclasses import dataclass
from functools import cached_property
from string import Template

import boto3
import yaml as pyyaml
from cdktf import TerraformStack

from cdktf_cdktf_provider_aws import (
    DataAwsAcmCertificate,
    DataAwsRoute53Zone,
    DataAwsSecurityGroup,
)


@dataclass
class ExampleData:
    stack: TerraformStack
    namespace: str
    region: str
    config: typing.Dict[str, str]

    def __post_init__(self):

        # Expose some data and config environment variables so they can be
        # referenced in config files.
        # Note exporting any data references here, since those are just string
        # IDs and not the ral values that would be desired
        os.environ["REGION"] = self.region
        os.environ["ACCOUNT_ID"] = self.account_id

    def aws_client(self, name):
        return boto3.client(name, region_name=self.region)

    @cached_property
    def account_id(self):
        return self.aws_client("sts").get_caller_identity().get("Account")

    @cached_property
    def domain(self):
        return self.config["domain"]

    @cached_property
    def vpc_name(self):
        return self.config["regions"][self.region]["vpc_name"]

    def security_group_full_name(self, sg_name):
        return f"{self.vpc_name}-{sg_name}"

    def resource_id(self, resource_name):
        return f"{self.namespace}-{resource_name}"

    @cached_property
    def vpc_id(self):
        return self.aws_client("ec2").describe_vpcs(
            Filters=[{"Name": "tag:Name", "Values": [self.vpc_name]}]
        )["Vpcs"][0]["VpcId"]

    def get_state_attribute(self, attr_name, default=None, raise_exception=False):
        attr_value = os.environ.get(attr_name.upper())
        if attr_value is None:
            try:
                attr_value = self.stack.remote_state_data().get(
                    attr_name.replace("_", "")
                )
            except boto3.resource("s3").meta.client.exceptions.NoSuchKey:
                pass

        if attr_value is None:
            if raise_exception:
                print(
                    f"\n\n{attr_name.upper()} must be set as an environment variable.\n",
                    file=sys.stderr,
                )
                sys.exit(1)
            return default
        return attr_value
