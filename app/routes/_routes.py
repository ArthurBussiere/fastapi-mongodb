from http import HTTPMethod

from fastapi import Depends
from fastapi.routing import APIRoute
from app.components.authentication.auth_manager import get_current_active_user

from app.routes import items
from app.routes import users
from app.routes import auth

routes = [

#-- METHOD ---------------- PATH ---------------------- ENDPOINT ---------------------- CODE --- AUTH ----------- #

    #LOGIN
    (HTTPMethod.POST,       "/token",                   auth.get_access_token,          200,     False),

    # ITEMS
    (HTTPMethod.GET,        "/items",                   items.get_items,                200,     True),
    (HTTPMethod.GET,        "/items/{id}",              items.get_item,                 200,     True),
    (HTTPMethod.POST,       "/items",                   items.add_item,                 200,     True),
    (HTTPMethod.DELETE,     "/items/{id}",              items.delete_item,              200,     True),

    # USERS
    (HTTPMethod.GET,        "/users",                   users.get_users,                200,     True),
    (HTTPMethod.GET,        "/users/{id}",              users.get_user,                 200,     True),
    (HTTPMethod.POST,       "/users",                   users.add_user,                 200,     True),
    (HTTPMethod.DELETE,     "/users/{id}",              users.delete_user,              200,     True),
]


def create_apiroute(path: str, endpoint: any, method: str, status_code: int, auth: bool) -> APIRoute:
    """Helper function to create an APIRoute."""
    dependencies = [Depends(get_current_active_user)] if auth else None
    return APIRoute(
        path=path,
        endpoint=endpoint,
        methods=[method],
        status_code=status_code,
        dependencies=dependencies
    )


def collect_routes(route_list: list[tuple[str, str, any, int, bool]]) -> list[APIRoute]:
    """Constructs a list of APIRoutes based on the provided route definitions."""
    return [
        create_apiroute(path, endpoint, method, status_code, auth)
        for method, path, endpoint, status_code, auth in route_list
    ]


fastapi_routes = collect_routes(routes)