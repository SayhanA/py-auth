from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import secrets
from flask_mail import Mail, Message

mongo = PyMongo()
mail = Mail()

def set_mongo(app):
    mongo.init_app(app)
    mail.init_app(app)

def create_user(name, email, password):
    verification_token = secrets.token_urlsafe(32)
    user = {
        "name": name,
        "email": email,
        "password": password,  # In production, you should hash the password
        "isVerified": False,
        "verificationToken": verification_token
    }
    mongo.db.users.insert_one(user)
    return verification_token

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def verify_user(email, password):
    user = find_user_by_email(email)
    if user and user["password"] == password:  # In production, use password hashing
        return user
    return None

def verify_user_by_token(token):
    user = mongo.db.users.find_one({"verificationToken": token})
    if user:
        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"isVerified": True, "verificationToken": None}}
        )
        return True
    return False

def generate_new_verification_token(email):
    """Generate a new verification token for the user"""
    verification_token = secrets.token_urlsafe(32)
    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"verificationToken": verification_token}}
    )
    return verification_token

def is_user_verified(email):
    """Check if user is already verified"""
    user = find_user_by_email(email)
    return user.get("isVerified", False) if user else False