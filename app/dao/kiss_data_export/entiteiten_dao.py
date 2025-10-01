from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class EntiteitenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_personen_count(self):
        select_clause = "select count(*) "
        from_clause = "from kiss.tblENTPersonen"

        sql = select_clause + from_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows(sql)

        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples

        #self.logger.debug(result)
        #self.logger.debug(result[0])
        #self.logger.debug(result[0][0])

        return result[0][0]

    def get_personen_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "e.ID, e.EntiteitVatting, e.Type, e.Icoon, e.oldIdKISS, e.creatie, e.laatsteWijziging, e.gebruikerLaatsteWijziging, e.entIcoon, "
        select_clause += "p.IdEntiteit, p.Naam, p.Voornaam, p.Dag, p.Maand, p.Jaar, p.Geboorteplaats, p.Nationaliteit, p.Geslacht, p.Bijnaam, p.Info, p.AFIS "
        from_clause = "from kiss.tblENTITEITEN e LEFT OUTER JOIN kiss.tblENTPersonen p on e.ID = p.IdEntiteit "
        where_clause = "where e.Type = 1 and p.IdEntiteit > " + str(last_id) + " "
        order_clause = "order by p.IdEntiteit";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result


    def get_entiteiten_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "e.ID, e.EntiteitVatting, e.Type, e.Icoon, e.oldIdKISS, e.creatie, e.laatsteWijziging, e.gebruikerLaatsteWijziging, e.entIcoon "
        from_clause = "from kiss.tblENTITEITEN e "
        where_clause = "where e.ID > " + str(last_id) + " "
        order_clause = "order by e.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
    