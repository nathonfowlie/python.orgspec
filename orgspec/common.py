from types import ModuleType
from typing import List, Optional
from dataclasses import dataclass
import importlib
from enum import Enum, unique


@unique
class EnvironmentType(Enum):
    """Environment categories."""

    DEV = ("DEV",)
    TST = ("TST",)
    STG = ("STG",)
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
    db_config: Optional[DBConfig] = None


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
            namespace=None,
            path=f"atl/{env.name}",
            keys=["ATL_DB_PASSWORD"]
        ),
    )


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
    environments: List[Environment]

    def env(self, name: str) -> Environment:
        """Retrieve an environment specification.

        Params:
            name: Name of the environment to retrieve.

        Returns:
            A Environment instnace, or `None` if an environment with the given
            name could not be found.
        """
        e = next((x for x in self.environments if x.name == name), None)
        return e


def load_envs(name: str) -> List[Environment]:
    """Plugin loader to dynamically load environment specifications.

    Params:
        name: Name of the module that contains the environment specs. Module
              must sit under the 'orgspec.environments' namespace.

    Returns:
        A list of one or more Environment instances.
    """
    mod: ModuleType = importlib.import_module(f"orgspec.environments.{name}")
    func = getattr(mod, "envspec")
    all = func()

    found_envs = []

    for e in all:
        if e.db_config:
            e.db_config = e.db_config(e)
        found_envs.append(e)

    return found_envs
