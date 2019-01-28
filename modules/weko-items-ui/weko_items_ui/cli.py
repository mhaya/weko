# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WEKO3; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.

"""WEKO3 module docstring."""

import click
import datetime
import uuid
from flask.cli import with_appcontext
from sqlalchemy import asc
from invenio_db import db
from flask import request
import urllib.request
import xml.etree.cElementTree as ET


@click.group()
def abcd():
    """
    Get SHERPA/ReMOO data !!
    :return:
    """


@abcd.command('init')
@with_appcontext
def init_item_metadata_reference():
    """
    Init table item_metadata_reference.
    :return:
    """

    # def get_reference_data():
    #     url = 'http://www.baidu.com/'
    #     response = urllib2.urlopen(url)  ##urlopen接受传入参数是string或者是request
    #     response_text = response.read()

    # url = 'http://www.sherpa.ac.uk/romeo/api29.php?all=yes'
    url = 'http://www.sherpa.ac.uk/romeo/api29.php?jtitle=modern&qtype=contains'
    response = urllib.request.urlopen(url)
    response_text = response.read()
    str_text = ET.fromstring(response_text)
    click.secho(str_text, fg='green')
    click.secho('Just do test!!!!!', fg='red')
