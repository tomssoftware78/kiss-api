from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_data_export.vragen_register_dao import VragenRegisterDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/vragenregister/entiteiten")
def get_dossiers(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    vragenregister_dao = VragenRegisterDao()

    result = vragenregister_dao.get_vragen_register_entiteiten_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)
