from kissutils import database_instance
import logging

class GebruikersProfielenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_toelatingen(self, badge_id):
        sql = """SELECT  min(tdn.Toelating) AS Toelating FROM KISS.tblGebruikersProfielen g 
                 LEFT JOIN KISS.tblToegangsDomeinen tdn ON (g.idProfiel = tdn.IdProfiel) 
                 LEFT JOIN KISS.tblToegangDomein td ON (td.IdToegangsDomein= tdn.IdToegangsDomein) 
                 WHERE tdn.IdToegangsDomein = 2 AND g.IdStamnummer = """
        sql = sql + str(badge_id)

        self.logger.debug("SQL: %s", sql)

        result = database_instance.fetch_rows(sql)