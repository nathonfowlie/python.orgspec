from orgspec.common import Environment, EnvironmentType, env_based_db_config
from typing import List

"""Dev environment."""
dev: Environment = Environment(
    name="dev",
    env_type=EnvironmentType.DEV,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

"""Test environment."""
tst: Environment = Environment(
    name="tst",
    env_type=EnvironmentType.TST,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

"""Staging environment."""
stg: Environment = Environment(
    name="stg",
    env_type=EnvironmentType.STG,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

"""Prod environment."""
prd: Environment = Environment(
    name="prd",
    env_type=EnvironmentType.PRD,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

def envspec() -> List[Environment]:
    """List all environments available in this module.

    Returns:
        A list containing zero or more Environment specifications.
    """
    return [dev, tst, stg, prd]
