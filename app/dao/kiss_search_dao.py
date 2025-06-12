from kissutils import database_instance
from dao.search_query_builder import SearchQueryBuilder

import logging
import os



class KissSearchDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __init__(self):
        self.search_query_builder = SearchQueryBuilder()

        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment
    
    def items(self, item_ids: list[int], badge_id: int):
        sql = self.search_query_builder.build_for_items(item_ids=item_ids, badge_id=badge_id)

        result = database_instance.fetch_rows(sql)
        return result
    
    def search_kiss_case(self, term: str, badge_id: int):
        sql = self.search_query_builder.build_for_search_kiss_case(term=term, badge_id=badge_id)
    
        result = database_instance.fetch_rows(sql)
        return result
    
    def get_kiss_items_from_case(self, case_id: int, badge_id: int):
        sql = self.search_query_builder.build_for_get_kiss_items_from_case(case_id=case_id, badge_id=badge_id)

        result = database_instance.fetch_rows(sql)
        return result
