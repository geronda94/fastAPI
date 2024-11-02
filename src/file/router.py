
import os
import shutil
from urllib.parse import unquote
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from .utils import get_files_recursive
from auth.base_config import current_user
from auth.roles import role, permission, Perms
from auth.models import User, Roles
from .schemas import CreateFolderRequest
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from pydantic import BaseModel
import aiofiles
from typing import Optional



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
  
    try:
        os.makedirs(folder_path, exist_ok=True)
        return {"status": "Folder created successfully"}
    except PermissionError:
        raise HTTPException(status_code=500, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    

@router.delete("/delete-file")
@role([Roles.admin.value, Roles.moderator.value])
async def delete_file(file_path: str, user: User = Depends(current_user)):
    file_path = unquote(file_path)
    
    safe_path = os.path.join(STATIC_DIR, file_path.lstrip('/'))

    # Проверка, существует ли путь
    if not os.path.exists(safe_path):
        raise HTTPException(status_code=404, detail="File or directory not found")
    
    try:
        # Проверяем, является ли это директорией
        if os.path.isdir(safe_path):
            # Удаляем директорию и все её содержимое
            for root, dirs, files in os.walk(safe_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(safe_path)  # Удаляем саму директорию
        else:
            # Удаляем файл
            os.remove(safe_path)

        return {"status": "File or directory deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
    
    





class MoveRequest(BaseModel):
    source_path: str
    destination_path: str

@router.post("/move")
@role([Roles.admin.value, Roles.moderator.value])
async def move_file_or_folder(request: MoveRequest, user: User = Depends(current_user)):
    # Корректируем путь для безопасности
    source = os.path.join(STATIC_DIR, request.source_path.lstrip('/'))
    destination_dir = os.path.join(STATIC_DIR, request.destination_path.lstrip('/'))
    
    if not os.path.exists(source):
        raise HTTPException(status_code=404, detail="Source path not found")
    
    # Убедимся, что целевая директория существует
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Получаем имя файла из исходного пути
    original_filename = os.path.basename(source)
    destination = os.path.join(destination_dir, original_filename)

    # Функция для генерации уникального имени файла
    def get_unique_destination(dest_path):
        base, extension = os.path.splitext(dest_path)
        counter = 2
        new_dest = dest_path
        # Проверяем, пока не найдем уникальный путь
        while os.path.exists(new_dest):
            new_dest = f"{base} ({counter}){extension}"
            counter += 1
        return new_dest

    # Если файл с таким именем уже существует, находим уникальное имя
    unique_destination = get_unique_destination(destination)

    try:
        # Перемещаем файл или директорию
        shutil.move(source, unique_destination)
        return {"status": "Move successful", "source": source, "destination": unique_destination}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error moving file or folder: {str(e)}")


@router.post('/upload-file')
@role([Roles.admin.value, Roles.moderator.value])
async def upload_file(
    path: str = Form(""),
    file: UploadFile = File(...),
    user: User = Depends(current_user)
):
    # Проверка пути, если пустой или корневой, используем STATIC_DIR
    safe_path = path.lstrip('/') if path.startswith('/') else path
    initial_file_path = os.path.join(STATIC_DIR, safe_path, file.filename)

    # Функция для получения уникального имени файла
    def get_unique_file_path(file_path):
        base, extension = os.path.splitext(file_path)
        counter = 2
        new_file_path = file_path
        while os.path.exists(new_file_path):
            new_file_path = f"{base} ({counter}){extension}"
            counter += 1
        return new_file_path

    # Получаем уникальное имя файла, если такое уже существует
    file_path = get_unique_file_path(initial_file_path)

    try:
        # Асинхронная запись файла
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
        return {"status": "File uploaded successfully", "path": file_path}
    except PermissionError:
        raise HTTPException(status_code=500, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))