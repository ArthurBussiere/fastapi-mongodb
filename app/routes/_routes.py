from http import HTTPMethod

from fastapi import Depends
from fastapi.routing import APIRoute
from components.authentication.auth_manager import get_current_active_user

from routes import items
from routes import users
from routes import auth

routes = [

#------- METHOD ------------- PATH ------------------------- ENDPOINT ----------------- CODE -- AUTH ------ TAG ----- #

    #LOGIN
    (HTTPMethod.POST,       "/token",                   auth.get_access_token,          200,    False,    ["Auth" ]),

    # ITEMS
    (HTTPMethod.GET,        "/items",                   items.get_items,                200,    True,     ["Items"]),
    (HTTPMethod.GET,        "/items/{id}",              items.get_item,                 200,    True,     ["Items"]),
    (HTTPMethod.POST,       "/items",                   items.add_item,                 200,    True,     ["Items"]),
    (HTTPMethod.DELETE,     "/items/{id}",              items.delete_item,              200,    True,     ["Items"]),

    # USERS
    (HTTPMethod.GET,        "/users",                   users.get_users,                200,    True,     ["Users"]),
    (HTTPMethod.GET,        "/users/{id}",              users.get_user,                 200,    True,     ["Users"]),
    (HTTPMethod.POST,       "/users",                   users.add_user,                 200,    True,     ["Users"]),
    (HTTPMethod.DELETE,     "/users/{id}",              users.delete_user,              200,    True,     ["Users"]),

]


def create_apiroute(path: str, endpoint: any, method: str, status_code: int, auth: bool, tags: list) -> APIRoute:
    """Helper function to create an APIRoute."""
    dependencies = [Depends(get_current_active_user)] if auth else None
    return APIRoute(
        path=path,
        endpoint=endpoint,
        methods=[method],
        status_code=status_code,
        dependencies=dependencies,
        tags=tags
    )


def collect_routes(route_list: list[tuple[str, str, any, int, bool]]) -> list[APIRoute]:
    """Constructs a list of APIRoutes based on the provided route definitions."""
    return [
        create_apiroute(path, endpoint, method, status_code, auth, tags)
        for method, path, endpoint, status_code, auth, tags in route_list
    ]


fastapi_routes = collect_routes(routes)