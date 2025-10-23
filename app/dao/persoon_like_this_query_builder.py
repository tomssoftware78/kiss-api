import logging

class PersoonLikeThisQueryBuilder:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def __build_where_for_voornaam(self, voornaam, naam, id):
        result = ''
        if voornaam:
            result = "p.Voornaam like '%" + voornaam + "%'"

        return result
    
    def __build_where_for_naam(self, voornaam, naam, id):
        result = ''
        if naam:
            if voornaam:
                result = " and "
            result = result + "p.naam like '%" + naam + "%'"

        return result
    
    def __build_where_for_id(self, voornaam, naam, id):
        result = ''
        if naam or voornaam:
            result = " and "
            
            result = result + "ent.ID != " + str(id)

        return result

    def build_query(self, voornaam, naam, id):
        select_clause = "select ent.*, p.* "
        from_clause = "from kiss.tblENTITEITEN ent inner join kiss.tblENTPersonen p on p.IdEntiteit = ent.ID "
        where_clause = "where " 
        where_clause = where_clause + self.__build_where_for_voornaam(voornaam=voornaam, naam=naam, id=id)
        where_clause = where_clause + self.__build_where_for_naam(voornaam=voornaam, naam=naam, id=id)
        where_clause = where_clause + self.__build_where_for_id(voornaam=voornaam, naam=naam, id=id)

        sql = select_clause + from_clause + where_clause
        sql = sql + " ORDER BY p.naam, p.Voornaam"

        self.logger.info("SQL: %s", sql)
                 
        return sql
