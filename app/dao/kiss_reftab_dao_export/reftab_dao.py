from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class ReftabDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_rpna_paged(self, page_size: int, last_id: str):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "p.PnaKey, p.PnaTextBD, p.PnaTextBF, p.PnaTextBG, p.PnaTextBE, p.PnaAlpha3, p.PnaAlpha6, p.PnaCreation, "
        select_clause += "p.PnaLastUpdate, p.PnaDeactivateDate, p.PNAActivationDate "
        from_clause = "from reftab.rPNA p "
        where_clause = "where p.PnaKey > " + last_id + " "
        order_clause = "order by p.PnaKey";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
