import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://rootuser:rootpass@localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.items

item_collection = database.get_collection("items_collection")


#helpers
def item_helper(item) -> dict :
    return {
        "id": str(item["_id"]),
        "name": str(item["name"]),
        "description": str(item["description"])
    }

async def retrieve_items():
    items = []
    async for item in item_collection.find():
        items.append(item_helper(item))
    return items


async def retrieve_item(id: str) -> dict:
    if item := await item_collection.find_one({"_id": ObjectId(id)}):
        return item_helper(item)


async def add_item_data(item_data: dict) -> dict:
    item = await item_collection.insert_one(item_data)
    new_item = await item_collection.find_one({"_id": item.inserted_id})
    return item_helper(new_item)

