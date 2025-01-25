

from http import HTTPMethod

from fastapi.routing import APIRoute
import app.server.routes.items as items


routes = [
    (HTTPMethod.GET,    "/items",              items.get_items,                 200),
    (HTTPMethod.GET,    "/items/{id}",         items.get_item,                  200),
    (HTTPMethod.POST,   "/items",              items.add_item,                  200)
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