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

"""Weko Indextree Journal celery tasks."""

from celery import shared_task
from celery import current_app as current_celery
from datetime import date, datetime, timedelta
from celery.utils.log import get_task_logger
from invenio_records.models import RecordMetadata
from invenio_db import db
from .api import WekoDeposit
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from elasticsearch.exceptions import TransportError
from __future__ import absolute_import, print_function
import math
import uuid

from celery.states import state
from .models import FileInstance, Location, MultipartObject, ObjectVersion
from .utils import obj_or_import_string

logger = get_task_logger(__name__)

@shared_task(ignore_result=True)
def export_data(frequency=None, batch_interval=None,
                files_query=None
                ):
    """Schedule a batch of files for checksum verification.

    The purpose of this task is to be periodically called through `celerybeat`,
    in order achieve a repeated verification cycle of all file checksums, while
    following a set of constraints in order to throttle the execution rate of
    the checks.

    :param dict frequency: Time period over which a full check of all files
        should be performed. The argument is a dictionary that will be passed
        as arguments to the `datetime.timedelta` class. Defaults to a month (30
        days).
    :param dict batch_interval: How often a batch is sent. If not supplied,
        this information will be extracted, if possible, from the
        celery.conf['CELERY_BEAT_SCHEDULE'] entry of this task. The argument is
        a dictionary that will be passed as arguments to the
        `datetime.timedelta` class.
    :param str files_query: Import path for a function returning a
        FileInstance query for files that should be checked.

    """
    current_app.logger.debug('Task is running.')
    print("Hello World!!! Bao Phung is here")
    frequency = timedelta(**frequency) if frequency else timedelta(days=30)
    if batch_interval:
        batch_interval = timedelta(**batch_interval)
    else:
        celery_schedule = current_celery.conf.get('CELERY_BEAT_SCHEDULE', {})
        batch_interval = batch_interval or next(
            (v['schedule'] for v in celery_schedule.values()
             if v.get('task') == schedule_checksum_verification.name), None)
    if not batch_interval or not isinstance(batch_interval, timedelta):
        raise Exception(u'No "batch_interval" could be decided')

    total_batches = int(
        frequency.total_seconds() / batch_interval.total_seconds())

    files = obj_or_import_string(
        files_query, default=default_checksum_verification_files_query)()
    files = files.order_by(sa.func.coalesce(FileInstance.last_check_at, date.min))
