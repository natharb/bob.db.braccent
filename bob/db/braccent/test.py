#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Thu Oct 09 11:27:27 CEST 2014
#
# Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks on the protocols of a subset of the CUHK database
"""

import bob.db.braccent
import numpy

""" Defining protocols. Yes, they are static """
PROTOCOLS = ('closedset_braccent_fold1', 'closedset_braccent_fold2', 'closedset_braccent_fold3', 'closedset_braccent_fold4', 'closedset_braccent_fold5', 'closedset_braccent_fold6', 'closedset_braccent_fold7', 'closedset_braccent_fold8', 'closedset_braccent_fold9', 'closedset_braccent_fold10')


GROUPS    = ('world', 'dev')

PURPOSES   = ('train', 'enroll', 'probe')


def test01_protocols_purposes_groups():
  
  #testing protocols
  possible_protocols = bob.db.braccent.Database().protocols()
  for p in possible_protocols:
    assert p  in PROTOCOLS

  #testing purposes
  possible_purposes = bob.db.braccent.Database().purposes()
  for p in possible_purposes:
    assert p  in PURPOSES

  #testing GROUPS
  possible_groups = bob.db.braccent.Database().groups()
  for p in possible_groups:
    assert p  in GROUPS


def test02_closed_set_braccent():

    world      = 547
    dev        = 828
    total_data = world + dev # =1375
  
    dev_enroll = 328
    dev_probe  = 500

    # Testing dev-enroll for ALL classes
    dev_enroll_nortista = 6
    dev_enroll_baiano = 28
    dev_enroll_fluminense = 10
    dev_enroll_mineiro = 26
    dev_enroll_carioca = 15
    dev_enroll_nordestino = 48
    dev_enroll_sulista = 195
 
    protocols = bob.db.braccent.Database().protocols()
    for p in protocols:
  
        if "closedset_braccent" in p:  

            # Checking overall stats
            assert len(bob.db.braccent.Database().objects(protocol=p)) == total_data
    
            assert len(bob.db.braccent.Database().objects(protocol=p, groups="world")) == world

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev")) == dev
            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll")) == dev_enroll
            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="probe"))  == dev_probe
            # Checking all classes
            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Nortista",])) == dev_enroll_nortista

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Baiano",])) == dev_enroll_baiano

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Fluminense",])) == dev_enroll_fluminense

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Mineiro",])) == dev_enroll_mineiro

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Carioca",])) == dev_enroll_carioca

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Nordestino",])) == dev_enroll_nordestino

            assert len(bob.db.braccent.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=["Sulista",])) == dev_enroll_sulista
