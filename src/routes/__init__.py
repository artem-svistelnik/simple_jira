from routes.health_router import health_router

def include_routes(app):
    app.include_router(health_router)

