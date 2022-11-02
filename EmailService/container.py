from dependency_injector import containers, providers

from email_repository import EmailRepository
from email_event_sender import EmailEventSender


class Container(containers.DeclarativeContainer):
    email_event_sender_provider = providers.Singleton(
        EmailEventSender
    )

    email_repository_provider = providers.Singleton(
        EmailRepository
    )
