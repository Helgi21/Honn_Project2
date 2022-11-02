from dependency_injector import containers, providers

from merchant_repository import MerchantRepository

class Container(containers.DeclarativeContainer):
    message_repository_provider = providers.Singleton(
        MerchantRepository
    )
