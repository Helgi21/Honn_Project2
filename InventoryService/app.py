import uvicorn
import contextlib
import time
import threading
from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide
from threading import Thread

from container import Container
import endpoints
from inventory_event_listener import InventoryEventListener
current_module = __import__(__name__)

def create_app(container) -> FastAPI:
    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app

@inject
def start_listener(inventory_event_listener: InventoryEventListener = 
                    Provide[Container.inventory_event_listener_provider]):
    inventory_event_listener.start()

# How the uvicorn github reccomends running it in a thread..
class Server(uvicorn.Server):
    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[current_module, endpoints])

    config = uvicorn.Config(create_app(container), host="0.0.0.0", port=8004)
    server = Server(config=config)
    with server.run_in_thread():
        start_listener()
        while True:
            pass
