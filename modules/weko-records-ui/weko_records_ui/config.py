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

"""Configuration for weko-records-ui."""
# from __future__ import absolute_import, print_function, unicode_literals

import os
from datetime import timedelta

from celery.schedules import crontab

from .views import blueprint

WEKO_RECORDS_UI_DETAIL_TEMPLATE = 'weko_records_ui/detail.html'
WEKO_RECORDS_UI_BASE_TEMPLATE = 'weko_theme/page.html'

WEKO_PERMISSION_ROLE_USER = ('System Administrator',
                             'Repository Administrator',
                             'Contributor',
                             'General')


WEKO_PERMISSION_SUPER_ROLE_USER = ('System Administrator',
                                   'Repository Administrator')

ADMIN_SET_ITEM_TEMPLATE = 'weko_records_ui/admin/item_setting.html'
# author setting page template


WEKO_ADMIN_PDFCOVERPAGE_TEMPLATE = 'weko_records_ui/admin/pdfcoverpage.html'
# pdfcoverpage templates

INSTITUTION_NAME_SETTING_TEMPLATE = 'weko_records_ui/admin/institution_name_setting.html'
# institution name setting page template

ITEM_SEARCH_FLG = 'name'
# setting author name search type: name or id

EMAIL_DISPLAY_FLG = True
# setting the email of author if display

RECORDS_UI_ENDPOINTS = dict(
    recid=dict(
        pid_type='recid',
        route='/records/<pid_value>',
        view_imp='weko_records_ui.views.default_view_method',
        template='weko_records_ui/detail.html',
        record_class='weko_deposit.api:WekoRecord',
        permission_factory_imp='weko_records_ui.permissions'
                               ':page_permission_factory',
    ),
    recid_export=dict(
        pid_type='recid',
        route='/records/<pid_value>/export/<format>',
        view_imp='weko_records_ui.views.export',
        template='weko_records_ui/export.html',
        record_class='weko_deposit.api:WekoRecord',
    ),
    recid_files=dict(
        pid_type='recid',
        route='/record/<pid_value>/files/<path:filename>',
        view_imp='weko_records_ui.fd.file_download_ui',
        record_class='weko_deposit.api:WekoRecord',
        permission_factory_imp='weko_records_ui.permissions'
                               ':page_permission_factory',
    ),
    recid_file_preview=dict(
        pid_type='recid',
        route='/record/<pid_value>/file_preview/<path:filename>',
        view_imp='weko_records_ui.fd.file_preview_ui',
        record_class='weko_deposit.api:WekoRecord',
        permission_factory_imp='weko_records_ui.permissions'
                               ':page_permission_factory',
    ),
    recid_preview=dict(
        pid_type='recid',
        route='/record/<pid_value>/preview/<path:filename>',
        view_imp='weko_records_ui.preview.preview',
        record_class='weko_deposit.api:WekoRecord',
        permission_factory_imp='weko_records_ui.permissions'
                               ':page_permission_factory',
    ),
    recid_publish=dict(
        pid_type='recid',
        route='/record/<pid_value>/publish',
        view_imp='weko_records_ui.views.publish',
        template='weko_records_ui/detail.html',
        record_class='weko_deposit.api:WekoRecord',
        permission_factory_imp='weko_items_ui.permissions'
                               ':edit_permission_factory',
        methods=['POST'],
    ),
)

RECORDS_UI_EXPORT_FORMATS = {
    'recid': {
        'junii2': dict(
            title='junii2',
            serializer='weko_schema_ui.serializers.WekoCommonSchema',
            order=1,
        ),
        'jpcoar': dict(
            title='JPCOAR',
            serializer='weko_schema_ui.serializers.WekoCommonSchema',
            order=2,
        ),
        'oai_dc': dict(
            title='DublinCore',
            serializer='weko_schema_ui.serializers.WekoCommonSchema',
            order=3,
        ),
        'json': dict(
            title='JSON',
            serializer='invenio_records_rest.serializers.json_v1',
            order=4,
        ),
        'bibtex': dict(
            title='BIBTEX',
            serializer='weko_schema_ui.serializers.BibTexSerializer',
            order=5,
        ),
    }
}

