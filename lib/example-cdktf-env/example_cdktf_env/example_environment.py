"""
Reusable config for stacks.
"""

import os

from deepmerge import always_merger
from envyaml import EnvYAML

DEFAULT_REGION = "us-east-1"


class Env:
    """
    Reusable config for stacks.
    """

    def __init__(self):
        """
        Reads and returns Yaml config.
        """

        if "ENV" not in os.environ:
            raise Exception("ENV must be set as an env var.")

        self.name = os.environ["ENV"]
        self.project = os.environ.get("PROJECT")
        self.region = os.environ.get("REGION", DEFAULT_REGION)
        self.suffix = self.name if self.name != "prod" else ""

    @property
    def config(self):
        """
        Reads and merges Yaml config files.

        The first level is the global config.yaml relative to this file.
        The second level is the stack specific config.yaml.
        """

        dirname = os.path.dirname(__file__)
        config = EnvYAML(os.path.join(dirname, "config.yaml"))
        global_config = config.get(self.name, {})

        default_global_config = config.get("default", {})

        # Merge default global config with global env-specific
        global_config = always_merger.merge(default_global_config, global_config)

        local_config_file = os.path.join(os.getcwd(), "config.yaml")
        local_config = {}
        if os.path.isfile(local_config_file):
            # Local config with all envs
            local_config_all = EnvYAML(local_config_file)
            # Local config with only this env
            config_key = f"{self.name}_{self.project}" if self.project else self.name
            local_config = local_config_all.get(config_key, {})
            # Default config for all envs
            default_config = local_config_all.get("default", {})
            # Merge default config with env-specific
            local_config = always_merger.merge(default_config, local_config)

        # Merge local config with global config
        return always_merger.merge(global_config, local_config)
