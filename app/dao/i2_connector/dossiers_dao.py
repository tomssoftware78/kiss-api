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
    
    def get_dossiers_details(self, dossier_ids):
        ids = ",".join(str(n) for n in dossier_ids)

        sql = f"""
            SELECT * FROM kiss.tblDOSSIERS d where d.ID in ({ids})
        """

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    
    def get_dossiers_for_entiteit(self, entiteit_id):
        sql = f"""
            SELECT d.iddossier
                FROM kiss.tblRELATIES r
                    JOIN kiss.tblGEBEURTENISSEN g ON g.id = r.IdGebeurtenis
                    JOIN kiss.tblDOCUMENTEN d ON d.id = g.iddocument
                    JOIN kiss.tblENTITEITEN e ON e.id = r.IdRelatieVan
                WHERE r.IdRelatieVan = {entiteit_id}
            UNION
            SELECT d.iddossier
                FROM kiss.tblRELATIES r
                    JOIN kiss.tblGEBEURTENISSEN g ON g.id = r.IdGebeurtenis
                    JOIN kiss.tblDOCUMENTEN d ON d.id = g.iddocument
                    JOIN kiss.tblENTITEITEN e ON e.id = r.IdRelatieNaar
                WHERE r.IdRelatieNaar = {entiteit_id}
        """
        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows(sql)
        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        flattened_result = [sub[0] for sub in result or [] if sub]
        return flattened_result
    


    def get_dossier_by_name(self, dossier_naam):
        sql = "select * from kiss.tblDOSSIERS d where upper(Naam) = '" + dossier_naam + "'"

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows_with_column_names(sql)
        return result

