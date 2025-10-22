from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_sci_data_export.relaties_dao import SciRelatiesDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/sci/relaties")
def get_relaties(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    relaties_dao = SciRelatiesDao()

    result = relaties_dao.get_relaties_paged(page_size=page_size, last_id=last_id)
    logger.debug(type(result))
    logger.debug(result)
    
    return JSONResponse(content=result)
