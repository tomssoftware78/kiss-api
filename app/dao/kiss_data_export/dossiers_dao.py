from kissutils import database_instance
from dao.util import kiss_db_table_mapping
import logging

class DossiersDao:

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def get_dossiers_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "d.ID, d.Naam, d.Notitienummer, d.NotitienummerParket, d.IdTeam, d.IdMagistraat, d.IdBomMagistraat, d.IdScharnierMagistraat, "
        select_clause += "d.DossierNummerOR, d.IdOR, d.IdAardDossier, d.IdTypeDossier, d.IdFenomeen, d.IdDadergroep, d.IdTypeDadergroep, d.GevoeligDossier, "
        select_clause += "d.ILPType, d.IdOorsprongDossier, d.PlaatsArchief, d.IdEenheid, d.Status, d.FenomeenBeheerder, d.BP, d.ONDos, d.idSite "
        from_clause = "from kiss.tblDOSSIERS d "
        where_clause = "where d.ID > " + str(last_id) + " "
        order_clause = "order by d.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    def get_documenten_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "d.ID, d.IdDossier, d.DocNr, d.RefDoc, d.DatumDocument, d.IdEenheid, d.Opsteller, d.Onderwerp, d.DossierSub, d.IdTypeDocument, "
        select_clause += "d.IdAardDocument, d.Afhandeling, d.Betrouwbaarheid, d.Juistheid, d.IdDadergroep, d.OMARead, d.DatumDocIn, d.DatumCreatie, "
        select_clause += "d.DatumLaatsteWijziging "
        from_clause = "from kiss.tblDOCUMENTEN d "
        where_clause = "where d.ID > " + str(last_id) + " "
        order_clause = "order by d.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    def get_gebeurtenissen_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "g.ID, g.IdDocument, g.RefGeb, g.DatumLaag, g.DatumHoog, g.JuistheidTijdstip, g.Inhoud, g.KorteInhoud, g.Restinfo, "
        select_clause += "g.RestinfoValidatie, g.IAIntrest, g.OMARead, g.SyncId, g.InhoudAscii "
        from_clause = "from kiss.tblGEBEURTENISSEN g "
        where_clause = "where g.ID > " + str(last_id) + " "
        order_clause = "order by g.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result

    def get_relaties_paged(self, page_size: int, last_id: int):
        select_clause = "select top " + str(page_size) + " "
        select_clause += "r.ID, r.IdGebeurtenis, r.IdRelatieVan, r.ThemaVan, r.TeDoenVan, r.TeDoenVanOk, r.IdRelatieNaar, r.ThemaNaar, "
        select_clause += "r.TeDoenNaar, r.TeDoenNaarOk, r.Label, r.IdRelatieType, r.DatumVatting, r.idRelatieRichting, r.SyncId "
        from_clause = "from kiss.tblRELATIES r "
        where_clause = "where r.ID > " + str(last_id) + " "
        order_clause = "order by r.ID";

        sql = select_clause + from_clause + where_clause + order_clause
        #self.logger.debug("SQL: %s", sql)
        
        result = database_instance.fetch_rows_with_column_names(sql)

        return result
