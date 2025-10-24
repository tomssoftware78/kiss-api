import logging
import os

from dao.entiteiten_dao import EntiteitenDao
from dao.relaties_dao import RelatiesDao

class EntiteitenService:
    entiteiten_dao: EntiteitenDao
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