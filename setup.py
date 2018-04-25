#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Thu Apr 16 16:39:01 CEST 2015
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

from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()


from bob.extension.utils import load_requirements
install_requires = load_requirements()

setup(

    name='bob.db.braccent',
    version=version,
    description='Brazilian Accent Database (Braccent)',
    url='https://gitlab.idiap.ch/bob/bob.db.braccent',
    license='BSD',
    keywords = "",
    author='Nathalia Batista',
    author_email='',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,

    install_requires=install_requires,

    namespace_packages = [
      'bob',
      'bob.db',
    ],

    entry_points = {      
       # bob database declaration
       'bob.db': [
         'braccent = bob.db.braccent.driver:Interface',
       ],

    },

    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Education',
      'License :: OSI Approved :: BSD License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
    ],
)
