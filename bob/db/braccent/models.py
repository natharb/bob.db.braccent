#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira<tiago.pereira@idiap.ch>
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

PROTOCOLS = ('braccent_fold1')

GROUPS = ('world', 'dev')

PURPOSES = ('train', 'enroll', 'probe')

# TODO: FILL THE GAPS HERE
ACCENTS = ('')


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

    modality_choices = ('photo', 'sketch')

    id = Column(Integer, primary_key=True)
    path = Column(String(100), unique=True)
    accent = Column(Enum(*ACCENTS))

    def __init__(self, id, path, accent):
        # call base class constructor
        bob.db.base.File.__init__(self, file_id=id, path=path)
        self.accent = accent

