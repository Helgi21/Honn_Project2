from dependency_injector import containers, providers

from buyer_repository import BuyerRepository


class Container(containers.DeclarativeContainer):
    buyer_repository_provider = providers.Singleton(
        BuyerRepository
    )
