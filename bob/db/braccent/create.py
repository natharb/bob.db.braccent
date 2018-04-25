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

    # TODO: POPULATE THE DB HERE

    s.commit()
    s.close()


def add_command(subparsers):
    """Add specific subcommands that the action "create" can use"""

    parser = subparsers.add_parser('create', help=create.__doc__)

    parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
    parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?')
    parser.add_argument('-f', '--files-dir', default='.', help="Directory of the files (defaults to %(default)s)")

    parser.set_defaults(func=create)  # action


def create_braccent_file(session, args):
    filenames = os.listdir(args.files_dir)
    i = 0;
    for filename in filenames:

        if "Amazonas".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Roraima".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Amapa".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Belem".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Para".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Acre".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Rondonia".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Tocantins".upper() in filename.upper():
            sotaque = 'nortista'
        elif "MatoGrosso".upper() in filename.upper():
            sotaque = 'nortista'
        elif "Bahia".upper() and "Salvador" in filename.upper():
            sotaque = 'baiano'
        elif "Sergipe".upper() in filename.upper():
            sotaque = 'baiano'
        elif "MinasGerais".upper() and "MontesClaros".upper() in filename.upper():
            sotaque = 'baiano'
        elif "MinasGerais".upper() and "SaoFrancisco".upper() in filename.upper():
            sotaque = 'baiano'
        elif "Mineiro".upper() in filename.upper():
            sotaque = 'mineiro'
        elif "EspiritoSanto".upper() in filename.upper():
            sotaque = 'fluminense'
        elif "EspiritoSanto".upper() and "camposdosgoytacazes".upper() in filename.upper():
            sotaque = 'fluminense'
        elif "EspiritoSanto".upper() and "ubatuba".upper() in filename.upper():
            sotaque = 'fluminense'
        elif "RioJaneiro".upper() in filename.upper():
            sotaque = 'carioca'
        elif "Bahia".upper() and "pauloafonso" in filename.upper():
            sotaque = 'nordestino'
        elif "Pernambuco".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "Piaui".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "Ceara".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "RioGrandeDoNorte".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "Paraiba".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "Alagoas".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "Maranhao".upper() in filename.upper():
            sotaque = 'nordestino'
        elif "SaoPaulo".upper() in filename.upper():
            sotaque = 'sulista'
        elif "Parana".upper() in filename.upper():
            sotaque = 'sulista'
        elif "SantaCatarina".upper() in filename.upper():
            sotaque = 'sulista'
        elif "PortoAlegre".upper() in filename.upper():
            sotaque = 'sulista'
        elif "RioGrandeDoSul".upper() in filename.upper():
            sotaque = 'sulista'
        elif "MatoGrossoDoSul".upper() in filename.upper():
            sotaque = 'sulista'

        f = bob.db.braccent.File(i, filename, sotaque)
        i = i + 1;
        session.add(f)

