from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class VragenRegisterDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_vragen_register_entiteiten_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "vre.Id, vre.IdVraag, vre.IdEntiteit "
        from_clause = "from kiss.tblVragenRegEntiteiten vre "
        where_clause = "where vre.Id > " + str(last_id) + " "
        order_clause = "order by vre.Id";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result