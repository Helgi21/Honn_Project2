from dependency_injector import containers, providers

from product_repository import ProductRepository
from inventory_event_listener import InventoryEventListener


class Container(containers.DeclarativeContainer):
    inventory_event_listener_provider = providers.Singleton(
        InventoryEventListener
    )

    product_repository_provider = providers.Singleton(
        ProductRepository
    )
