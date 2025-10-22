from kissutils import database_instance
import logging

class SciRelatiesDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_relaties_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "e.ID, e.IdCIDDocument, e.IdRelatieVan, e.ThemaVan, e.TeDoenVan, e.TeDoenVanOk, e.IdRelatieNaar, e.ThemaNaar, "
        select_clause += "e.TeDoenNaar, e.TeDoenNaarOk, e.Label, e.IdRelatieType, e.DatumVatting, e.idRelatieRichting "
        from_clause = "from kiss.tblCIDRELATIES e "
        where_clause = "where e.ID > " + str(last_id) + " "
        order_clause = "order by e.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
