from routers.ping import router as ping_router
from routers.user import router as user_router
from routers.auth import router as auth_router
from routers.tasks import router as tasks_router
from routers.categories import router as categories_router

routers = [ping_router, user_router, auth_router, tasks_router, categories_router]