from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_sci_data_export.entiteiten_dao import SciEntiteitenDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/sci/entiteiten")
def get_entiteiten(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste IdEntiteit uit vorige batch, of 0 voor de eerste batch"),
):
    entiteiten_dao = SciEntiteitenDao()

    result = entiteiten_dao.get_entiteiten_paged(page_size=page_size, last_id=last_id)
    
    return JSONResponse(content=result)

@router.get("/export/sci/entiteit/personen")
def get_personen(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste IdEntiteit uit vorige batch, of 0 voor de eerste batch"),
):
    entiteiten_dao = SciEntiteitenDao()

    result = entiteiten_dao.get_personen_paged(page_size=page_size, last_id=last_id)
    
    return JSONResponse(content=result)