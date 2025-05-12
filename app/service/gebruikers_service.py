import logging
import os
from uuid import UUID

from dao.gebruikers_dao import GebruikersDao
from model import KissUser

class GebruikersService:
    gebruikers_dao: GebruikersDao
    KISS_IRIS_ENVIRONMENT: str

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __init__(self):
        self.gebruikers_dao = GebruikersDao()
        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment

    def get_user(self, badge_id):
        result = self.gebruikers_dao.get_user(badge_id=badge_id)

        for row in result:
            self.logger.debug(str(row))
            unit = row[5]
            superuser = (unit == 'RCCU')
            uuid = str(UUID('00000000000000000000000' + str(badge_id)))
            return KissUser.custom_init(uuid, str(row[0]), row[2], row[1], row[3], unit, row[4], superuser, superuser,
                                    superuser, "NL", None, None)

        return None


    def get_team(self, badge_id):
        result = self.gebruikers_dao.get_team(badge_id=badge_id)

        for row in result:
            return row[0]

        return ""