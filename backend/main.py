from fastapi import FastAPI
from .database import Base, engine
from .routers import customers, tasks, analytics
from . import auth
from  bizpilot.database import Base,engine
from backend.bizpilot.routes import authi,customer,task

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BizPilot Lite API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(tasks.router)
app.include_router(analytics.router)
Base.metadata.create_all(bind=engine)
app.include_router(authi.router)
app.include_router(customer.router)
app.include_router(task.router)