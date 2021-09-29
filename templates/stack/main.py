#!/usr/bin/env python

"""
Example stack
"""

from cdktf_cdktf_provider_aws import AwsProvider
from constructs import Construct
from example_cdktf_env import ExampleApp, ExampleStack


class MyStack(ExampleStack):
    """
    Example stack
    """

    def __init__(self, scope: Construct, ns: str):

        super().__init__(scope, ns, AwsProvider)

        # Define resources here


if __name__ == "__main__":
    app = ExampleApp()
    stack = MyStack(app, "example-stack")
    app.synth()
