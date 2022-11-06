from dependency_injector import containers, providers

from email_sender import EmailSender


class Container(containers.DeclarativeContainer):
    email_sender_provider = providers.Singleton(
        EmailSender
    )