from routes.health_routes import health_router
from routes.auth_routes import auth_router
from routes.task_routes import task_router


def include_routes(app):
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(task_router)
