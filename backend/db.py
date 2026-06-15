import os
import hashlib
from supabase import create_client

def get_supabase_client():
    supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_key:
        raise ValueError("SUPABASE_KEY not found in .env file.")
    return create_client(supabase_url, supabase_key)

def get_user_by_username(username):
    supabase = get_supabase_client()
    response = supabase.table("app_users").select("id, avatar").eq("username", username.strip()).limit(1).execute()
    if response.data:
        return response.data[0]
    return None

def authenticate_user(username, password):
    supabase = get_supabase_client()
    hashed_pw = hashlib.sha256(password.strip().encode('utf-8')).hexdigest()
    response = supabase.table("app_users").select("id, password, avatar").eq("username", username.strip()).limit(1).execute()
    if response.data and response.data[0].get("password") == hashed_pw:
        return response.data[0]
    return None

def check_user_exists(username):
    supabase = get_supabase_client()
    response = supabase.table("app_users").select("id").eq("username", username.strip()).execute()
    return len(response.data) > 0

def create_user(username, password, avatar_emoji):
    supabase = get_supabase_client()
    hashed_pw = hashlib.sha256(password.strip().encode('utf-8')).hexdigest()
    new_user = {"username": username.strip(), "password": hashed_pw, "avatar": avatar_emoji}
    return supabase.table("app_users").insert(new_user).execute()

def fetch_user_history(user_id):
    supabase = get_supabase_client()
    response = supabase.table("user_predictions").select("*").eq("user_id", user_id).order("id").execute()
    return response.data

def insert_history_record(record):
    supabase = get_supabase_client()
    return supabase.table("user_predictions").insert(record).execute()

def clear_user_history(user_id):
    supabase = get_supabase_client()
    return supabase.table("user_predictions").delete().eq("user_id", user_id).execute()

def get_all_predictions():
    supabase = get_supabase_client()
    return supabase.table("user_predictions").select("id, timestamp, disease, confidence, image_url, user_id, app_users(username)").execute()

def delete_prediction(row_id):
    supabase = get_supabase_client()
    return supabase.table("user_predictions").delete().eq("id", row_id).execute()

def delete_all_predictions():
    supabase = get_supabase_client()
    return supabase.table("user_predictions").delete().neq("id", -1).execute()

def upload_image(file_name, file_bytes, content_type):
    supabase = get_supabase_client()
    supabase.storage.from_("Leafimage").upload(
        path=file_name,
        file=file_bytes,
        file_options={"content-type": content_type}
    )
    return supabase.storage.from_("Leafimage").get_public_url(file_name)