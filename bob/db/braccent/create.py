#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nathália Alves Rocha Batista

"""
This script creates the BRACCENT database in a single pass.
"""

import os

import numpy
numpy.random.seed(10)

from .models import ACCENTS, SEX, File, Protocol_File_Association

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

    files = create_braccent_file(s,args)
    s.commit()
    
    braccent_sets_per_protocol = create_closedset_braccent_protocols(s,  files)
    
    s.commit()
    s.close()


def add_command(subparsers):
    """Add specific subcommands that the action "create" can use"""

    parser = subparsers.add_parser('create', help=create.__doc__)

    parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
    parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?', default=1)
    parser.add_argument('-f', '--files-dir', default='.', help="Directory of the files (defaults to %(default)s)")

    parser.set_defaults(func=create)  # action


def create_closedset_braccent_protocols(session, files):
    """
    Create the closedset braccent protocol

    10 folds will be created with the following format: closedset_braccent_fold[1-10]

    For each accent,
      - 40% of the files will be used in the set - world
      - 60% of the files will be used in the set - dev. For the dev set
         - 40% of the files will be used to train the accent
         - 60% of the files will be used to probe
    """
  
    # hard coding the percentages
    world_set = 0.4

    dev_set = 0.6
    dev_enroll = 0.4
    dev_probe = 0.6

    # For each fold
    sets_per_protocol = dict()
    for i in range(1,11):

        protocol = "closedset_braccent_fold{0}".format(i)
        sets_per_protocol[protocol] = []

        # for each accent
        for accent in ACCENTS:

            # defining the number of files per accent
            total_files_accent = len(files[accent])

            n_world = int(numpy.floor(total_files_accent * world_set))
            n_dev = int(numpy.ceil(total_files_accent * dev_set))
            n_dev_enroll = int(numpy.floor(n_dev * dev_enroll))
            #n_dev_probe = numpy.ceil(n_dev * dev_probe) # will keep this just for didactics

            # NOW let's filter the files
            accent_files = numpy.array(files[accent])

            # Shuffling
            numpy.random.shuffle(accent_files)

            # Selecting the data
            world_files = accent_files[0:n_world]
            dev_files = accent_files[n_world:]
            dev_enroll_files = dev_files[0:n_dev_enroll]
            dev_probe_files = dev_files[n_dev_enroll:]

            # Appending the files sets in case you want to use this in the future
            sets_per_protocol[protocol].append(world_files)
            sets_per_protocol[protocol].append(dev_enroll_files)
            sets_per_protocol[protocol].append(dev_probe_files)

            # Appending to the dataset
            for f in world_files:
                session.add(Protocol_File_Association(protocol, "world", "train", f.id))
               
            # Appending to the dataset
            for f in dev_enroll_files:
                session.add(Protocol_File_Association(protocol, "dev", "enroll", f.id))
     
            # Appending to the dataset
            for f in dev_probe_files:
                session.add(Protocol_File_Association(protocol, "dev", "probe", f.id))

    # Returning the selected list if you want to use them in the future
    return sets_per_protocol


def create_braccent_file(session, args):
    """
    Inserted braccent files into the database (table File)
    """

    # Keeping all files in a dict, so we can easilly organize the protocols
    files = dict()

    # Basepath is /xxx/Braccent/Mono
    base_path = args.files_dir
    braccent_path = os.path.join("BRAccent", "Mono")
    
    # primary key
    i = 0

    # For each accent /xxx/Braccent/Mono/ACCENT/
    for accent in ACCENTS:
     
        # For each sex /xxx/Braccent/Mono/ACCENT/SEX/
        for sex in SEX:

            # Now list dir
            braccent_full_dir = os.path.join(braccent_path, accent, sex)
            for f in os.listdir(os.path.join(base_path, braccent_full_dir)):
                i += 1 #auto increment
                file_name = os.path.splitext(os.path.join(braccent_full_dir, f))[0]
                file_object = File(i, file_name.rstrip("\n"), accent, sex)

                # Creating dict to store the files in memory
                if accent not in files:
                    files[accent] = []
                files[accent].append(file_object)
                session.add(file_object)                

    return files

