import logging

from dao.kiss.gebruikers_profielen_dao import GebruikersProfielenDao
from dao.kiss.gebruikers_dao import GebruikersDao
from service.kiss_tools import KissTools

class SearchQueryBuilder:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def __init__(self):
        self.gebruikers_profielen_dao = GebruikersProfielenDao()   
        self.gebruikers_dao = GebruikersDao()  
    
    def build_for_items(self, item_ids: list[int], badge_id: int):
        string_list = ",".join(str(num) for num in item_ids)

        sql = "SELECT c.ID as id, c.IdDetail AS Number, c.reserv1 AS sin, c.merk->beschrijving AS mark_model_str, " \
                "c.type AS type, {fn CONCAT({fn CONCAT(g.Voornaam, ' ')}, g.naam)} AS operator_identity, " \
                "c.idRelatie->idgebeurtenis->idDocument->Docnr AS pv_number, c.prioriteit AS urgent, " \
                "CONVERT(VARCHAR(20),c.DatumIn, 111) AS Date_in, CONVERT(VARCHAR(20),c.DatumIBN, 111) AS Date_end, CONVERT(VARCHAR(20),c.DatumOut, 111) AS Date_out " \
                "FROM KISS.tblCCUdetail c LEFT JOIN Kiss.tblgebruikers g ON c.nagezienDoor = g.Stamnummer " \
                "WHERE c.DatumOUT <> \"1900-01-01\" AND c.ID in (" + string_list + ") "

        if self.__check_limited_to_team(badge_id):
            teamId = str(self.__get_team(badge_id))
            sql = sql + " AND c.idRelatie->idgebeurtenis->idDocument->iddossier->idTeam = " + teamId

        sql = sql + " ORDER BY id DESC"

        self.logger.info("SQL: %s", sql)
                 
        return sql

    def build_for_get_kiss_items_from_case(self, case_id: int, badge_id: int):
        sql = "SELECT c.ID as id, c.IdDetail AS Number, c.reserv1 AS sin, c.merk->beschrijving AS mark_model_str, " \
            "c.type AS type, {fn CONCAT({fn CONCAT(g.Voornaam, ' ')}, g.naam)} AS operator_identity, " \
            "c.idRelatie->idgebeurtenis->idDocument->Docnr AS pv_number, c.prioriteit AS urgent, " \
            "CONVERT(VARCHAR(20),c.DatumIn, 111) AS Date_in, CONVERT(VARCHAR(20),c.DatumIBN, 111) AS Date_end, CONVERT(VARCHAR(20),c.DatumOut, 111) AS Date_out, " \
            " c.opdracht->beschrijving AS opdracht " \
            "FROM KISS.tblCCUdetail c LEFT JOIN Kiss.tblgebruikers g ON c.nagezienDoor = g.Stamnummer " \
            "WHERE c.DatumOUT <> \"1900-01-01\" AND c.IdDetail like '" + KissTools.convertCaseIDToKissDetail(case_id) + "%' "
        
        if self.__check_limited_to_team(badge_id):
            teamId = str(get_team(badge_id))
            sql = sql + " AND c.idRelatie->idgebeurtenis->idDocument->iddossier->idTeam = " + teamId

        sql = sql + " ORDER BY id DESC"

        self.logger.info("SQL: %s", sql)
                 
        return sql


    def build_for_search_kiss_case(self, term: str, badge_id: int):
        term4chars = term.rjust(4, "0")
        self.logger.info("term4chars: %s", term4chars)

        sql = "SELECT TOP 10 c.IdDetail AS id, c.idRelatie->idgebeurtenis->idDocument->iddossier->Naam AS CaseName, " \
        "c.idRelatie->idgebeurtenis->idDocument->iddossier->notitienummer AS last_notice, " \
        "c.idRelatie->idgebeurtenis->idDocument->iddossier->idMagistraat->Naam AS last_magistrat, " \
        "{fn CONCAT({fn CONCAT(g.Voornaam, ' ')}, g.naam)} AS last_enqueteur, g.paswoord AS last_email, " \
        "c.idRelatie->idgebeurtenis->idDocument->iddossier->idEenheid->Naam AS last_service " \
        "FROM KISS.tblCCUdetail c LEFT JOIN Kiss.tblgebruikers g ON c.nagezienDoor = g.Stamnummer " \
        "WHERE c.DatumOUT <> \"1900-01-01\" "

        termcondition = "c.IdDetail like 'RCCU/%" + term4chars + "/0%'"

        if not term.isdigit():
            # also check names of cases
            termcondition = termcondition + " OR c.idRelatie->idgebeurtenis->idDocument->iddossier->Naam like '%" + str(term) + "%'"

        sql = sql + " AND (" + termcondition + ")"

        if (self.__check_limited_to_team(badge_id=badge_id)):
            teamId = str(self.__get_team(badge_id))
            sql = sql + " AND c.idRelatie->idgebeurtenis->idDocument->iddossier->idTeam = " + teamId

        sql = sql + " ORDER BY id DESC"

        self.logger.info("SQL: %s", sql)
                 
        return sql


    def __check_limited_to_team(self, badge_id):
        result = self.gebruikers_profielen_dao.get_toelatingen(badge_id=badge_id)

        for row in result:
            return row[0] == 3

        return True

    def __get_team(self, badge_id):
        result = self.gebruikers_dao.get_team(badge_id=badge_id)

        for row in result:
            return row[0]

        return ""
    