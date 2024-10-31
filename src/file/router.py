
import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from .utils import get_files_recursive
from auth.base_config import current_user
from auth.roles import role, permission, Perms
from auth.models import User, Roles
from .schemas import CreateFolderRequest




router = APIRouter(
    prefix='/file',
    tags=['Media']
)

STATIC_DIR = "static"  # Путь к папке со статическими файлами


@router.get('/all-files')
@role([Roles.admin.value, Roles.moderator.value])
async def get_files(user: User = Depends(current_user)):
    try:
        files_structure = get_files_recursive(STATIC_DIR)
        return {"files": files_structure}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Static directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/file/{filename}")
async def get_file(filename: str, request: Request):
    file_path = f"static/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")







@router.post('/create-folder')
@role([Roles.admin.value, Roles.moderator.value])
async def create_folder(data: CreateFolderRequest, user: User = Depends(current_user)):
    # Удаляем начальный слэш, если он есть
    safe_path = data.path.lstrip('/') if data.path.startswith('/') else data.path
    folder_path = os.path.join(STATIC_DIR, safe_path, data.folder_name)
    print(folder_path)
    try:
        os.makedirs(folder_path, exist_ok=True)
        return {"status": "Folder created successfully"}
    except PermissionError:
        raise HTTPException(status_code=500, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))