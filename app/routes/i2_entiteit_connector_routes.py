from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from service.entiteiten_service import EntiteitenService

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


@router.get("/dossier/entiteiten")
def expand_entiteit(request: Request, dossier_naam: str = Query(...), type: str | None = None):
    logger.debug('/dossier/entiteiten')

    client_ip = request.client.host
    query_params = dict(request.query_params)
    logging.info(f"Request received from {client_ip} with parameters: {query_params}")

    entiteiten_service = EntiteitenService()
    result = entiteiten_service.get_all_entiteiten_in_dossier(dossier_naam=dossier_naam, type=type)

    return JSONResponse(content=result)
