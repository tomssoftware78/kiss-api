from kissutils import database_instance
import logging

class GebeurtenissenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_gebeurtenis_ids_for_document_ids(self, document_ids):
        select_clause = "select g.ID "
        from_clause = "from kiss.tblGEBEURTENISSEN g "
        where_clause = "where g.IdDocument in (" + ", ".join(str(x) for x in (document_ids)) + ")"

        sql = f"""
                {select_clause}
                {from_clause}
                {where_clause}
            """
        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows(sql)
        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        flattened_result = [sub[0] for sub in result or [] if sub]
        return flattened_result