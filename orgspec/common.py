"""Common classes, enums and helper functions used by the orgspec framework."""
from types import ModuleType
from typing import Any, Callable, List, Optional
from dataclasses import dataclass, field
import importlib
from enum import Enum, unique


@unique
class ComponentType(Enum):
    """Types of components available to an Environment."""

    COMPONENT1 = "COMPONENT1"
    COMPONENT2 = "COMPONENT2"
    COMPONENT3 = "COMPONENT3"


@dataclass
class Component:
    name: str
    component_type: Optional[ComponentType] = None
    foo: Optional[str] = None


@unique
class EnvironmentType(Enum):
    """Environment categories."""

    DEV = "DEV"
    TST = "TST"
    STG = "STG"
    PRD = "PRD"


@dataclass
class VaultSecret:
    """Helper class used to access a secret in vaults KV backend."""

    """Path to the vault secret."""
    path: str

    """One or more keys used to access the secret.
    
    The keys will be appended to the vault path.
    """
    keys: List[str]

    """Vault namespace."""
    namespace: Optional[str] = None


@dataclass
class DBConfig:
    """Database configuration for a specific component."""

    """Username used to access the database."""
    db_user: str

    """Defines how to retrieve the database password from Vault."""
    db_password: VaultSecret


@dataclass
class Environment:
    """Specification for a single environment, owned by a single Org."""

    """Environment name.
    
    The name must be lowercase as a matter of convention, as the name is used
    to determine how to retrieve sensitive information from Vault.
    """
    name: str

    """Environment type

    Used to identify whether this environment spec is for a non-prod, or
    production environment.
    """
    env_type: EnvironmentType

    """Database schema used to connect to the application backend."""
    db_config: Optional[Callable[[Any], DBConfig]] = None

    """Components running in the environment."""
    components: List[Component] = field(default_factory=list)


@dataclass
class Organisation:
    """Organisation specification."""

    """Organisations friendly name."""
    name: str

    """Abbreviated org name.
    
    Case sensitive. This is embedded into various application configurations.
    """
    short_name: str

    """List of environments hosted by the organisation."""
    environments: List[Environment] = field(default_factory=list)

    def env(self, name: str) -> Optional[Environment]:
        """Retrieve an environment specification.

        Params:
            name: Name of the environment to retrieve.

        Returns:
            A Environment instnace, or `None` if an environment with the given
            name could not be found.
        """
        e = next((x for x in self.environments if x.name == name), None)
        return e


def env_based_db_config(env: Environment, db_user: str) -> DBConfig:
    """Generate a database schema adjusted for the target environment.

    Currently the namespace attribute is ignored. In future vault secrets will
    be namespace aware.

    Params:
        env: Environment specification.
        db_user: Username used to access the database.

    Returns:
        A DBConfig database schema.
    """
    return DBConfig(
        db_user=db_user,
        db_password=VaultSecret(
            namespace=None, path=f"atl/{env.name}", keys=["ATL_DB_PASSWORD"]
        ),
    )


def env_based_foo_config(org: Organisation, env: Environment, cmp: Component) -> str:
    """"""
    return f"{org.name}/{env.name}"


def load_envs(name: str) -> List[Environment]:
    """Plugin loader to dynamically load environment specifications.

    Params:
        name: Name of the module that contains the environment specs. Module
              must sit under the 'orgspec.environments' namespace.

    Returns:
        A list of one or more Environment instances.
    """
    mod_name: str = f"orgspec.environments.{name}"
    mod: ModuleType = importlib.import_module(mod_name)
    envspec_func = getattr(mod, "envspec")

    found_envs = []
    for env in envspec_func():
        if env.db_config:
            env.db_config = env.db_config(env)
        found_envs.append(env)

    return found_envs
