from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class DossiersDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_dossier_historiek_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "dh.ID, dh.IdDossier, dh.IdAard, dh.Info, dh.Datum, dh.InfoParket "
        from_clause = "from kiss.tblDossierHistoriek dh "
        where_clause = "where dh.ID > " + str(last_id) + " "
        order_clause = "order by dh.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
    def get_dossiers_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "d.ID, d.Naam, d.Notitienummer, d.NotitienummerParket, d.IdAardDossier, d.IdTypeDossier "
        from_clause = "from kiss.tblDOSSIERS d "
        where_clause = "where d.ID > " + str(last_id) + " "
        order_clause = "order by d.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    def get_documenten_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "d.ID, d.IdDossier, d.IdEenheid, d.IdAardDocument "
        from_clause = "from kiss.tblDOCUMENTEN d "
        where_clause = "where d.ID > " + str(last_id) + " "
        order_clause = "order by d.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    def get_gebeurtenissen_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "g.ID, g.IdDocument "
        from_clause = "from kiss.tblGEBEURTENISSEN g "
        where_clause = "where g.ID > " + str(last_id) + " "
        order_clause = "order by g.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    def get_relaties_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "r.ID, r.IdGebeurtenis, r.IdRelatieVan, r.IdRelatieNaar, r.Label, r.DatumVatting "
        from_clause = "from kiss.tblRELATIES r "
        where_clause = "where r.ID > " + str(last_id) + " "
        order_clause = "order by r.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
