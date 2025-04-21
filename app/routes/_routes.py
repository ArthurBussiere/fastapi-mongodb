from http import HTTPMethod
from typing import List

from models.response import Response
from models.items import Item
from models.users import User
from models.auth import NewToken, Token
from fastapi import Depends
from fastapi.routing import APIRoute
from components.authentication.auth_manager import get_current_active_user

from routes import items
from routes import users
from routes import auth

# fmt: off
routes = [
	# --- METHOD ------------- PATH ----------------- ENDPOINT --------------- CODE - AUTH ---- RESPONSE -------- TAG ----- #
	# LOGIN
	(HTTPMethod.POST,	 	'/login', 			auth.get_access_token, 			200, False, 	NewToken, 		['Auth']),
	(HTTPMethod.POST, 		'/login/refresh', 	auth.refresh_token, 			200, False, 	Token, 			['Auth']),
	# ITEMS
	(HTTPMethod.GET, 		'/items', 			items.get_items, 				200, True, 		List[Item], 	['Items']),
	(HTTPMethod.GET, 		'/items/{id}', 		items.get_item, 				200, True, 		Item, 			['Items']),
	(HTTPMethod.POST, 		'/items', 			items.add_item, 				200, True, 		Item, 			['Items']),
	(HTTPMethod.DELETE, 	'/items/{id}', 		items.delete_item, 				200, True, 		Item, 			['Items']),
	# USERS
	(HTTPMethod.GET, 		'/users', 			users.get_users, 				200, True, 		List[User],		['Users']),
	(HTTPMethod.GET, 		'/users/{id}', 		users.get_user, 				200, True, 		User, 			['Users']),
	(HTTPMethod.POST, 		'/users', 			users.add_user, 				200, False, 		User, 			['Users']),
	(HTTPMethod.PUT, 		'/users/{id}', 		users.update_user, 				200, True, 		User, 			['Users']),
	(HTTPMethod.DELETE, 	'/users/{id}', 		users.delete_user, 				200, True, 		User, 			['Users']),
]
# fmt: on


def create_apiroute(
	path: str, endpoint: any, method: str, status_code: int, auth: bool, response_model: any, tags: list
) -> APIRoute:
	"""Helper function to create an APIRoute."""
	dependencies = [Depends(get_current_active_user)] if auth else None
	return APIRoute(
		path=path,
		endpoint=endpoint,
		methods=[method],
		status_code=status_code,
		dependencies=dependencies,
		response_model=Response[response_model],
		tags=tags,
	)


def collect_routes(route_list: list[tuple[str, str, any, int, bool]]) -> list[APIRoute]:
	"""Constructs a list of APIRoutes based on the provided route definitions."""
	return [
		create_apiroute(
			path,
			endpoint,
			method,
			status_code,
			auth,
			response_model,
			tags,
		)
		for method, path, endpoint, status_code, auth, response_model, tags in route_list
	]


fastapi_routes = collect_routes(routes)