OAISERVER_METADATA_FORMATS = {
    'junii2': {
        'serializer': (
            'weko_schema_ui.utils:dumps_oai_etree', {
                'schema_type': 'junii2',
            }
        ),
        'schema': 'http://irdb.nii.ac.jp/oai/junii2-3-1.xsd',
        'namespace': 'http://irdb.nii.ac.jp/oai',
    },
    'jpcoar': {
        'serializer': (
            'weko_schema_ui.utils:dumps_oai_etree', {
                'schema_type': 'jpcoar',
            }
        ),
        'namespace': 'https://irdb.nii.ac.jp/schema/jpcoar/1.0/',
        'schema': 'https://irdb.nii.ac.jp/schema/jpcoar/1.0/jpcoar_scm.xsd',
    },
    'oai_dc': {
        'serializer': (
            'weko_schema_ui.utils:dumps_oai_etree', {
                'schema_type': 'oai_dc',
            }
        ),
        'namespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
    }
}

URL_OA_POLICY_HEIGHT = 7  # height of the URL & OA-policy
# title_h = 8  # height of the title
TITLE_HEIGHT = 8  # height of the title
# header_h = 20  # height of the header cell
HEADER_HEIGHT = 20  # height of the header cell
# footer_h = 4  # height of the footer cell
FOOTER_HEIGHT = 4  # height of the footer cell
# meta_h = 9  # height of the metadata cell
METADATA_HEIGHT = 9

# Path to the JPAexg font file
JPAEXG_TTF_FILEPATH = blueprint.root_path + "/fonts/ipaexg00201/ipaexg.ttf"

# Path to the JPAexm font file
JPAEXM_TTF_FILEPATH = blueprint.root_path + "/fonts/ipaexm00201/ipaexm.ttf"


""" STATS """
STATS_EVENTS = {
    'file-download': {
        'signal': 'invenio_files_rest.signals.file_downloaded',
        'event_builders': [
            'invenio_stats.contrib.event_builders.file_download_event_builder'
        ]
    },
}

#: Enabled aggregations from 'zenoodo.modules.stats.registrations'
STATS_AGGREGATIONS = {
    'record-download-agg': {},
    'record-download-all-versions-agg': {},
    # NOTE: Since the "record-view-agg" aggregations is already registered in
    # "invenio_stasts.contrib.registrations", we have to overwrite the
    # configuration here
    'record-view-agg': dict(
        templates='zenodo.modules.stats.templates.aggregations',
        aggregator_config=dict(
            #client=current_stats_search_client,
            event='record-view',
            aggregation_field='recid',
            aggregation_interval='day',
            batch_size=1,
            copy_fields=dict(
                record_id='record_id',
                recid='recid',
                conceptrecid='conceptrecid',
                doi='doi',
                conceptdoi='conceptdoi',
                communities=lambda d, _: (list(d.communities)
                                          if d.communities else None),
                owners=lambda d, _: (list(d.owners) if d.owners else None),
                is_parent=lambda *_: False
            ),
            metric_aggregation_fields=dict(
                unique_count=('cardinality', 'unique_session_id',
                              {'precision_threshold': 1000}),
            )
        )
    ),
    'record-view-all-versions-agg': {},
}
#: Enabled queries from 'zenoodo.modules.stats.registrations'
STATS_QUERIES = {
    'record-view': {},
    'record-view-all-versions': {},
    'record-download': {},
    'record-download-all-versions': {},
}

# Queues
# ======
#QUEUES_BROKER_URL = CELERY_BROKER_URL

# Proxy configuration
#: Number of proxies in front of application.
WSGI_PROXIES = 0

#: Set the session cookie to be secure - should be set to true in production.
SESSION_COOKIE_SECURE = False

# Indexer
# =======
#: Provide a custom record_to_index function for invenio-indexer
INDEXER_RECORD_TO_INDEX = "zenodo.modules.indexer.utils.record_to_index"
INDEXER_SCHEMA_TO_INDEX_MAP = {
    'records-record-v1.0.0': 'record-v1.0.0',
    'licenses-license-v1.0.0': 'license-v1.0.0',
    'grants-grant-v1.0.0': 'grant-v1.0.0',
    'deposits-records-record-v1.0.0': 'deposit-record-v1.0.0',
    'funders-funder-v1.0.0': 'funder-v1.0.0',
}
