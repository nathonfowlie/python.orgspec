from orgspec.common import (
    Environment,
    EnvironmentType,
    env_based_db_config,
    env_based_foo_config,
)
from orgspec.components import Component1, Component2


dev: Environment = Environment(
    name="dev",
    env_type=EnvironmentType.DEV,
    components=[
        Component1(
            name="Component 1",
            db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
        ),
        Component2(name="Component 2"),
    ],
)

dev1: Environment = Environment(
    name="dev1",
    env_type=EnvironmentType.DEV,
    db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
    components=[
        Component1(
            name="Component 1",
            foo=lambda cmp, org, env: env_based_foo_config(org, env, cmp),
            db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
        ),
        Component2(name="Component 2"),
        Component2(name="Another Componnent #2"),
    ],
)
