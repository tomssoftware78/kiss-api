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
    
    def get_dossier_by_name(self, dossier_naam):
        sql = "select * from kiss.tblDOSSIERS d where upper(Naam) = '" + dossier_naam + "'"

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows_with_column_names(sql)
        return result

