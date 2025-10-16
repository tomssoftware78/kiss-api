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
        select_clause_van = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
        from_clause_van = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieNaar = e.ID "
        where_clause_van = "where r.IdRelatieVan = " + entiteitId

        select_clause_naar = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
        from_clause_naar = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieVan = e.ID "
        where_clause_naar = "where r.IdRelatieNaar = " + entiteitId
        
        sql = f"""
                {select_clause_van}
                {from_clause_van}
                {where_clause_van}
                UNION
                {select_clause_naar}
                {from_clause_naar}
                {where_clause_naar}
            """

#        sql = f"""SELECT r.ID AS RelatieID, r.*, e.*, e.ID AS IdEntiteit
#FROM (
#    SELECT TOP 3 *
#    FROM kiss.tblRELATIES
#    WHERE IdRelatieVan = 4331
#    ORDER BY ID DESC
#) r
#INNER JOIN kiss.tblENTITEITEN e ON r.IdRelatieNaar = e.ID
#
#UNION all
#
#SELECT r.ID AS RelatieID, r.*, e.*, e.ID AS IdEntiteit
#FROM (
#    SELECT TOP 2 *
#    FROM kiss.tblRELATIES
#    WHERE IdRelatieNaar = 4331
#    ORDER BY ID DESC
#) r
#INNER JOIN kiss.tblENTITEITEN e ON r.IdRelatieVan = e.ID
#"""

        self.logger.debug("SQL: %s", sql)
        #result = database_instance.fetch_rows(sql)
        #result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        resultaten = database_instance.fetch_rows_with_column_names(sql) #this is always a list of dictionaries.
                                                                            #dictionary: KEY = column name, VALUE = column value
        
        #return result
        return resultaten