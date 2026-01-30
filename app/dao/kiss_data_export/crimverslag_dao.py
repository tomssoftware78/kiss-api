from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class CrimverslagDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_crimverslag_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "cv.ID, cv.Notitienummer, cv.Type, cv.Referte, cv.Aard, cv.Poging, cv.Eenheid, cv.PZ, cv.Arro, "
        select_clause += "cv.DatumImport, cv.DatumCrimverslag, cv.DatumLaag, cv.DatumHoog, cv.Localisatie, cv.Postcode, "
        select_clause += "cv.Gemeente, cv.Straat, cv.Huisnr, cv.Afgehandeld, cv.IARead, cv.IAIntrest, "
        select_clause += "cv.teVerwijderen, cv.Koppeling, cv.RefGeb "
        from_clause = "from kiss.tblCRIMVERSLAG cv "
        where_clause = "where cv.ID > " + str(last_id) + " "
        order_clause = "order by cv.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

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