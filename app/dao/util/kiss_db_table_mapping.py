entiteit_table_mapping = {
    1: {
            'tabel': 'kiss.tblENTPersonen',
            'naam': 'persoon',
            'details': [
                "IdEntiteit", "Naam", "Voornaam", "Dag", "Maand", "Jaar", "Geboorteplaats", 
                "Nationaliteit", "Geslacht", "Bijnaam", "Info", "AFIS"
            ]
        },
    2: {
            'tabel': 'kiss.tblENTVoertuig',
            'naam': 'voertuig',
            'details': [
                "IdEntiteit", "Kenteken", "Chassis", "Merk", "Type", "Kleur", "Aard", 
                "Nationaliteit", "Info"
            ]
        },
    3: {
            'tabel': 'kiss.tblENTLocaties',
            'naam': 'locatie',
            'details': [
                "IdEntiteit", "idREFTABLand", "Provincie", "idREFTABProvincie", "Gemeente", "idREFTABGemeente", "DeelGemeente", 
                "idREFTABDeelGemeente", "idREFTABStraat", "Straat", "Nr", "Postcode", "AardLocatie", "Info", "VrijeVelden", 
                "latitude", "longitude"
            ]
        },
    4: {
            'tabel': 'kiss.tblENTNummer',
            'naam': 'nummer',
            'details': [
                "IdEntiteit", "Nummer", "Type", "Info", "IdNationaliteit"
            ]
        },
    5: {
            'tabel': 'kiss.tblENTVoorwerp',
            'naam': 'voorwerp',
            'details': [
                "IdEntiteit", "SerieNr", "Beschrijving", "Info"
            ]
        },
    6: {
            'tabel': 'kiss.tblENTRechtsPersoon',
            'naam': 'rechtspersoon',
            'details': [
                "IdEntiteit", "Naam", "Vorm", "Nationaliteit", "Nr", "Info"
            ]
        },
    7: {
            'tabel': 'kiss.tblENTFeit',
            'naam': 'feit',
            'details': [
                "IdEntiteit", "Nummer", "Datum", "Uur", "Beschrijving", "Info"
            ]
    }
}