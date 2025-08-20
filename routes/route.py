from fastapi import APIRouter, Request, Form, HTTPException, Header,File,UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models.model import User
from schemas.schema import individual_serial
from schemas.schema import list_serial
from config.database import collection_name
from auth.auths import hash_password,verify_password,create_access_token, decode_access_token    
import os,shutil
from bson import ObjectId


router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/get")
def message():
    return {"message":"this is home page"}


# @router.get("/")
# async def get_users():
#     users = list_serial(collection_name.find())
#     return {"users" : users , "message": "here is all users"}

@router.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/create")
def create_user(
    name : str = Form(...),
    email: str  = Form(...),
    password : str = Form(..., description="enter password here"),
    address : str = Form(...),
    phone : str = Form(...),
    image: UploadFile = File(...),
    pdf: UploadFile = File(...),
    document: UploadFile = File(...)
):
    # 🔒 hash the password before saving
    hashed_pw = hash_password(password)

    user = {
        "name" : name,
        "email": email,
        "password": hashed_pw,
        "address": address,
        "phone": phone,
        "complete": False,
        "image": image.filename,
        "pdf": pdf.filename,
        "document": document.filename,
        }
        # return 1
    if image:
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        user["image"] = f"/{image_path}"

    if pdf:
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        user["pdf"] = f"/{pdf_path}"

    if document :
        document_path = os.path.join(UPLOAD_FOLDER, document.filename)
        with open(document_path, "wb") as buffer:
            shutil.copyfileobj(document.file, buffer)
        user["document"] = f"/{document_path}"
    collection_name.insert_one(user)
    return RedirectResponse("/", status_code=303) 






@router.get("/login", response_class=HTMLResponse)
def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login User (JWT token)
@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = collection_name.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 🔒 check if entered password matches hashed password
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # ✅ create token
    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}


# read all user
@router.get("/users")
def get_users(token: str = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    users = collection_name.find()
    return list_serial(users)

#  read one user
@router.get("/users/{id}")
def get_one_user(id : str):
    user = collection_name.find_one({"_id": ObjectId(id)})
    return individual_serial(user)

# update user
# @router.put("/users/{id}")
# def update_user(    {"_id" : ObjectId(id)},
#         {"$set":{
#             "name" :name,
#             "email": email,
#             "password" : password,
#             "address" : address,
#             "phone" : phone,
#             "complete": complete
#         }}
#     )
#     id : str,
#     name: str = Form(...),
#     email : str = Form(...),
#     password : str = Form(...),
#     address : str = Form(...),
#     phone: str = Form(...),
#     complete: bool = Form(...),
# ):
#     collection_name.update_one(
#     
#     updated_user=collection_name.find_one({"_id": ObjectId(id)})
#     return individual_serial(updated_user)
    

    # update user 
@router.put("/users/{id}")
async def update_user(id : str , user: User):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="invalid Id")
    
    updated = collection_name.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": user.model.dump()}
    )
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}

# delete user
@router.delete("/users/{id}")
def delete_user(id: str):
        # check if id is valid
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = collection_name.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}