# curd-with-JWT
This project is a **CRUD system** built using **FastAPI**, **MongoDB**, and **JWT authentication** with hashed passwords.  
It demonstrates secure user management, token-based authentication, and MongoDB integration.


##  Features
- User registration with **hashed passwords**
- **JWT authentication** for secure access
- CRUD operations (Create, Read, Update, Delete)
- MongoDB database connection using **pymongo**
- Organized folder structure with **routes**, **templates** folder for html files and also with**uploads**  folder to save pdf, image and document file.
- `.env` support for secret keys and configuration
- File upload support (images & PDFs)

##  first create virtual env
- python -m venv venv
- activate virtual-env .\venv\scripts\activate

## connect with mongodb
- pip install pymonog 
- python -m pip install "pymongo[srv]==3.11"
- copy the uri and paste in monogo client in database file  


##  also add requirements.txt file 
-pip freeze > requirements.txt

##  Project Structure

├── main.py # Entry point of the application
├── routes/ # API route handlers
├── templates/ # HTML templates (if any)
├── uploads/ # upload files (documents, pdf, Images)
├── schemas/ # serialization and all list of serials
├── auth / # hashed and verify password 
├── config / # connect with mongodb
├── models  / # pydantic model 
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── .gitignore # Git ignore rules
└── README.md # Documentation

## .env file code
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

## add .gitignore file 
first go cmd  and write git clone and write ssh code  copied from github and copy all files in new folder then make a .gitignore file and write comment and push the code.
## in gitignore file 
- venv/
- __pycache__/
- .env

## run the application
uvicorn main:app --reload
we can also change the port using
uvicorn main:app --host 127.0.0.1 --port 8000