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
import os

from flask_babelex import gettext as _
from invenio_records_rest.utils import allow_all

from .views import blueprint

WEKO_RECORDS_UI_DETAIL_TEMPLATE = 'weko_records_ui/detail.html'
WEKO_RECORDS_UI_BASE_TEMPLATE = 'weko_theme/page.html'

WEKO_PERMISSION_REQUIRED_TEMPLATE = 'weko_workflow/permission_required.html'

WEKO_PERMISSION_ROLE_USER = ('System Administrator',
                             'Repository Administrator',
                             'Community Administrator',
                             'Contributor',
                             'General')

WEKO_PERMISSION_SUPER_ROLE_USER = ('System Administrator',
                                   'Repository Administrator',
                                   'Community Administrator')

WEKO_RECORDS_UI_BULK_UPDATE_FIELDS = {
    'fields': [{'id': '1', 'name': 'Access Type'},
               {'id': '2', 'name': 'Licence'}],

    'licences': [{'id': 'license_free', 'name': _('write your own license')},
                 {'id': 'license_0', 'name': _(
                     'Creative Commons : Attribution')},
                 {'id': 'license_1', 'name': _(
                     'Creative Commons : Attribution - ShareAlike')},
                 {'id': 'license_2', 'name': _(
                     'Creative Commons : Attribution - NoDerivatives')},
                 {'id': 'license_3', 'name': _(
                     'Creative Commons : Attribution - NonCommercial')},
                 {'id': 'license_4', 'name': _(
                     'Creative Commons : Attribution - NonCommercial - ShareAlike')},
                 {'id': 'license_5', 'name': _('Creative Commons : Attribution - NonCommercial - NoDerivatives')}]
}

ADMIN_SET_ITEM_TEMPLATE = 'weko_records_ui/admin/item_setting.html'
# author setting page template


WEKO_ADMIN_PDFCOVERPAGE_TEMPLATE = 'weko_records_ui/admin/pdfcoverpage.html'
# pdfcoverpage templates

INSTITUTION_NAME_SETTING_TEMPLATE = 'weko_records_ui/admin/institution_name_setting.html'
# institution name setting page template

WEKO_PIDSTORE_IDENTIFIER_TEMPLATE_CREATOR = 'weko_records_ui/admin/pidstore_identifier_creator.html'
# pidstore identifier creator template

WEKO_PIDSTORE_IDENTIFIER_TEMPLATE_EDITOR = 'weko_records_ui/admin/pidstore_identifier_editor.html'
# pidstore identifier editor template

ITEM_SEARCH_FLG = 'name'
# setting author name search type: name or id

EMAIL_DISPLAY_FLG = True
# setting the email of author if display

# CSL Citation Formatter
# ======================
#: Styles Endpoint for CSL
CSL_STYLES_API_ENDPOINT = '/api/csl/styles'

#: Records Endpoint for CSL
CSL_RECORDS_API_ENDPOINT = '/api/record/cites/'

#: Template dirrectory for CSL
CSL_JSTEMPLATE_DIR = 'node_modules/invenio-csl-js/dist/templates/'

#: Template for CSL citation result
CSL_JSTEMPLATE_CITEPROC = 'template/weko_records_ui/invenio_csl/citeproc.html'

#: Template for CSL citation list item
CSL_JSTEMPLATE_LIST_ITEM = 'template/weko_records_ui/invenio_csl/item.html'

#: Template for CSL error
CSL_JSTEMPLATE_ERROR = os.path.join(CSL_JSTEMPLATE_DIR, 'error.html')

#: Template for CSL loading
CSL_JSTEMPLATE_LOADING = os.path.join(CSL_JSTEMPLATE_DIR, 'loading.html')

#: Template for CSL typeahead
CSL_JSTEMPLATE_TYPEAHEAD = os.path.join(CSL_JSTEMPLATE_DIR, 'typeahead.html')

RECORDS_UI_ENDPOINTS = dict(
    recid=dict(
        pid_type='recid',
        route='/records/<pid_value>',
        view_imp='weko_records_ui.views.default_view_method',
        template='weko_records_ui/detail.html',
        record_class='weko_deposit.api:WekoRecord',
        permission_factory_imp='weko_records_ui.permissions'
                               ':page_permission_factory',
        # read_permission_factory_imp=allow_all,
        # record_serializers={
        #     'text/x-bibliography': ('weko_records.serializers',
        #         ':citeproc_v1_response'),
        # }
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
    recid_file_details=dict(
        pid_type='recid',
        route='/records/<pid_value>/file_details/<path:filename>',
        view_imp='weko_records_ui.views.default_view_method',
        template='weko_records_ui/file_details.html',
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

WEKO_RECORDS_UI_CITES_REST_ENDPOINTS = {
    'depid': {
        'pid_type': 'depid',
        'pid_minter': 'deposit',
        'pid_fetcher': 'deposit',
        'record_class': 'weko_deposit.api:WekoRecord',
        'record_serializers': {
            'text/x-bibliography': ('weko_records.serializers',
                                    ':citeproc_v1_response'),
        },
        'cites_route': '/record/cites/<int:pid_value>',
        'default_media_type': 'application/json',
        'max_result_window': 10000,
    },
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

PDF_COVERPAGE_LANG_FILEPATH = blueprint.root_path + "/translations/"

PDF_COVERPAGE_LANG_FILENAME = "/pdf_coverpage.json"
