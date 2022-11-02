from dependency_injector import containers, providers

from product_repository import EmailRepository
from inventory_event_listener import EmailEventSender


class Container(containers.DeclarativeContainer):
    inventory_event_listener_provider = providers.Singleton(
        InventoryEventListener
    )

    product_repository_provider = providers.Singleton(
        ProductRepository
    )
