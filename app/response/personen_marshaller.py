import logging
import os
from uuid import UUID

from dao.personen_dao import PersonenDao
from model import KissUser

class PersonenMarshaller:

    columns = [
                "ID", 
                "EntiteitVatting", 
                "Creatie", 
                "LaatsteWijziging", 
                "Naam", 
                "Voornaam", 
                "Dag", 
                "Maand", 
                "Jaar", 
                "Geboorteplaats", 
                "Nationaliteit", 
                "Geslacht", 
                "Bijnaam", 
                "Info", 
                "AFIS"
            ]

    

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    def marshal_result(self, personen: list):
        return [
                    dict(
                            zip(self.columns, p)
                        ) for p in personen
                ]
