

from http import HTTPMethod

from fastapi.routing import APIRoute
from app.routes import items
from app.routes import users


routes = [
    # ITEMS
    (HTTPMethod.GET,        "/items",                   items.get_items,                200),
    (HTTPMethod.GET,        "/items/{id}",              items.get_item,                 200),
    (HTTPMethod.POST,       "/items",                   items.add_item,                 200),
    (HTTPMethod.DELETE,     "/items/{id}",              items.delete_item,              200),

    # USERS
    (HTTPMethod.GET,        "/users",                   users.get_users,                200),
    (HTTPMethod.GET,        "/users/{id}",              users.get_user,                 200),
    (HTTPMethod.POST,       "/users",                   users.add_user,                 200),
    (HTTPMethod.DELETE,     "/users/{id}",              users.delete_user,              200),
]


def collect_routes(
    routes: list[tuple[HTTPMethod, str, any, int]]
) -> list[APIRoute]:

    constructed_routes: list[APIRoute] = []
    for http_method, path, endpoint, status_code, in routes:
        constructed_routes.append(
            APIRoute(
                path,
                endpoint,
                methods=[http_method.value],
                status_code=status_code
            )
        )
    return constructed_routes

fastapi_routes = collect_routes(routes)