from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class EntiteitenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_entiteit_data(self, entiteitId, entiteit_type):
        tabel_naam = kiss_db_table_mapping.entiteit_table_mapping[entiteit_type]['tabel']

        select_clause = "select tb.*, e.EntiteitVatting "
        from_clause = "from " + tabel_naam + " tb inner join kiss.tblENTITEITEN e on tb.IdEntiteit = e.ID"
        where_clause = " where tb.IdEntiteit = " + str(entiteitId)
        
        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows_with_column_names(sql)
        #result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
        #                                        # returned from the database was a list of tuples
        return result[0]