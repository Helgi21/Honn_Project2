from dependency_injector import containers, providers

from merchant_repository import MerchantRepository
from merchant_event_sender import MerchantEventSender


class Container(containers.DeclarativeContainer):
    merchant_event_sender_provider = providers.Singleton(
        MerchantEventSender
    )

    message_repository_provider = providers.Singleton(
        MerchantRepository
    )
