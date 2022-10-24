from orgspec.common import Component, ComponentType, DBConfig
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


@dataclass
class Component1(Component):
    """Spec for a Component1 component residing within an environment."""

    """Database schema used to connect to the application backend."""
    db_config: Optional[Callable[[Any], DBConfig]] = None

    def __init__(
        self,
        name: str,
        component_type: ComponentType = ComponentType.COMPONENT1,
        db_config: Optional[Callable[[Any], DBConfig]] = None,
        **kwargs: Any
    ) -> None:
        """Initialize a new Component1.

        The component_type property will be automatically set here to simplify
        consumption of the component.

        Params:
            self: Class reference
            name: Component name
            component_type: The type of component that this is.
            db_config: Database configuration.
            **kwargs: Additional arguments to passed through to the superclass.
        """
        super().__init__(name=name, component_type=component_type, **kwargs)
        self.db_config = db_config


@dataclass
class Component2(Component):
    """Spec for a Component2 component residing within an environment."""

    def __init__(
        self,
        name: str,
        component_type: ComponentType = ComponentType.COMPONENT2,
        **kwargs: Any
    ) -> None:
        """Initialize a new Component2.

        The component_type property will be automatically set here to simplify
        consumption of the component.

        Params:
            self: Class reference
            name: Component name
            component_type: The type of component that this is.
            **kwargs: Additional arguments to passed through to the superclass.
        """
        super().__init__(name=name, component_type=component_type, **kwargs)
