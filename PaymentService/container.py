from dependency_injector import containers, providers

from payment_repository import PaymentRepository
from payment_event_sender import PaymentEventSender


class Container(containers.DeclarativeContainer):
    payment_event_sender_provider = providers.Singleton(
        PaymentEventSender
    )

    payment_repository_provider = providers.Singleton(
        PaymentRepository
    )
