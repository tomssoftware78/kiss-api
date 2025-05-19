from pydantic import BaseModel
from typing import Union
from datetime import datetime, timedelta, date

class Item(BaseModel):
    name: str

    @classmethod
    def custom_init(cls, name: str):
        return cls(name=name)

class KissCase(BaseModel):
    id: int
    name: str
    last_notice: Union[str, None]
    last_magistrat: Union[str, None]
    last_enqueteur: Union[str, None]
    last_email: Union[str, None]
    last_service: Union[str, None]

    @classmethod
    def custom_init(cls, id: int, name: str, last_notice: str, last_magistrat: str,
                    last_enqueteur: str, last_email: str, last_service: str):
        return cls(id=id,
               name=name,
               last_notice=last_notice,
               last_magistrat=last_magistrat,
               last_enqueteur=last_enqueteur,
               last_email=last_email,
               last_service=last_service)

class KissUser(BaseModel):
    uuid: str
    badgeid: str
    firstName: str
    lastName: str
    email: str
    unit: str
    division: str
    operator: bool
    staff: bool
    superuser: bool
    language: str
    mobilePhone: Union[str, None]
    officePhone: Union[str, None]

    @classmethod
    def custom_init(cls, uuid: str, badgeid: str, firstName: str, lastName: str,
                    email: str, unit: str, division: str, operator: bool, staff: bool,
                    superuser: bool, language: str, mobilePhone: str, officePhone: str):
        return cls(uuid=uuid,
                   badgeid=badgeid,
                   firstName=firstName,
                   lastName=lastName,
                   email=email,
                   unit=unit,
                   division=division,
                   operator=operator,
                   staff=staff,
                   superuser=superuser,
                   language=language,
                   mobilePhone=mobilePhone,
                   officePhone=officePhone)

class KissItem(BaseModel):
    id: int
    number: str
    sin: Union[str, None]
    mark_model_str: Union[str, None]
    type: Union[str, None]
    operator_identity: Union[str, None]
    pv_number: Union[str, None]
    urgent: bool
    date_in: date
    date_end: date
    date_out: date

    @classmethod
    def custom_init(cls, id: int, number: str, sin: str, mark_model_str: str, type: str, operator_identity: str,
                    pv_number: str, urgent: bool, date_in: date, date_end: date, date_out: date):

        return cls(id=id,
                   number=number,
                   sin=sin,
                   mark_model_str=mark_model_str,
                   type=type,
                   operator_identity=operator_identity,
                   pv_number=pv_number,
                   urgent=urgent,
                   date_in=date_in,
                   date_end=date_end,
                   date_out=date_out)