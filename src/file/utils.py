import os
from fastapi import HTTPException

# def get_files_recursive(directory):
#     contents = []
#     try:
#         for item in os.listdir(directory):
#             item_path = os.path.join(directory, item)
#             if os.path.isdir(item_path):
#                 # Если это папка, добавляем тип "folder" и рекурсивно вызываем функцию
#                 contents.append({
#                     "type": "folder",
#                     "name": item,
#                     "content": get_files_recursive(item_path)
#                 })
#             else:
#                 # Если это файл, добавляем тип "file"
#                 contents.append({
#                     "type": "file",
#                     "name": item
#                 })
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return contents

def get_files_recursive(directory, current_path=""):
    contents = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        item_full_path = os.path.join(current_path, item)
        if os.path.isdir(item_path):
            contents.append({
                "type": "folder",
                "name": item,
                "fullPath": item_full_path,
                "content": get_files_recursive(item_path, item_full_path)
            })
        else:
            contents.append({
                "type": "file",
                "name": item,
                "fullPath": item_full_path
            })
    
    # Сортируем: сначала папки, затем файлы, оба типа по алфавиту
    contents = sorted(contents, key=lambda x: (x["type"] != "folder", x["name"].lower()))
    
    return contents
