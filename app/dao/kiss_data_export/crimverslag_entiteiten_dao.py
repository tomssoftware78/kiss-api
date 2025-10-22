from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class CrimverslagEntiteitenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
        
    def get_distinct_crimverslag_ids(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "cve.crimVerslag "
        from_clause = "from kiss.tblCrimVerslagEntiteiten cve "
        where_clause = "where cve.crimVerslag > " + str(last_id) + " "
        order_clause = "order by cve.crimVerslag";

        sql = select_clause + from_clause + where_clause + order_clause
        self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows(sql)
        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        return result

    def get_crimverslag_entiteiten(self, crimverslag_ids: list):
        ids_str = ", ".join(str(i) for i in crimverslag_ids)

        select_clause = "select cve.crimVerslag, cve.idEntiteit "
        from_clause = "from kiss.tblCrimVerslagEntiteiten cve "
        where_clause = "where cve.crimVerslag in (" + ids_str + ") "
        order_clause = "order by cve.crimVerslag, cve.idEntiteit";

        sql = select_clause + from_clause + where_clause + order_clause
        self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
