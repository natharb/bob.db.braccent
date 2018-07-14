#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nathália Alves Rocha Batista

"""
Table models and functionality for the BRACCENT DATABASE

"""

import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, or_, and_, not_
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import bob.db.base

import os

Base = declarative_base()

""" Defining protocols. Yes, they are static """

PROTOCOLS = ('closedset_braccent_fold1', 'closedset_braccent_fold2', 'closedset_braccent_fold3', 'closedset_braccent_fold4', 'closedset_braccent_fold5', 'closedset_braccent_fold6', 'closedset_braccent_fold7', 'closedset_braccent_fold8', 'closedset_braccent_fold9', 'closedset_braccent_fold10')

GROUPS = ('world', 'dev')

PURPOSES = ('train', 'enroll', 'probe')

ACCENTS = ('Nortista', 'Baiano', 'Fluminense', 'Mineiro', 'Carioca', 'Nordestino', 'Sulista')

SEX     = ("Feminino", "Masculino")

class Protocol_File_Association(Base):
    """
    Describe the protocols
    """
    __tablename__ = 'protocol_file_association'

    protocol = Column('protocol', Enum(*PROTOCOLS), primary_key=True)
    group = Column('group', Enum(*GROUPS), primary_key=True)
    purpose = Column('purpose', Enum(*PURPOSES), primary_key=True)

    file_id = Column('file_id', Integer, ForeignKey('file.id'), primary_key=True)

    def __init__(self, protocol, group, purpose, file_id):
        self.protocol = protocol
        self.group = group
        self.purpose = purpose
        self.file_id = file_id
        # self.client_id = client_id


class File(Base, bob.db.base.File):
    """
    Information about the files of the BRACCENT database.

    Each file includes
    * the client id
    """
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    path = Column(String(300), unique=True)
    client_id = Column(Enum(*ACCENTS)) # Compatible with bob.bio.base
    sex = Column(Enum(*SEX))

    def __init__(self, id, path, accent, sex):
        # call base class constructor
        bob.db.base.File.__init__(self, file_id=id, path=path)
        self.client_id = accent
        self.sex = sex

