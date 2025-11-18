from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from service.entiteiten_service import EntiteitenService
from dao.entiteiten_dao import EntiteitenDao
from dao.i2_connector.dossiers_dao import DossiersDao
from routes.i2_connector.model.entiteiten_connector_models import EntiteitenDetailsData
from routes.i2_connector.model.dossiers_connector_models import DossiersDetailsData

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/entiteit/persoon/like_this")
def entiteit_by_name(request: Request, id: str = Query(...), voornaam: str = Query(...), naam: str = Query(...)):
    logger.debug('/entiteit/persoon/like_this')

    client_ip = request.client.host
    query_params = dict(request.query_params)

    logging.info(f"Request received from {client_ip} with parameters: {query_params}")

    entiteiten_service = EntiteitenService()
    logger.info('test')
    logger.info(id)
    logger.info(voornaam)
    logger.info(naam)

    result = entiteiten_service.get_persoon_entiteiten_like_this(voornaam=voornaam, naam=naam, id=id)
    return JSONResponse(content=result)


@router.get("/entiteit")
def entiteit_by_name(request: Request, vatting: str = Query(...), type: str | None = None):
    logger.debug('/entiteit')

    client_ip = request.client.host
    query_params = dict(request.query_params)

    logging.info(f"Request received from {client_ip} with parameters: {query_params}")

    entiteiten_service = EntiteitenService()
    logger.info('test')
    logger.info('Look entiteiten by vatting: %s', vatting)
    logger.info('Look entiteiten by type: %s', type)

    result = entiteiten_service.get_entiteiten_by_vatting(vatting=vatting, type=type)
    
    return JSONResponse(content=result)

@router.get("/entiteit/expand")
def expand_entiteit(request: Request, id: str = Query(...)):
    logger.debug('/entiteit/expand')

    client_ip = request.client.host
    query_params = dict(request.query_params)
    logging.info(f"Request received from {client_ip} with parameters: {query_params}")

    entiteiten_service = EntiteitenService()
    result = entiteiten_service.expand_entiteit(id=id)

    return JSONResponse(content=result)

@router.get("/entiteit/dossiers")
def get_dossiers_for_entiteit(request: Request, id: str = Query(...)):
    logger.debug('/entiteit/dossiers')

    client_ip = request.client.host
    query_params = dict(request.query_params)
    logging.info(f"Request received from {client_ip} with parameters: {query_params}")

    entiteiten_service = EntiteitenService()
    result = entiteiten_service.get_all_dossiers_for_entiteit(id)
    return JSONResponse(content=result)

@router.post("/dossiers/details")
def get_dossiers__details(dossiersDetailsData: DossiersDetailsData):
    logger.debug('/dossiers/details')

    logger.debug(dossiersDetailsData.dossier_ids)

    dossiers_dao = DossiersDao()
    result = dossiers_dao.get_dossiers_details(dossier_ids=dossiersDetailsData.dossier_ids)

    logger.debug(type(result))
    logger.debug(result)
    
    return JSONResponse(content=result)


@router.get("/dossier/entiteiten")
def expand_entiteit(request: Request, dossier_naam: str = Query(...), type: str | None = None):
    logger.debug('/dossier/entiteiten')

    client_ip = request.client.host
    query_params = dict(request.query_params)
    logging.info(f"Request received from {client_ip} with parameters: {query_params}")

    entiteiten_service = EntiteitenService()
    result = entiteiten_service.get_all_entiteiten_in_dossier(dossier_naam=dossier_naam, type=type)

    return JSONResponse(content=result)

@router.post("/dossier/entiteiten/details")
def get_dossier_entiteiten_details(entiteitenDetailsData: EntiteitenDetailsData):
    entiteiten_dao = EntiteitenDao()

    logger.debug(entiteitenDetailsData.type)
    logger.debug(entiteitenDetailsData.entiteit_ids)

    result = entiteiten_dao.get_entiteiten_data(entiteitenDetailsData.entiteit_ids, entiteitenDetailsData.type)

    logger.debug(type(result))
    logger.debug(result)
    
    return JSONResponse(content=result)