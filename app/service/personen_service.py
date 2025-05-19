import logging
import os
from uuid import UUID

from dao.personen_dao import PersonenDao
from model import KissUser

class PersonenService:
    personen_dao: PersonenDao
    KISS_IRIS_ENVIRONMENT: str

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __init__(self):
        self.personen_dao = PersonenDao()
        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment

    def get_personen_by_name(self, name):
        result = self.personen_dao.get_personen_by_name(name=name)

        self.logger.debug(result)
        return result


    def get_team(self, badge_id):
        result = self.gebruikers_dao.get_team(badge_id=badge_id)

        for row in result:
            return row[0]

        return ""