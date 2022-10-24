from orgspec.common import env_based_db_config, Environment, EnvironmentType

dev: Environment = Environment(
    name="dev",
    env_type=EnvironmentType.DEV,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

tst: Environment = Environment(
    name="tst",
    env_type=EnvironmentType.TST,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

stg: Environment = Environment(
    name="stg",
    env_type=EnvironmentType.STG,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)

prd: Environment = Environment(
    name="prd",
    env_type=EnvironmentType.PRD,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
)
