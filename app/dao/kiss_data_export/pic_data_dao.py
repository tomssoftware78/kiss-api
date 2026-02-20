from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class PicDataDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_dossier_types_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "dt.ID, dt.Beschrijving, dt.BeschrijvingFR, dt.BeschrijvingDE, dt.BeschrijvingEN "
        from_clause = "from kiss.PicDossierType dt "
        where_clause = "where dt.ID > " + str(last_id) + " "
        order_clause = "order by dt.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
    
    def get_tel_tech_nrs(self, page_size: int, last_id: int):
        #offset = (page - 1) * page_size
        
        select_clause = "select top " + str(page_size) + " "
        select_clause += "%ID, Nummer, Info "
        from_clause = "from kiss.picTelTechNrs "
        where_clause = "where %ID > " + str(last_id) + " "
        order_clause = "order by %ID"

        sql = select_clause + from_clause + where_clause + order_clause

        #sql = f"""
        #    SELECT TOP {page_size} Nummer, Info
        #    FROM KISS.picTelTechNrs
        #    WHERE %ID NOT IN (
        #        SELECT TOP {offset} %ID
        #        FROM KISS.picTelTechNrs
        #        ORDER BY Nummer, %ID
        #    )
        #    ORDER BY Nummer, %ID
        #    """
        
        self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result