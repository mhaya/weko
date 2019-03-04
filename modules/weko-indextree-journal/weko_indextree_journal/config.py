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

"""Configuration for weko-indextree-journal."""

"""Module of weko-indextree-journal."""

import copy

from invenio_records_rest.config import RECORDS_REST_ENDPOINTS
from invenio_records_rest.facets import terms_filter
from invenio_search import RecordsSearch


WEKO_BUCKET_QUOTA_SIZE = 50 * 1024 * 1024 * 1024  # 50 GB
"""Maximum quota per bucket."""

WEKO_MAX_FILE_SIZE = WEKO_BUCKET_QUOTA_SIZE
WEKO_MAX_FILE_SIZE_FOR_ES = 1 * 1024 * 1024  # 1MB
"""Maximum file size accepted."""

WEKO_MIMETYPE_WHITELIST_FOR_ES = [
    'text/plain',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/pdf',
]

WEKO_INDEXTREE_JOURNAL_BASE_TEMPLATE = 'weko_indextree_journal/base.html'
"""Default base template for the indextree journal page."""

WEKO_INDEXTREE_JOURNAL_INDEX_TEMPLATE = 'weko_indextree_journal/index.html'
"""Index template for the indextree journal page."""

WEKO_INDEXTREE_JOURNAL_CONTENT_TEMPLATE = 'weko_indextree_journal/journal.html'
"""Index template for the indextree journal page."""

WEKO_INDEXTREE_JOURNAL_API = "/api/indextree/journal"

WEKO_INDEXTREE_JOURNAL_LIST_API = "/api/journal"

_IID = 'iid(tid,record_class="weko_indextree_journal.api:Journals")'

WEKO_INDEXTREE_JOURNAL_REST_ENDPOINTS = dict(
    tid=dict(
        pid_type='tid',
        record_class='weko_indextree_journal.api:Journals',
        indextree_journal_route='/indextree/journal/<int:journal_id>',
        journal_route='/indextree/journal',
        # item_tree_journal_route='/tree/journal/<int:pid_value>',
        # journal_move_route='/tree/journal/move/<int:index_id>',
        default_media_type='application/json',
        create_permission_factory_imp=
        'weko_indextree_journal.permissions:indextree_journal_permission',
        read_permission_factory_imp=
        'weko_indextree_journal.permissions:indextree_journal_permission',
        update_permission_factory_imp=
        'weko_indextree_journal.permissions:indextree_journal_permission',
        delete_permission_factory_imp=
        'weko_indextree_journal.permissions:indextree_journal_permission',
    )
)

WEKO_INDEXTREE_JOURNAL_UPDATED = True
"""For index tree cache."""

RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY = None
RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY = None
RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY = None
