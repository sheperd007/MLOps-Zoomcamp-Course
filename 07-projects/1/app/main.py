from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.home import router as home_router
from routers.model import router as prediction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup!")
    yield
    print("Application shutdown!")


app = FastAPI(title="Covid Detection Service", lifespan=lifespan)


app.include_router(home_router)
app.include_router(prediction_router)

