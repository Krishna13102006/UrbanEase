import os
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
BUCKET_NAME = 'urbanease-images'

def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image(file_bytes, filename, folder=''):
    """Upload image to Supabase Storage. Returns public URL."""
    client = get_client()
    path = f"{folder}/{filename}" if folder else filename
    # Need to verify if the file exists already? The upsert logic handles it.
    client.storage.from_(BUCKET_NAME).upload(
        path, file_bytes, {"content-type": "image/jpeg", "upsert": "true"}
    )
    public_url = client.storage.from_(BUCKET_NAME).get_public_url(path)
    return public_url

def delete_image(path):
    """Delete image from Supabase Storage."""
    client = get_client()
    client.storage.from_(BUCKET_NAME).remove([path])
