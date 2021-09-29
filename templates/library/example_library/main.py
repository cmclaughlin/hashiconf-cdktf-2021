import typing
from dataclasses import dataclass

from cdktf import TerraformOutput, TerraformStack
from cdktf_cdktf_provider_aws import IamPolicy, IamRole


@dataclass
class MyModule:
    stack: TerraformStack
