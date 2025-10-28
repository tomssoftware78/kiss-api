from kissutils import database_instance
#from .persoon_like_this_query_builder import PersoonLikeThisQueryBuilder 
from dao.util import kiss_db_table_mapping
import logging

class DossiersDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_dossier_id_by_name(self, dossier_naam):
        sql = "select d.ID from kiss.tblDOSSIERS d where upper(Naam) = '" + dossier_naam + "'"

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows(sql)
        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples
        return result[0][0] if result and len(result) > 0 and len(result[0]) > 0 else None

