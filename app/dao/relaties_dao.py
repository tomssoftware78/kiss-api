from kissutils import database_instance
import logging

class RelatiesDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_relaties_with_entiteiten(self, entiteitId):
        select_clause = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
        from_clause = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieNaar = e.ID "
        where_clause = "where r.IdRelatieVan = " + entiteitId
        
        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        #result = database_instance.fetch_rows(sql)
        #result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        resultaten = database_instance.fetch_rows_with_column_names(sql) #this is always a list of dictionaries.
                                                                            #dictionary: KEY = column name, VALUE = column value
        
        #return result
        return resultaten