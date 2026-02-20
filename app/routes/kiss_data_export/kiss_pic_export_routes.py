from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_data_export.pic_data_dao import PicDataDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/pic/dossiertypes")
def get_dossiers(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    pic_data_dao = PicDataDao()

    result = pic_data_dao.get_dossier_types_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)

@router.get("/export/pic/teltechnrs")
def get_picTelTechNrs(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste IdEntiteit uit vorige batch, of 0 voor de eerste batch")
):
    pic_data_dao = PicDataDao()

    result = pic_data_dao.get_tel_tech_nrs(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)
