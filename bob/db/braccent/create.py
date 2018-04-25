#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nathália Alves Rocha Batista

"""
This script creates the BRACCENT database in a single pass.
"""

import os

from .models import *
import numpy
import os
numpy.random.seed(10)



def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2));
  File.metadata.create_all(engine)
  

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))

  #TODO: POPULATE THE DB HERE

  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?')
  parser.add_argument('-f', '--files-dir', default='.',  help="Directory of the files (defaults to %(default)s)")

  parser.set_defaults(func=create) #action

def create_braccent_file(session,args):
   filenames = os.listdir(args.files_dir)
   i = 0;
   for filename in filenames:
        if "Amazonas".upper() in filename.upper(): sotaque = 'nortista'
		else if "Roraima".upper() in filename.upper(): sotaque = 'nortista'
		else if "Amapa".upper() in filename.upper(): sotaque = 'nortista'
		else if "Belem".upper() in filename.upper(): sotaque = 'nortista'
		else if "Para".upper() in filename.upper(): sotaque = 'nortista'
		else if "Acre".upper() in filename.upper(): sotaque = 'nortista'
		else if "Rondonia".upper() in filename.upper(): sotaque = 'nortista'
		else if "Tocantins".upper() in filename.upper(): sotaque = 'nortista'
		else if "MatoGrosso".upper() in filename.upper(): sotaque = 'nortista'
		else if "Bahia".upper() and "Salvador" in filename.upper(): sotaque = 'baiano'
		else if "Sergipe".upper() in filename.upper(): sotaque = 'baiano'
		else if "MinasGerais".upper() and "MontesClaros".upper() in filename.upper(): sotaque = 'baiano'
		else if "MinasGerais".upper() and "SaoFrancisco".upper() in filename.upper(): sotaque = 'baiano'
	    else if "Mineiro".upper() in filename.upper(): sotaque = 'mineiro'
		else if "EspiritoSanto".upper() in filename.upper(): sotaque = 'fluminense'
	    else if "EspiritoSanto".upper() and "camposdosgoytacazes".upper() in filename.upper(): sotaque = 'fluminense'
		else if "EspiritoSanto".upper() and "ubatuba".upper() in filename.upper(): sotaque = 'fluminense'
        else if "RioJaneiro".upper() in filename.upper(): sotaque = 'carioca'
		else if "Bahia".upper() and "pauloafonso" in filename.upper(): sotaque = 'nordestino'
        else if "Pernambuco".upper() in filename.upper(): sotaque = 'nordestino' 
        else if "Piaui".upper() in filename.upper(): sotaque = 'nordestino'
        else if "Ceara".upper() in filename.upper(): sotaque = 'nordestino'
		else if "RioGrandeDoNorte".upper() in filename.upper(): sotaque = 'nordestino'
	    else if "Paraiba".upper() in filename.upper(): sotaque = 'nordestino'
	    else if "Alagoas".upper() in filename.upper(): sotaque = 'nordestino'
		else if "Maranhao".upper() in filename.upper(): sotaque = 'nordestino'
		else if "SaoPaulo".upper() in filename.upper(): sotaque = 'sulista'
	    else if "Parana".upper() in filename.upper(): sotaque = 'sulista'
	    else if "SantaCatarina".upper() in filename.upper(): sotaque = 'sulista'
	    else if "PortoAlegre".upper() in filename.upper(): sotaque = 'sulista'
		else if "RioGrandeDoSul".upper() in filename.upper(): sotaque = 'sulista'
		else if "MatoGrossoDoSul".upper() in filename.upper(): sotaque = 'sulista'

			
        f = bob.db.braccent.File(i,filename,sotaque)
	i=i+1;
