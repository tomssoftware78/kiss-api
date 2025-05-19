from kissutils import database_instance
import logging

class GebruikersDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_user(self, badge_id):
        select_clause = "SELECT g.Stamnummer AS badgeid, g.Naam AS lastname, g.Voornaam AS firstname, g.Paswoord AS email, e.naam AS unit, g.idTeam->beschrijving AS division "
        from_clause = "FROM kiss.tblGebruikers g LEFT JOIN kiss.piceenheden e ON (g.IdEenheid = e.id) "
        where_clause = "WHERE Stamnummer = " + str(badge_id)

        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows(sql)

        return result

    def get_team(self, badge_id):
        sql = "SELECT g.idTeam FROM kiss.tblGebruikers g WHERE Stamnummer = " + str(badge_id)
        
        self.logger.debug("SQL: %s", sql)

        result = database_instance.fetch_rows(sql)
        return result
