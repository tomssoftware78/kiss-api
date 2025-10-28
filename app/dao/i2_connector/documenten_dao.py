from kissutils import database_instance
import logging

class DocumentenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_document_ids_by_dossier_id(self, dossier_id):
        select_clause_van = "select d.ID "
        from_clause_van = "from kiss.tblDOCUMENTEN d "
        where_clause_van = "where d.IdDossier = " + str(dossier_id)

        sql = f"""
                {select_clause_van}
                {from_clause_van}
                {where_clause_van}
            """

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows(sql)
        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        flattened_result = [sub[0] for sub in result or [] if sub]
        return flattened_result