from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from dao.kiss_data_export.crimverslag_entiteiten_dao import CrimverslagEntiteitenDao
from routes.kiss_data_export.model.crimverslag_export_models import CrimverslagIdList
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/crimverslag/ids")
def get_crimverslag_ids(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste ID uit vorige batch, of 0 voor de eerste batch"),
):
    crimverslag_entiteiten_dao = CrimverslagEntiteitenDao()

    result = crimverslag_entiteiten_dao.get_distinct_crimverslag_ids(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)


@router.post("/export/crimverslag/entiteiten")
def get_crimverslag_entiteiten(crimverslagIds: CrimverslagIdList):
    crimverslag_entiteiten_dao = CrimverslagEntiteitenDao()

    print(crimverslagIds.ids)

    result = crimverslag_entiteiten_dao.get_crimverslag_entiteiten(crimverslag_ids=crimverslagIds.ids)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)
