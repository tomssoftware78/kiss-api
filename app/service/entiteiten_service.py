import logging
import os
import json

from uuid import UUID

from dao.util.kiss_db_table_mapping import entiteit_table_mapping
from dao.entiteiten_dao import EntiteitenDao
from dao.personen_dao import PersonenDao
from dao.relaties_dao import RelatiesDao
from model import KissUser

class EntiteitenService:
    entiteiten_dao: EntiteitenDao
    personen_dao: PersonenDao
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
        self.personen_dao = PersonenDao()
        self.relaties_dao = RelatiesDao()
        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment

    def get_entiteiten_by_vatting(self, vatting, type):
        result = self.entiteiten_dao.get_entiteiten_by_vatting(vatting=vatting, type=type)

        self.logger.debug(result)
        return result

    def expand_entiteit(self, id=id):
        relaties = self.relaties_dao.get_relaties_with_entiteiten(entiteitId=id)
        print(type(relaties))

        for r in relaties:
            van_entiteit = self.entiteiten_dao.get_entiteit_generic_data(entiteitId=r['IdRelatieVan'])    
            naar_entiteit = self.entiteiten_dao.get_entiteit_generic_data(entiteitId=r['IdRelatieNaar'])
            r['entiteit_van'] = van_entiteit
            r['entiteit_naar'] = naar_entiteit

        return relaties
    
    def expand_persoon(self, id):
        relaties = self.relaties_dao.get_relaties_with_entiteiten(entiteitId=id)
        self.logger.debug('Relaties: %s', relaties)
        result = []
        naar_entiteiten = []
        if relaties:
            for r in relaties:
                self.logger.debug('Row: %s', json.dumps(r, indent=2))
                r['Type']
                naar_entiteit = self.entiteiten_dao.get_entiteit_data(entiteitId=r['IdEntiteit'], entiteit_type=r['Type'])
                naar_entiteiten.append(naar_entiteit)

                result_entry = {
                    'relatie': r,
                    'naar_entiteit': naar_entiteit,
                    'entiteit_type': entiteit_table_mapping[r['Type']]['naam']
                }
                result.append(result_entry)

        self.logger.debug('Naar entiteiten: %s', relaties)

        return result

    def get_team(self, badge_id):
        result = self.gebruikers_dao.get_team(badge_id=badge_id)

        for row in result:
            return row[0]

        return ""