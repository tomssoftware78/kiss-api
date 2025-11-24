import logging

class LocatieLikeThisQueryBuilder:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def __build_where_for_straat(self, straat, nummer, land, gemeente):
        result = ''
        if straat:
            result = "l.Straat like '%" + straat + "%'"

        return result
    
    def __build_where_for_nummer(self, straat, nummer, land, gemeente):
        result = ''
        if nummer:
            if straat:
                result = " and "
            result = result + "l.Nr like '%" + nummer + "%'"

        return result
    
    def __build_where_for_land(self, straat, nummer, land, gemeente):
        result = ''
        #if naam:
        #    if voornaam:
        #        result = " and "
        #    result = result + "l.naam like '%" + naam + "%'"

        return result
    
    def __build_where_for_gemeente(self, straat, nummer, land, gemeente):
        result = ''
        if gemeente:
            if straat or nummer:
                result = " and "
            result = result + "l.Gemeente like '%" + gemeente + "%'"

        return result
    
    def build_query(self, straat, nummer, land, gemeente):
        select_clause = "select ent.*, l.*, c.CouTextBD "
        from_clause = "from kiss.tblENTITEITEN ent inner join kiss.tblENTLocaties l on l.IdEntiteit = ent.ID "
        from_clause += "left join reftab.rCou c on l.idREFTABLand = c.CouKey "
        where_clause = "where "
        where_clause = where_clause + self.__build_where_for_straat(straat=straat, nummer=nummer, land=land, gemeente=gemeente)
        where_clause = where_clause + self.__build_where_for_nummer(straat=straat, nummer=nummer, land=land, gemeente=gemeente)
        where_clause = where_clause + self.__build_where_for_land(straat=straat, nummer=nummer, land=land, gemeente=gemeente)
        where_clause = where_clause + self.__build_where_for_gemeente(straat=straat, nummer=nummer, land=land, gemeente=gemeente)


        sql = select_clause + from_clause + where_clause
        sql = sql + " ORDER BY l.Gemeente, l.Straat"

        self.logger.info("SQL: %s", sql)
                 
        return sql
