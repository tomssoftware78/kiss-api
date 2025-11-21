import logging

class RechtspersoonLikeThisQueryBuilder:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def __build_where_for_nummer(self, nummer, naam):
        result = ''
        if nummer:
            result = "(r.Nr = '" + nummer + "' or r.Nr = '0" + nummer + "')"

        return result
    
    def __build_where_for_naam(self, nummer, naam):
        result = ''
        if naam:
            if nummer:
                result = " or "
            result = result + "r.Naam like '%" + naam + "%'"

        return result
    
    def build_query(self, nummer, naam):
        select_clause = "select ent.*, r.* "
        from_clause = "from kiss.tblENTITEITEN ent inner join kiss.tblENTRechtsPersoon r on r.IdEntiteit = ent.ID "
        where_clause = "where " 
        where_clause = where_clause + self.__build_where_for_nummer(nummer=nummer, naam=naam)
        where_clause = where_clause + self.__build_where_for_naam(nummer=nummer, naam=naam)

        sql = select_clause + from_clause + where_clause
        sql = sql + " ORDER BY r.Naam"

        self.logger.info("SQL: %s", sql)
                 
        return sql
