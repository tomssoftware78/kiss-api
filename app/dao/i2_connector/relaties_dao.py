from kissutils import database_instance
import logging
from more_itertools import chunked

class RelatiesDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def __split_list(self, arguments: list):
        return list(chunked(arguments, 1000))

    def test(self, gebeurtenis_ids):
        all_results = []
        gebeurtenis_ids_chunks = self.__split_list(gebeurtenis_ids)

        for chunk in gebeurtenis_ids_chunks:
            
            select_clause = "select r.ID as RelatieID, r.*, e_van.ID as ID_van, e_van.EntiteitVatting as vatting_van, e_van.Type as type_van, "
            select_clause = select_clause + "e_naar.ID as ID_naar, e_naar.EntiteitVatting as vatting_naar, e_naar.Type as type_naar "
            from_clause = "FROM kiss.tblRELATIES r LEFT JOIN kiss.tblENTITEITEN e_van on r.IdRelatieVan = e_van.ID "
            from_clause = from_clause + "LEFT JOIN kiss.tblENTITEITEN e_naar on r.IdRelatieNaar = e_naar.ID "

            where_clause = "where r.IdGebeurtenis in (" + ", ".join(str(x) for x in chunk) + ")"

            sql = f"""
                {select_clause}
                {from_clause}
                {where_clause}
            """

            self.logger.debug("SQL (chunk %d-%d): %s", chunk[0], chunk[-1], sql)

            # Ophalen van resultaten voor deze chunk
            resultaten = database_instance.fetch_rows_with_column_names(sql)

            # Voeg toe aan verzameling
            all_results.extend(resultaten)
        return all_results
    

    def get_relaties_with_entiteiten_for_gebeurtenissen(self, gebeurtenis_ids):
        all_results = []
        gebeurtenis_ids_chunks = self.__split_list(gebeurtenis_ids)

        for chunk in gebeurtenis_ids_chunks:
            # Bouw WHERE-clause voor deze chunk
            where_clause_van = "where r.IdGebeurtenis in (" + ", ".join(str(x) for x in chunk) + ")"
            where_clause_naar = "where r.IdGebeurtenis in (" + ", ".join(str(x) for x in chunk) + ")"

            select_clause_van = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
            from_clause_van = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieVan = e.ID "

            select_clause_naar = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
            from_clause_naar = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieNaar = e.ID "

            sql = f"""
                {select_clause_van}
                {from_clause_van}
                {where_clause_van}
                UNION
                {select_clause_naar}
                {from_clause_naar}
                {where_clause_naar}
            """

            self.logger.debug("SQL (chunk %d-%d): %s", chunk[0], chunk[-1], sql)

            # Ophalen van resultaten voor deze chunk
            resultaten = database_instance.fetch_rows_with_column_names(sql)

            # Voeg toe aan verzameling
            all_results.extend(resultaten)
        return all_results
        
#        select_clause_van = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
#        from_clause_van = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieVan = e.ID "
#        where_clause_van = "where r.IdGebeurtenis in (" + ", ".join(str(x) for x in (gebeurtenis_ids)) + ")"

#        select_clause_naar = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
#        from_clause_naar = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieNaar = e.ID "
#        where_clause_naar = "where r.IdGebeurtenis in (" + ", ".join(str(x) for x in (gebeurtenis_ids)) + ")"
        
#        sql = f"""
#                {select_clause_van}
#                {from_clause_van}
#                {where_clause_van}
#                UNION
#                {select_clause_naar}
#                {from_clause_naar}
#                {where_clause_naar}
#            """
        
#        self.logger.debug("SQL: %s", sql)
#        resultaten = database_instance.fetch_rows_with_column_names(sql) #this is always a list of dictionaries.
                                                                            #dictionary: KEY = column name, VALUE = column value
        
#        return resultaten
        
    def get_relaties_with_entiteiten(self, entiteitId):
        select_clause_van = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
        from_clause_van = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieVan = e.ID "
        where_clause_van = "where r.IdRelatieVan = " + entiteitId

        select_clause_naar = "select r.ID as RelatieID, r.*, e.*, e.ID as IdEntiteit "
        from_clause_naar = "from kiss.tblRELATIES r inner join kiss.tblENTITEITEN e on r.IdRelatieNaar = e.ID "
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