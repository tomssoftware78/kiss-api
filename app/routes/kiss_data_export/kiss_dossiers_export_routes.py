from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_data_export.dossiers_dao import DossiersDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/dossiers")
def get_dossiers(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    dossiers_dao = DossiersDao()

    result = dossiers_dao.get_dossiers_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)

@router.get("/export/documenten")
def get_documenten(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    dossiers_dao = DossiersDao()

    result = dossiers_dao.get_documenten_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)

@router.get("/export/gebeurtenissen")
def get_gebeurtenissen(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    dossiers_dao = DossiersDao()

    result = dossiers_dao.get_gebeurtenissen_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)

@router.get("/export/relaties")
def get_relaties(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    dossiers_dao = DossiersDao()

    result = dossiers_dao.get_relaties_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)
