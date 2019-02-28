# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery weko index tree journal tasks."""

from __future__ import absolute_import, print_function
from celery import shared_task

from .proxies import current_stats

@shared_task
def export_data(data_types):
    """Index statistics events."""
    celery_schedule = current_celery.conf.get('CELERY_INDEXTREE_JOURNAL_SCHEDULE', {})
    print('_______________________CELERY_SCHEDULE____' , celery_schedule)
    print('_______________________Export_____________' , data_types)

    """
    results = []
    for e in data_types:
        processor = current_stats.events[e].processor_class(
            **current_stats.events[e].processor_config)
        results.append((e, processor.run()))
    return results
    """
