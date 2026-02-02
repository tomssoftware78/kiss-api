from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_reftab_dao_export.reftab_dao import ReftabDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/reftab/rpna")
def get_entiteiten(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: str = Query(..., description="Laatste IdEntiteit uit vorige batch, of 0 voor de eerste batch"),
):
    reftab_dao = ReftabDao()

    result = reftab_dao.get_rpna_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)
