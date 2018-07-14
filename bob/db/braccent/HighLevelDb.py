#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

"""
Database plugin (HighLEvel DB) that connects with bob.bio.base
"""

from bob.bio.spear.database import AudioBioFile
from bob.bio.base.database import BioDatabase


class BraccentBioFile(AudioBioFile):

    def __init__(self, f):
        super(BraccentBioFile, self).__init__(client_id=f.client_id, path=f.path, file_id=f.id)
        self._f = f


class BraccentBioDatabase(BioDatabase):
    """
    Braccent Database plugin (HighLEvel DB) that connects with bob.bio.base
    """

    def __init__(
            self,
            original_directory=None,
            original_extension=None,
            **kwargs
    ):
        from bob.db.braccent.query import Database as LowLevelDatabase
        self._db = LowLevelDatabase(original_directory, original_extension)

        # call base class constructors to open a session to the database
        super(BraccentBioDatabase, self).__init__(
            name='braccent',
            original_directory=original_directory,
            original_extension=original_extension,
            **kwargs)

    @property
    def original_directory(self):
        return self._db.original_directory

    @original_directory.setter
    def original_directory(self, value):
        self._db.original_directory = value

    def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
        return self._db.model_ids(groups=groups, protocol=protocol)

    def objects(self, groups=None, protocol=None, purposes=None, model_ids=None, **kwargs):
        retval = self._db.objects(groups=groups, protocol=protocol, purposes=purposes, model_ids=model_ids, **kwargs)
        return [BraccentBioFile(f) for f in retval]
        
    def annotations(self, file):
        return None

