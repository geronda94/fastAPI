from pydantic import BaseModel



class CreateFolderRequest(BaseModel):
    path: str  # Путь, где нужно создать папку
    folder_name: str  # Название новой папки