#
# This file is part of WEKO3.
# Copyright (C) 2019 National Institute of Informatics.
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

"""Weko Indextree-journal celery tasks."""

from celery import shared_task
from celery.utils.log import get_task_logger
from invenio_records.models import RecordMetadata
from invenio_db import db
from .api import WekoDeposit
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from elasticsearch.exceptions import TransportError

logger = get_task_logger(__name__)

#@shared_task(ignore_result=True)
#@shared_task(base=RequestContextTask)
@shared_task
def export_data():
    INDEXTREE_JOURNAL_SCHEDULE = celery_schedule = current_app.conf.get('CELERY_INDEXTREE_JOURNAL_SCHEDULE', {})
    print("-------------------------------------Hello INDEXTREE_JOURNAL!!!-------------------------------------")
