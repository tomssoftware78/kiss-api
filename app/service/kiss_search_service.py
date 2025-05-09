import re
import os
import logging

from service.gebruikers_profielen_service import GebruikersProfielenService
from dao.kiss.search.kiss_search_dao import KissSearchDao
from model import KissCase, KissItem
from service.kiss_tools import KissTools

class KissSearchService:
    gebruikers_profielen_service: GebruikersProfielenService
    kiss_search_dao: KissSearchDao

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __init__(self):
        self.gebruikers_profielen_service = GebruikersProfielenService()
        self.kiss_search_dao = KissSearchDao()

        iris_db_environment = os.environ.get('KISS_IRIS_ENVIRONMENT')
        self.logger.debug("Instantiating %s for IRIS DB environment: %s", self.__class__.__name__, iris_db_environment)
        self.KISS_IRIS_ENVIRONMENT = iris_db_environment

    def items(self, item_ids: list[int], badge_id: int):
        result = self.kiss_search_dao.items(item_ids=item_ids, badge_id=badge_id)

        items = []
        for row in result:
            self.logger.debug(str(row))
            items.append(KissItem.custom_init(row[0], 
                                              row[1], 
                                              row[2], 
                                              row[3], 
                                              row[4], 
                                              row[5],
                                              row[6], 
                                              False, 
                                              self.__convert_date_string(row[8]), 
                                              self.__convert_date_string(row[9]),
                                              self.__convert_date_string(row[10])
                                              )
                        )

        return items


    def get_kiss_items_from_case(self, case_id: int, badge_id: int):
        result = self.kiss_search_dao.get_kiss_items_from_case(case_id=case_id, badge_id=badge_id)

        items = []
        for row in result:
            self.logger.debug(str(row))
            items.append(KissItem.custom_init(row[0], 
                                              row[1], 
                                              row[2], 
                                              str(row[4]) + ' ' + str(row[3]), 
                                              row[11], 
                                              row[5],
                                              row[6], 
                                              False, 
                                              self.__convert_date_string(row[8]), 
                                              self.__convert_date_string(row[9]),
                                              self.__convert_date_string(row[10])
                                             )
                        )

        return items



    def search_kiss_case(self, term: str, badge_id: int):
        result = self.kiss_search_dao.search_kiss_case(term=term, badge_id=badge_id)
        
        cases = []
        ids_processed = []
        for row in result:
            self.logger.debug(str(row))

            caseId = KissTools.convertKissDetailToCaseID(row[0])
            if caseId not in ids_processed:
                name = row[1]
                if name == "DOMEIN RCCU":
                    name = KissTools.convertKissDetailToCaseName(row[0])
                cases.append(KissCase.custom_init(caseId, name, row[2], row[3], row[4], str(row[5]), row[6]))
                ids_processed.append(caseId)


        return cases   
    
    def __convert_date_string(self, d):
        if d is not None and len(d) >=10:
            return d[0:4] + '-' + d[5:7] + '-' + d[8:10]

        return d
