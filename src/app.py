# import os
import logging
from fastapi import FastAPI, BackgroundTasks
from auth.router import router as auth_router
from db.database import engine, Base
# from worker.celery_app import celery_app


def get_application() -> FastAPI:
    """
    This function is responsible to create a table metadata, our engine and
    the main application router that inherits other apps routers
    """
    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    # TODO : middleware missing
    # TODO : CORS missing
    # TODO : Headers missing

    app.include_router(auth_router)

    return app
    

app = get_application()

@app.get("/")
async def read_root():
    return {"Hello": "World"}



# log = logging.getLogger(__name__)

# def celery_on_message(body):
#     log.warn(body)

# def background_on_message(task):
#     log.warn(task.get(on_message=celery_on_message, propagate=False))

# @app.get("/{word}")
# async def root(word: str, background_task: BackgroundTasks):
    
#     task_name = "src.worker.celery_worker.test_celery"

#     task = celery_app.send_task(task_name, args=[word])
#     print(task)
#     background_task.add_task(background_on_message, task)

#     return {"message": "Word received"}
