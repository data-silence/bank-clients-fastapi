"""
This module contains Models for database tables
"""

from .db import Base
from .imports import Mapped, mapped_column


class TableClient(Base):
    """Model for Bank's clients table"""
    __tablename__ = "client"
    __table_args__ = {"schema": "public"}

    ID: Mapped[int] = mapped_column(primary_key=True, name="ID")
    AGE: Mapped[int] = mapped_column(nullable=False, name='AGE')
    GENDER: Mapped[int] = mapped_column(nullable=False, name='GENDER')
    EDUCATION: Mapped[str] = mapped_column(nullable=False, name='EDUCATION')
    MARITAL_STATUS: Mapped[str] = mapped_column(nullable=False, name='MARITAL_STATUS')
    CHILD_TOTAL: Mapped[int] = mapped_column(nullable=False, name='CHILD_TOTAL')
    DEPENDANTS: Mapped[int] = mapped_column(nullable=False, name='DEPENDANTS')
    SOCSTATUS_WORK_FL: Mapped[int] = mapped_column(nullable=False, name='SOCSTATUS_WORK_FL')
    SOCSTATUS_PENS_FL: Mapped[int] = mapped_column(nullable=False, name='SOCSTATUS_PENS_FL')
    FACT_ADDRESS_PROVINCE: Mapped[str] = mapped_column(nullable=False, name='FACT_ADDRESS_PROVINCE')
    FL_PRESENCE_FL: Mapped[int] = mapped_column(nullable=False, name='FL_PRESENCE_FL')
    OWN_AUTO: Mapped[int] = mapped_column(nullable=False, name='OWN_AUTO')
    AGREEMENT_RK: Mapped[int] = mapped_column(nullable=False, name='AGREEMENT_RK')
    TARGET: Mapped[int] = mapped_column(nullable=False, name='TARGET')
    CREDIT: Mapped[float] = mapped_column(nullable=False, name='CREDIT')
    TERM: Mapped[int] = mapped_column(nullable=False, name='TERM')
    FST_PAYMENT: Mapped[float] = mapped_column(nullable=False, name='FST_PAYMENT')
    GEN_INDUSTRY: Mapped[str] = mapped_column(nullable=False, name='GEN_INDUSTRY')
    GEN_TITLE: Mapped[str] = mapped_column(nullable=False, name='GEN_TITLE')
    JOB_DIR: Mapped[str] = mapped_column(nullable=False, name='JOB_DIR')
    WORK_TIME: Mapped[int] = mapped_column(nullable=False, name='WORK_TIME')
    FAMILY_INCOME: Mapped[str] = mapped_column(nullable=False, name='FAMILY_INCOME')
    PERSONAL_INCOME: Mapped[float] = mapped_column(nullable=False, name='PERSONAL_INCOME')


class TableY(Base):
    """Model for Y - prediction and target table"""
    __tablename__ = "y"
    __table_args__ = {"schema": "public"}

    ID: Mapped[int] = mapped_column(primary_key=True, nullable=False, name="ID")
    TARGET: Mapped[int] = mapped_column(nullable=False, name="TARGET")
    prediction_regular: Mapped[float] = mapped_column(nullable=False)
    prediction_tuned: Mapped[float] = mapped_column(nullable=False)


class SingleClientTable(Base):
    """Model for Bank's clients single table"""
    __tablename__ = "single_client"
    __table_args__ = {"schema": "public"}

    ID: Mapped[int] = mapped_column(primary_key=True, name="ID")
    AGE: Mapped[int] = mapped_column(nullable=False, name='AGE')
    GENDER: Mapped[int] = mapped_column(nullable=False, name='GENDER')
    EDUCATION: Mapped[str] = mapped_column(nullable=False, name='EDUCATION')
    MARITAL_STATUS: Mapped[str] = mapped_column(nullable=False, name='MARITAL_STATUS')
    CHILD_TOTAL: Mapped[int] = mapped_column(nullable=False, name='CHILD_TOTAL')
    DEPENDANTS: Mapped[int] = mapped_column(nullable=False, name='DEPENDANTS')
    SOCSTATUS_WORK_FL: Mapped[int] = mapped_column(nullable=False, name='SOCSTATUS_WORK_FL')
    SOCSTATUS_PENS_FL: Mapped[int] = mapped_column(nullable=False, name='SOCSTATUS_PENS_FL')
    FACT_ADDRESS_PROVINCE: Mapped[str] = mapped_column(nullable=False, name='FACT_ADDRESS_PROVINCE')
    FL_PRESENCE_FL: Mapped[int] = mapped_column(nullable=False, name='FL_PRESENCE_FL')
    OWN_AUTO: Mapped[int] = mapped_column(nullable=False, name='OWN_AUTO')
    CREDIT: Mapped[float] = mapped_column(nullable=False, name='CREDIT')
    TERM: Mapped[int] = mapped_column(nullable=False, name='TERM')
    FST_PAYMENT: Mapped[float] = mapped_column(nullable=False, name='FST_PAYMENT')
    GEN_INDUSTRY: Mapped[str] = mapped_column(nullable=False, name='GEN_INDUSTRY')
    GEN_TITLE: Mapped[str] = mapped_column(nullable=False, name='GEN_TITLE')
    JOB_DIR: Mapped[str] = mapped_column(nullable=False, name='JOB_DIR')
    WORK_TIME: Mapped[int] = mapped_column(nullable=False, name='WORK_TIME')
    FAMILY_INCOME: Mapped[str] = mapped_column(nullable=False, name='FAMILY_INCOME')
    PERSONAL_INCOME: Mapped[float] = mapped_column(nullable=False, name='PERSONAL_INCOME')


class TableSelectedModel(Base):
    """Model for user selection model and params"""
    __tablename__ = "selected_model"
    __table_args__ = {"schema": "public"}

    type_model: Mapped[str] = mapped_column(primary_key=True, name='model_type')
    threshold: Mapped[float] = mapped_column(nullable=False)
