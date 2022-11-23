import hashlib
from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi import status

from app.controllers import ItemController, StorageController
from app.exceptions import ItemNotFoundError
from app.models import Item

files_router = APIRouter(prefix='/files')


@files_router.post('/', status_code=status.HTTP_201_CREATED)
async def upload_file(
        files: List[UploadFile],
        item_controller: ItemController = Depends(),
        storage_controller: StorageController = Depends()
):
    conflicts = []
    output = []

    for file in files:
        _content = await file.read()
        _digest = hashlib.md5(_content).hexdigest()
        _filename = file.filename

        try:
            item_controller.get_by_digest(_digest)
            # If it gets past this, it means the file already exists
            # if so, append it to the conflicts list
            conflicts.append(_filename)
        except ItemNotFoundError:
            storage_controller.write(_content, filename=_digest)
            _item = item_controller.insert(Item(digest=_digest, filename=_filename))
            output.append(_item)
            continue

    if len(conflicts) == len(files):
        # Only raise error if all uploaded files conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    # In case everything goes right, return a list of uploaded items
    return output
