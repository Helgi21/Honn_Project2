from dependency_injector import containers, providers

from order_repository import OrderRepository
from order_event_sender import OrderEventSender


class Container(containers.DeclarativeContainer):
    order_event_sender_provider = providers.Singleton(
        OrderEventSender
    )

    order_repository_provider = providers.Singleton(
        OrderRepository
    )
