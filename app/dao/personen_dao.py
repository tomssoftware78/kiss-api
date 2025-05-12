from kissutils import database_instance
import logging

class PersonenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_personen_by_name(self, name):
        select_clause = "select e.ID, e.EntiteitVatting, e.Type, e.creatie, e.laatsteWijziging, p.Naam, p.Voornaam, p.Dag, p.Maand, p.Jaar, "
        select_clause = select_clause + "p.Geboorteplaats, p.Nationaliteit, p.Geslacht, p.Bijnaam, p.Info, p.AFIS "
        from_clause = "from kiss.tblENTITEITEN e inner join kiss.tblENTPersonen p on p.IdEntiteit = e.ID "
        where_clause = "where e.type = 1 and p.Naam like '%" + name + "%'"

        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows(sql)
        result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
                                                # returned from the database was a list of tuples
        return result