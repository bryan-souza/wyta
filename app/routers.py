import hashlib
from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi import status

from app.controllers import ItemController, StorageController, ReportController
from app.exceptions import ItemNotFoundError
from app.models import Item

files_router = APIRouter(prefix='/files')


@files_router.post('/', status_code=status.HTTP_200_OK)
async def upload_file(
        files: List[UploadFile],
        item_controller: ItemController = Depends(),
        storage_controller: StorageController = Depends(),
        report_controller: ReportController = Depends()
):
    digests = []

    for file in files:
        _content = await file.read()
        _digest = hashlib.md5(_content).hexdigest()
        _filename = file.filename

        try:
            _item = item_controller.get_by_digest(_digest)
        except ItemNotFoundError:
            storage_controller.write(_content, filename=_digest)
            _item = item_controller.insert(Item(digest=_digest, filename=_filename))
        finally:
            digests.append(_item.digest)
            continue

    return report_controller.create_report(digests)
