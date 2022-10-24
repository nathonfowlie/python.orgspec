# OrgSpec

Proof of concept framework for defining environment configuration as code, with
support for multi-tenancy, and component specific configurations.

The framework makes extensive use of reflection to automagically discover 
organisations, and environment specifications based on a strict naming
convention.

## How It Works

1. The framework inspects the contents of `orgspec.organisations` for any
   `Organisation` class instances.
2. For each discovered class instance, the framework will look under the
   `orgspec.environments` namespace for a module that exactly matches the
   organisations short name.
3. If a matching module is found, the module is loaded.
4. The framework inspects the contents of the loaded module for any
   `Environment` class instances.
5. For each discovered class instance, the framework iterates over any
   components defined for that environment, and executes lambda functions
   embedded within the component. The lambda functions accept both the
   Organisation and the Environment as arguments, to allow the component to
   adjust it's configuration based on the environment that it's running within.
6. The same lambda execution process is repeated on the Environment class
   instance(s).
7. An additional Vault helper (not yet implemented) can then be used to
   retrieve any secrets required to provision/configuration an Organisation,
   Environment or Component.

## Usage

```python
"""Main entrypoint for the demo orgspec utility."""
from orgspec import init_config
from orgspec.organisations import org1, org2

# Initialize the framework. Auto-discovers the Organisation definitions,
# environments associated with each definition, then loads the 
# environments + components for each Organisation.
init_config()

# Dump a full organisation specification
print(org1)

# Get the specification for the "DEV" environment in Org2.
dev = org2.env('dev')
print(dev.db_config.db_username)

# Get the specification for a component running in the DEV environment in Org1
cmp = x for x in org1.env('dev').components if x.component_type == ComponentType.COMPONENT1

# <- this component has it's own database configuration either separate to,
# or complimentary to the environments default database config.
print(cmp.db_config.db_username)

# Not yet implemented. Relies on a strict naming convention to determine the
# location of the secret within Vault, which is based on the short name of
# the Organisation, the Environment name, and one or more additional keys.
db_password = get_secret(cmp.db_config.db_password)
```

### Defining Organisations

Simple add a new Organisation class instance to the `orgspec.organisations` module.

```python
# orgspec/organisations.py
myorg: Organisation = Organisation(
    name="My Organisation"
    short_name="myorg"
)
```

### Defining Environments

Create a module under `orgspec.environments` with a name that exactly matches
the Organisations short name.

**note:**
Additional logic needs to be addded to `orgspec.init_config` if any changes are
made to the lambdas defined here, so that the framework knows how to generate
the Org/Environment/Component aware configuration.

```python
# orgspec/environments/myorg.py
dev: Environment = Environment(
    name = 'dev1',
    environment_type = EnvironmentType.DEV,
    components=[
        Component1(
            name="Component 1",
            db_config=lambda env: env_based_db_config(env, "ATL_ENTERPRISE_OWNER"),
        ),
        Component2(name="Component 2"),
    ],
)
```

### Defining Components

Add components to `orgspec.components`, then they can used within the
Environment specifications.

As for Environments, if you add any additional lambdas here, you will need to
make the relevant changes to `orgspec.init_config` so the framework can take
the Organisation and Environment into account when loading the component
specification.

```python
# orgspec/components.py
@dataclass
class MyComponent(Component):
    db_config: Optional[Callable[[Any], DBConfig]] = None

    def __init__(
        self,
        name: str,
        component_type: ComponentType = ComponentType.COMPONENT1,
        db_config: Optional[Callable[[Any], DBConfig]] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(name=name, component_type=component_type, **kwargs)
        self.db_config = db_config
```