from bson import ObjectId

def individual_serial(user) -> dict:
    return {
        "id" : str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        # "password": user["password"],
        "address" : user["address"],
        "phone": user["phone"],
        "complete" : user["complete"],
        "image" : user.get(),
        "pdf": user.get("pdf"),
        "document": user.get("document")
    }

def list_serial(users) -> list:
    return[individual_serial(user) for user in users]