"""
This module contains FastApi Models for Bank Clients App
"""

from .imports import BaseModel, Enum


class ModelNames(str, Enum):
    """"Enum Class, contains the available y types from Y tables"""
    REGULAR = 'regular'
    TUNED = "tuned"


class Client(BaseModel):
    """Client table data schema for Pydantic model"""
    ID: int
    AGE: int
    GENDER: int
    EDUCATION: str
    MARITAL_STATUS: str
    CHILD_TOTAL: int
    DEPENDANTS: int
    SOCSTATUS_WORK_FL: int
    SOCSTATUS_PENS_FL: int
    FACT_ADDRESS_PROVINCE: str
    FL_PRESENCE_FL: int
    OWN_AUTO: int
    CREDIT: float
    TERM: int
    FST_PAYMENT: float
    GEN_INDUSTRY: str
    GEN_TITLE: str
    JOB_DIR: str
    WORK_TIME: int
    FAMILY_INCOME: str
    PERSONAL_INCOME: float
    AGREEMENT_RK: int
    TARGET: int

    class Config:
        from_orm = True


class ClientShort(BaseModel):
    """Client table data schema for Pydantic model"""
    ID: int
    AGE: int
    GENDER: int
    EDUCATION: str
    MARITAL_STATUS: str
    CHILD_TOTAL: int
    DEPENDANTS: int
    SOCSTATUS_WORK_FL: int
    SOCSTATUS_PENS_FL: int
    FACT_ADDRESS_PROVINCE: str
    FL_PRESENCE_FL: int
    OWN_AUTO: int
    CREDIT: float
    TERM: int
    FST_PAYMENT: float
    GEN_INDUSTRY: str
    GEN_TITLE: str
    JOB_DIR: str
    WORK_TIME: int
    FAMILY_INCOME: str
    PERSONAL_INCOME: float

    class Config:
        from_attributes = True


class Y(BaseModel):
    """Y table data schema for Pydantic model"""
    ID: int
    TARGET: int
    prediction_regular: float
    prediction_tuned: float

    class Config:
        from_orm = True


class SelectedModel(BaseModel):
    """Client table data schema for Pydantic"""
    type_model: str
    threshold: float

    class Config:
        from_attributes = True


if __name__ == "__main__":
    pass
