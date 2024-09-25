import os
import shutil
from fastapi import File, UploadFile, HTTPException


ALLOWED_FILE_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

async def validate_file(file):
    # Check file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Check file size
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

    file.file.seek(0)  # Reset file pointer after reading
    return file


async def save_file(file,id=None,image=None):
     # Get the directory of the current file (auth.py)
    current_dir = os.path.dirname(__file__)

    # Move up two levels to the 'auth' directory
    auth_dir = os.path.dirname(current_dir)

    if image!=None:
        static_dir = os.path.join(auth_dir, 'static')
        static_dir = os.path.join(static_dir, 'images')
    else:   
        static_dir = os.path.join(auth_dir, 'static')

    # Ensure the logs directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    if id == None:
        id=''
    # Save the file
    if image!=None:
        file_path = os.path.join(auth_dir, r'static\images', id + file.filename)
    else:
        file_path = os.path.join(auth_dir, 'static', id + file.filename)
    # file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    filename = os.path.basename(file_path)
    return file_path