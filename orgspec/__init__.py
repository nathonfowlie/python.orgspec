from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from orgspec.common import Component, Environment, Organisation, load_envs
from typing import List

from orgspec.components import Component1


def init_config():
    """Initializes the orgspec configuration.

    This method must be called before consuming Organisation specifications,
    to ensure that Environments owned by the Organisation are correctly
    registered.

    If this method isn't called, the ```Organisation.environments``` will
    contain an empty list.
    """
    org_module = import_module("orgspec.organisations")

    org_list = _get_org_defs(org_module)
    for org in org_list:
        org.environments = _get_env_defs(org)
        for env in org.environments:
            _init_env(env)
            _init_components(org, env)


def _get_env_defs(org: Organisation) -> List[Environment]:
    """Auto-discover Environment specifications for each Organisation

    In order for this to function correctly, the environment specifications
    must reside within a module whose name exactly matches the Organisations
    short_name property.

    For example, environment specs for an Organisation with short name
    `myorg` should be defined in `orgspec/environments/myorg.py`.

    Params:
        org: Organisation that the environment specs belong to.

    Returns:
        A list of Environments. If none found, returns an empty list.
    """
    env_list: List[Environment] = []
    mod_name: str = f"orgspec.environments.{org.short_name}"

    if find_spec(mod_name) is not None:
        mod = import_module(mod_name)
        for obj in dir(mod):
            val = getattr(mod, obj)
            if isinstance(val, Environment):
                env_list.append(val)
    return env_list


def _get_org_defs(mod: ModuleType) -> List[Organisation]:
    """Auto-discover Organisation definitions.

    Params:
        mod: Module expected to contain the organisation definitions.

    Returns:
        A list of Organisations. If none found, returns an empty list.
    """
    org_list: List[Organisation] = []
    for obj in dir(mod):
        val = getattr(mod, obj)
        if isinstance(val, Organisation):
            org_list.append(val)
    return org_list


def _init_component(org: Organisation, env: Environment, cmp: Component) -> Component:
    """Initialize a single component residing with an Organisations environment.

    Component configuration that needs to be aware of the Organisation that
    owns the component, and the Environment that the Component resides within
    will be applied here.

    Params:
        org: Organisation that owns the component.
        env: Environment that the component resides in.
        cmp: Component to be initialized.

    Returns:
        A fully initialized component that is aware of the Organisation and
        Environment that owns it.
    """
    if isinstance(cmp, Component1):
        if cmp.foo and callable(cmp.foo):
            cmp.foo = cmp.foo(cmp, org, env)

        if cmp.db_config and callable(cmp.db_config):
            cmp.db_config = cmp.db_config(env)  # type: ignore

    return cmp


def _init_components(org: Organisation, env: Environment) -> Environment:
    """Initialize components within an Organisations environment.

    Params:
        org: Organisation that owns the component.
        env: Environment that the component resides in.

    Returns:
        A fully initialized environment containing Components that are
        Organisation and Environment aware.
    """
    for cmp in env.components:
        _init_component(org, env, cmp)
    return env


def _init_env(env: Environment) -> None:
    """Initializes a single Environment specification.

    This is primarily used to execute any lambdas within the environment
    specification, so that the consumer recieves an object that contains
    the actual environment spec, instead of references to anonymous lambda
    functions.

    Params:
        env: Environment to be initialized.
    """
    if env.db_config and callable(env.db_config):
        env.db_config = env.db_config(env)  # type: ignore
