from kissutils import database_instance
from .persoon_like_this_query_builder import PersoonLikeThisQueryBuilder 
from dao.util import kiss_db_table_mapping
import logging

class EntiteitenDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_persoon_entiteiten_like_this(self, voornaam, naam, id):
        query_builder = PersoonLikeThisQueryBuilder()
        sql = query_builder.build_query(voornaam=voornaam, naam=naam, id=id)

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
        select_clause = "select ent.* "
        from_clause = "from kiss.tblENTITEITEN ent "
        where_clause = "where ent.EntiteitVatting like '%" + vatting + "%'"

        if type and type.lower() != 'none':
            where_clause += "and ent.type = " + type

        sql = select_clause + from_clause + where_clause
        self.logger.debug("SQL: %s", sql)
        
        entiteiten_with_names = database_instance.fetch_rows_with_column_names(sql)
        entiteit_ids_for_details = {
            1: [], #persoon
            2: [], #voertuig
            3: [], #location
            4: [], #nummer
            5: [], #voorwerp
            6: [], #rechtspersoon
            7: [] #Feit
        }

        for r in entiteiten_with_names:
            #self.logger.debug(r)
            #self.logger.debug(r['Type'])
            entiteit_ids_for_details[r['Type']].append(r['ID'])


        details_in_sub = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: []
        }
        for s in entiteit_ids_for_details:
            if len(entiteit_ids_for_details[s]) > 0:
                sql = "select * from " + kiss_db_table_mapping.entiteit_table_mapping[s]['tabel']
                sql = sql + " where IdEntiteit in (" + ", ".join(str(x) for x in (entiteit_ids_for_details[s])) + ")"

                self.logger.debug("SQL: %s", sql)
                sub_result_with_names = database_instance.fetch_rows_with_column_names(sql)
                details_in_sub[s] = sub_result_with_names

                #self.logger.debug(sub_result_with_names)


        indexes_in_sub = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0
        }
        
        for r in entiteiten_with_names:
            k = r['Type']

            index_in_sub = indexes_in_sub[k]

            details = details_in_sub[k][index_in_sub]
            details['Type'] = r['Type']

            r['details'] = details

            index_in_sub+= 1
            indexes_in_sub[k] = index_in_sub


        #self.logger.debug(entiteit_ids_for_details)
        #self.logger.debug(entiteiten_with_names)    
        #this for loop is just debugging info 
        for r in entiteiten_with_names:
            id = r['ID']
            if not r['details']:
                print('entiteit with id', id, 'has no details found')
            else:
                details = r['details']
                if details['IdEntiteit'] != id:
                    print('id ', id, 'is not equal to ', details['IdEntiteit'])
            
        return entiteiten_with_names
    
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