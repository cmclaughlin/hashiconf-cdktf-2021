"""
Example inheritable stack.
"""

import boto3
import json
import re

from cdktf import S3Backend, TerraformStack
from constructs import Construct

from example_cdktf_env.example_environment import Env
from example_cdktf_env.example_data import ExampleData

from botocore.exceptions import ClientError


# The name of your S3 bucket for state files and DynamoDB table for locking
STATE_NAME = "hashiconf2021-cdktf-cmclaughlin"


class ExampleStack(TerraformStack):
    """
    A base CDKTF stack class with common variables and env setup.
    """

    def __init__(self, scope: Construct, ns: str, AwsProvider):

        self.ns = ns
        self.check_stack_name()

        # Environment setup for common variables used by most stacks
        self.env = Env()
        self.region = self.env.region
        self.config = self.env.config

        # The namespace is used throughout the synthesized output and it's
        # hashed to genenerate a UUID. We append the env name and region
        # to ensure it's really unique accross all our deployments.
        self.ns_uniq = f"{ns}-{self.env.name}-{self.region}"

        # Init the parrent class
        super().__init__(scope, self.ns_uniq)

        # Data lookups
        self.data = ExampleData(
            stack=self,
            namespace=self.ns_uniq,
            region=self.region,
            config=self.env.config,
        )

        # Read config with env vars set
        self.config = self.env.config

        # Common app name
        self.app_name = f"{self.data.vpc_name}-{self.ns}"

        # Another namespace option including the account ID
        self.ns_uniq_acct = f"{self.ns_uniq}-{self.data.account_id}"

        # Configure state
        self.state_name = STATE_NAME
        state = {
            "bucket": self.state_name,
            "key": self.ns_uniq,
            "region": self.region,
            "encrypt": True,
            "dynamodb_table": self.state_name,
        }
        S3Backend(self, **state)

        # Setup AWS provider
        AwsProvider(self, "Aws", region=self.region)

    def remote_state_data(self, stack=None, env_name=None):
        """
        Workaround for https://github.com/hashicorp/terraform-cdk/issues/247

        cdktf adds a hash to output keys, which makes reading them from another
        state difficult. So here we read the remote state from S3 ourselves and
        strip out the hashes from the dictionary keys.

        Unfortunately cdktf also strips underscores from the output names, e.g.
        my_output becomes myoutput.

        Based on https://stackoverflow.com/questions/40995251
        """

        if stack is None:
            stack = self.ns

        if env_name is None:
            env_name = self.env.name

        key = f"{stack}-{env_name}-{self.region}"
        try:
            content_object = boto3.resource("s3").Object(self.state_name, key)
            content = content_object.get()["Body"].read().decode("utf-8")
            outputs = json.loads(content)["outputs"]
        except ClientError as e:
            print(f"Remote state issue {e}")
            return {}

        ret = {}

        for key, output in outputs.items():
            normalized_key = key.split("_")[1]
            ret[normalized_key] = output["value"]

        return ret

    def restrict_env(self, envs=()):
        """
        Provides the option to restrict a stack to certain environments.
        i.e. you might need a DNS entry in prod, but not in dev/qa.
        """

        if self.env.name not in envs:
            raise Exception(f"This stack can only run in {envs}")

    def check_stack_name(self):
        """
        Ensure ns only contains letters, numbers and dashes.
        """

        if not re.match("^[A-Za-z0-9-]*$", self.ns):
            raise Exception("Stack names should only have letters, numbers and dashes")
