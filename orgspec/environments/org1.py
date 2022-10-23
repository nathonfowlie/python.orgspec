from orgspec.common import Environment, EnvironmentType, env_based_db_config
from typing import List

"""Primary dev environment."""
dev: Environment = Environment(
    name="dev",
    env_type=EnvironmentType.DEV,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

"""Secondary dev environment."""
dev1: Environment = Environment(
    name="dev1",
    env_type=EnvironmentType.DEV,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)


def envspec() -> List[Environment]:
    """List all environments available in this module.

    Returns:
        A list containing zero or more Environment specifications.
    """
    return [dev, dev1]
