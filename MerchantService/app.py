import uvicorn
from fastapi import FastAPI
from container import Container
import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001, reload=True)