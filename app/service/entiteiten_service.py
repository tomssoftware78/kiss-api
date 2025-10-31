import logging
import os

from dao.entiteiten_dao import EntiteitenDao
from dao.i2_connector.dossiers_dao import DossiersDao
from dao.i2_connector.documenten_dao import DocumentenDao
from dao.i2_connector.gebeurtenissen_dao import GebeurtenissenDao
from dao.i2_connector.relaties_dao import RelatiesDao


class EntiteitenService:
    entiteiten_dao: EntiteitenDao
    dossiers_dao: DossiersDao
    documenten_dao: DocumentenDao
    gebeurtenissen_dao: GebeurtenissenDao
    relaties_dao: RelatiesDao
    KISS_IRIS_ENVIRONMENT: str

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __init__(self):
        self.entiteiten_dao = EntiteitenDao()
        self.dossiers_dao = DossiersDao()
        self.documenten_dao = DocumentenDao()
        self.gebeurtenissen_dao = GebeurtenissenDao()
        self.relaties_dao = RelatiesDao()
        
        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment

    def get_persoon_entiteiten_like_this(self, voornaam, naam, id):
        result = self.entiteiten_dao.get_persoon_entiteiten_like_this(voornaam=voornaam, naam=naam, id=id)

        self.logger.debug(result)
        return result

    def get_entiteiten_by_vatting(self, vatting, type):
        result = self.entiteiten_dao.get_entiteiten_by_vatting(vatting=vatting, type=type)

        self.logger.debug(result)
        return result
    
    def get_all_entiteiten_in_dossier(self, dossier_naam, type):
        dossier = self.dossiers_dao.get_dossier_by_name(dossier_naam=dossier_naam)
        
        ## TODO what if dossier_id = None
        document_ids = self.documenten_dao.get_document_ids_by_dossier_id(dossier_id=dossier[0]['ID'])
        gebeurtenis_ids = self.gebeurtenissen_dao.get_gebeurtenis_ids_for_document_ids(document_ids=document_ids)

        #relaties = self.relaties_dao.get_relaties_with_entiteiten_for_gebeurtenissen(gebeurtenis_ids=gebeurtenis_ids)
        relaties = self.relaties_dao.test(gebeurtenis_ids=gebeurtenis_ids)
        for r in relaties:
            #van_entiteit = self.entiteiten_dao.get_entiteit_generic_data(entiteitId=r['IdRelatieVan'])    
            #naar_entiteit = self.entiteiten_dao.get_entiteit_generic_data(entiteitId=r['IdRelatieNaar'])
            #r['entiteit_van'] = van_entiteit
            #r['entiteit_naar'] = naar_entiteit
            r['entiteit_van'] = {}
            r['entiteit_naar'] = {}
            
        dossier[0]['relaties'] = relaties
        return dossier[0]    


    def expand_entiteit(self, id=id):
        relaties = self.relaties_dao.get_relaties_with_entiteiten(entiteitId=id)

        for r in relaties:
            van_entiteit = self.entiteiten_dao.get_entiteit_generic_data(entiteitId=r['IdRelatieVan'])    
            naar_entiteit = self.entiteiten_dao.get_entiteit_generic_data(entiteitId=r['IdRelatieNaar'])
            r['entiteit_van'] = van_entiteit
            r['entiteit_naar'] = naar_entiteit

        return relaties    

    def get_team(self, badge_id):
        result = self.gebruikers_dao.get_team(badge_id=badge_id)

        for row in result:
            return row[0]

        return ""