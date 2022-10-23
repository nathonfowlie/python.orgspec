from orgspec.common import Organisation, load_envs

org1 = Organisation(
    name="Org 1",
    short_name="org1",
    environments=load_envs("org1"),
)

org2 = Organisation(
    name="Org 2",
    short_name="org2",
    environments=load_envs("org2"),
)
