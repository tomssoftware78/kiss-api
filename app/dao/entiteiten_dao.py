from kissutils import database_instance
from .persoon_like_this_query_builder import PersoonLikeThisQueryBuilder 
from .rechtspersoon_like_this_query_builder import RechtspersoonLikeThisQueryBuilder
from .locatie_like_this_query_builder import LocatieLikeThisQueryBuilder
from dao.util import kiss_db_table_mapping
import logging

class EntiteitenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_locatie_entiteiten(self, straat, nummer, land, gemeente):
        query_builder = LocatieLikeThisQueryBuilder()
        sql = query_builder.build_query(straat=straat, nummer=nummer, land=land, gemeente=gemeente)

        #self.logger.debug("SQL: %s", sql)
        entiteiten_with_names = database_instance.fetch_rows_with_column_names(sql)

        entiteiten_with_names_with_rechtspersoon_as_details = []
        if entiteiten_with_names:
            for item in entiteiten_with_names:
                keys = list(item.keys())
                first_part = {k: item[k] for k in keys[:9]}     # eerste 9
                remaining = {k: item[k] for k in keys[9:]}      # alles na de 9e
                
                if remaining:  # alleen toevoegen als er iets overblijft
                    first_part["details"] = remaining
                else:
                    first_part["details"] = {}
                
                entiteiten_with_names_with_rechtspersoon_as_details.append(first_part)

        return entiteiten_with_names_with_rechtspersoon_as_details

    def get_rechtspersoon_entiteiten(self, nummer, naam):
        query_builder = RechtspersoonLikeThisQueryBuilder()
        sql = query_builder.build_query(nummer=nummer, naam=naam)

        #self.logger.debug("SQL: %s", sql)
        entiteiten_with_names = database_instance.fetch_rows_with_column_names(sql)

        entiteiten_with_names_with_rechtspersoon_as_details = []

        if entiteiten_with_names:
            for item in entiteiten_with_names:
                keys = list(item.keys())
                first_part = {k: item[k] for k in keys[:9]}     # eerste 9
                remaining = {k: item[k] for k in keys[9:]}      # alles na de 9e
                
                if remaining:  # alleen toevoegen als er iets overblijft
                    first_part["details"] = remaining
                else:
                    first_part["details"] = {}
                
                entiteiten_with_names_with_rechtspersoon_as_details.append(first_part)

        return entiteiten_with_names_with_rechtspersoon_as_details

    
    def get_persoon_entiteiten_like_this(self, voornaam, naam):
        query_builder = PersoonLikeThisQueryBuilder()
        sql = query_builder.build_query(voornaam=voornaam, naam=naam)

        #self.logger.debug("SQL: %s", sql)
        entiteiten_with_names = database_instance.fetch_rows_with_column_names(sql)

        entiteiten_with_names_with_persoon_as_details = []

        if entiteiten_with_names:
            for item in entiteiten_with_names:
                keys = list(item.keys())
                first_part = {k: item[k] for k in keys[:9]}     # eerste 9
                remaining = {k: item[k] for k in keys[9:]}      # alles na de 9e
                
                if remaining:  # alleen toevoegen als er iets overblijft
                    first_part["details"] = remaining
                else:
                    first_part["details"] = {}
                
                entiteiten_with_names_with_persoon_as_details.append(first_part)

        return entiteiten_with_names_with_persoon_as_details

    def get_entiteiten_by_vatting(self, vatting, type):
        types = []
        if type and type.lower() != 'none':
            types.append(int(type))
        else:
            types = [1, 2, 3, 4, 5, 6, 7]


        result = []
        for t in types:    
            sub_table = kiss_db_table_mapping.entiteit_table_mapping[t]['tabel']
            prefix_sub_table = "sub_ent"
            column_names_sub_table = kiss_db_table_mapping.entiteit_table_mapping[t]["details"]
            select_sub_part = ", ".join(f"{prefix_sub_table}.{veld}" for veld in column_names_sub_table)

            print(select_sub_part)

            select_clause = "select ent.ID, ent.EntiteitVatting, ent.Type as entType, ent.Icoon, ent.oldIdKISS, ent.creatie, ent.laatsteWijziging, "
            select_clause = select_clause + "ent.gebruikerLaatsteWijziging, ent.entIcoon, " + select_sub_part + " "
            from_clause = "from kiss.tblENTITEITEN ent "
            from_clause = from_clause + "left outer join " + sub_table + " " + prefix_sub_table + " "
            from_clause = from_clause + "on sub_ent.IdEntiteit = ent.ID "
            where_clause = "where ent.EntiteitVatting like '%" + vatting + "%' "
            where_clause += "and sub_ent.IdEntiteit is not null"

            sql = select_clause + from_clause + where_clause
            self.logger.debug("SQL: %s", sql)

            entiteiten_with_names = database_instance.fetch_rows_with_column_names(sql)
        
        

            if entiteiten_with_names:
                for r in entiteiten_with_names:
                    r["details"] = {}

                    for key in kiss_db_table_mapping.entiteit_table_mapping[t]['details']:
                        r["details"][key] = r.pop(key)

                    r["Type"] = r.pop("entType")
                    result.append(r)
        return result
    
    def get_entiteit_generic_data(self, entiteitId):
        select_clause = "select * "
        from_clause = "from kiss.tblENTITEITEN e "
        where_clause = " where e.ID = " + str(entiteitId)

        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        generic_entiteit = database_instance.fetch_rows_with_column_names(sql)

        
        if not generic_entiteit:
            self.logger.warning("No results found for query: %s", sql)
            return {}

        type = generic_entiteit[0]['Type']
        detail_data = self.get_entiteit_data(entiteitId=entiteitId, entiteit_type=type)
        generic_entiteit[0]['details'] = detail_data
        return generic_entiteit[0]

    
    def get_entiteit_data(self, entiteitId, entiteit_type):
        tabel_naam = kiss_db_table_mapping.entiteit_table_mapping[entiteit_type]['tabel']

        select_clause = "select tb.*, e.EntiteitVatting "
        from_clause = "from " + tabel_naam + " tb inner join kiss.tblENTITEITEN e on tb.IdEntiteit = e.ID"
        where_clause = " where tb.IdEntiteit = " + str(entiteitId)
        
        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows_with_column_names(sql)
        #result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
        #                                        # returned from the database was a list of tuples
        result[0]['Type'] = entiteit_type
        return result[0]
    
    def get_entiteiten_data(self, entiteit_ids, entiteit_type):
        tabel_naam = kiss_db_table_mapping.entiteit_table_mapping[entiteit_type]['tabel']
        
        ids = ", ".join(map(str, entiteit_ids))

        select_clause = "select tb.*, e.EntiteitVatting "
        from_clause = "from " + tabel_naam + " tb inner join kiss.tblENTITEITEN e on tb.IdEntiteit = e.ID"
        where_clause = " where tb.IdEntiteit in (" +  ids + ")"
        
        sql = select_clause + from_clause + where_clause

        self.logger.debug("SQL: %s", sql)
        result = database_instance.fetch_rows_with_column_names(sql)
        #result = [list(row) for row in result] #Ensure we always can process with a list of lists, even when the initial result 
        #                                        # returned from the database was a list of tuples
        return result