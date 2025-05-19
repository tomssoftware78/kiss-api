import logging
import os

from dao.gebruikers_profielen_dao import GebruikersProfielenDao

class GebruikersProfielenService:
    gebruikers_profielen_dao: GebruikersProfielenDao
    KISS_IRIS_ENVIRONMENT: str

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __init__(self):
        self.gebruikers_profielen_dao = GebruikersProfielenDao()
        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment

    def check_limited_to_team(self, badge_id):
        result = self.gebruikers_profielen_dao.get_toelatingen(badge_id=badge_id)
        
        for row in result:
            return row[0] == 3

        return True
