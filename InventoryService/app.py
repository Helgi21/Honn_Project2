import uvicorn
from fastapi import FastAPI
import multiprocessing
from dependency_injector.wiring import inject, Provide

from container import Container
import endpoints
from inventry_event_listener import InventoryEventListener


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app

@inject
def start_listener(inventory_event_listener: InventoryEventListener = 
                    Provide[Container.inventory_event_listener_provider]):
    inventory_event_listener.start()

app = create_app()

if __name__ == '__main__':
    multiprocessing.process(uvicorn.run('application:app', host='0.0.0.0', port=8004, reload=True))
    multiprocessing.process(start_listener())
