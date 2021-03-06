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

"""Views for weko-admin."""

import json
import math
import sys
from datetime import timedelta

from flask import Blueprint, abort, current_app, flash, jsonify, \
    make_response, render_template, request
from flask_babelex import lazy_gettext as _
from flask_breadcrumbs import register_breadcrumb
from flask_login import current_user, login_required
from flask_menu import register_menu
from invenio_admin.proxies import current_admin
from sqlalchemy.orm import session
from weko_records.api import ItemTypes
from werkzeug.local import LocalProxy

from .models import SearchManagement, SessionLifetime
from .utils import get_admin_lang_setting, get_api_certification_type, \
    get_current_api_certification, get_initial_stats_report, \
    get_selected_language, get_unit_stats_report, save_api_certification, \
    update_admin_lang_setting, validate_certification

_app = LocalProxy(lambda: current_app.extensions['weko-admin'].app)


blueprint = Blueprint(
    'weko_admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/accounts/settings',
)

blueprint_api = Blueprint(
    'weko_admin',
    __name__,
    url_prefix='/admin',
    template_folder='templates',
    static_folder='static',
)


def _has_admin_access():
    """Use to check if a user has any admin access."""
    return current_user.is_authenticated and current_admin \
        .permission_factory(current_admin.admin.index_view).can()


@blueprint.route('/session/lifetime/<int:minutes>', methods=['GET'])
def set_lifetime(minutes):
    """Update session lifetime in db.

    :param minutes:
    :return: Session lifetime updated message.
    """
    try:
        db_lifetime = SessionLifetime.get_validtime()
        if db_lifetime is None:
            db_lifetime = SessionLifetime(lifetime=minutes)
        else:
            db_lifetime.lifetime = minutes
        db_lifetime.create()
        _app.permanent_session_lifetime = timedelta(
            minutes=db_lifetime.lifetime)
        return jsonify(code=0, msg='Session lifetime was updated.')
    except BaseException:
        current_app.logger.error('Unexpected error: ', sys.exc_info()[0])
        return abort(400)


@blueprint.route('/session', methods=['GET', 'POST'])
@blueprint.route('/session/', methods=['GET', 'POST'])
@register_menu(
    blueprint, 'settings.lifetime',
    _('%(icon)s Session', icon='<i class="fa fa-cogs fa-fw"></i>'),
    visible_when=_has_admin_access,
    order=14
)
@register_breadcrumb(
    blueprint, 'breadcrumbs.settings.session',
    _('Session')
)
@login_required
def lifetime():
    """Loading session setting page.

    :return: Lifetime in minutes.
    """
    if not _has_admin_access():
        return abort(403)
    try:
        db_lifetime = SessionLifetime.get_validtime()
        if db_lifetime is None:
            db_lifetime = SessionLifetime(lifetime=30)

        if request.method == 'POST':
            # Process forms
            form = request.form.get('submit', None)
            if form == 'lifetime':
                new_lifetime = request.form.get('lifetimeRadios', '30')
                db_lifetime.lifetime = int(new_lifetime)
                db_lifetime.create()
                _app.permanent_session_lifetime = timedelta(
                    minutes=db_lifetime.lifetime)
                flash(_('Session lifetime was updated.'), category='success')

        return render_template(
            current_app.config['WEKO_ADMIN_LIFETIME_TEMPLATE'],
            current_lifetime=str(db_lifetime.lifetime),
            map_lifetime=[('15', _('15 mins')),
                          ('30', _('30 mins')),
                          ('45', _('45 mins')),
                          ('60', _('60 mins')),
                          ('180', _('180 mins')),
                          ('360', _('360 mins')),
                          ('720', _('720 mins')),
                          ('1440', _('1440 mins'))]
        )
    except ValueError as valueErr:
        current_app.logger.error(
            'Could not convert data to an integer: {0}'.format(valueErr))
    except BaseException:
        current_app.logger.error('Unexpected error: ', sys.exc_info()[0])
        return abort(400)


@blueprint.route('/session/offline/info', methods=['GET'])
def session_info_offline():
    """Get session lifetime from app setting.

    :return: Session information offline in json.
    """
    current_app.logger.info('request session_info by offline')
    session_id = session.sid_s if hasattr(session, 'sid_s') else 'None'
    lifetime_str = str(current_app.config['PERMANENT_SESSION_LIFETIME'])
    return jsonify(user_id=current_user.get_id(),
                   session_id=session_id,
                   lifetime=lifetime_str,
                   _app_lifetime=str(_app.permanent_session_lifetime),
                   current_app_name=current_app.name)


@blueprint_api.route('/load_lang', methods=['GET'])
def get_lang_list():
    """Get Language List."""
    results = dict()
    try:
        results['results'] = get_admin_lang_setting()
        results['msg'] = 'success'
    except Exception as e:
        results['msg'] = str(e)

    return jsonify(results)


@blueprint_api.route('/save_lang', methods=['POST'])
def save_lang_list():
    """Save Language List."""
    if request.headers['Content-Type'] != 'application/json':
        current_app.logger.debug(request.headers['Content-Type'])
        return jsonify(msg='Header Error')
    data = request.get_json()
    result = update_admin_lang_setting(data)

    return jsonify(msg=result)


@blueprint_api.route('/get_selected_lang', methods=['GET'])
def get_selected_lang():
    """Get selected language."""
    try:
        result = get_selected_language()
    except Exception as e:
        result = {'error': str(e)}
    return jsonify(result)


@blueprint_api.route('/get_api_cert_type', methods=['GET'])
def get_api_cert_type():
    """Get list of supported API, to display on the combobox on UI.

    :return: Example
    {
        'result':[
        {
            'api_code': 'DOI',
            'api_name': 'CrossRef API'
        },
        {
            'api_code': 'AMA',
            'api_name': 'Amazon'
        }],
        'error':''
    }
    """
    result = {
        'results': '',
        'error': ''
    }
    try:
        result['results'] = get_api_certification_type()
    except Exception as e:
        result['error'] = str(e)
    return jsonify(result)


@blueprint_api.route('/get_curr_api_cert/<string:api_code>', methods=['GET'])
def get_curr_api_cert(api_code=''):
    """Get current API certification data, to display on textbox on UI.

    :param api_code: API code
    :return:
    {
        'results':
        {
            'api_code': 'DOI',
            'api_name': 'CrossRef API',
            'cert_data':
            {
                'account': 'abc@xyz.com'
            }
        },
        'error':''
    }
    """
    result = {
        'results': '',
        'error': ''
    }
    try:
        result['results'] = get_current_api_certification(api_code)
    except Exception as e:
        result['error'] = str(e)
    return jsonify(result)


@blueprint_api.route('/save_api_cert_data', methods=['POST'])
def save_api_cert_data():
    """Save api certification data to database.

    :return: Example
    {
        'results': true // true if save successfully
        'error':''
    }
    """
    result = dict()

    if request.headers['Content-Type'] != 'application/json':
        result['error'] = _('Header Error')
        return jsonify(result)

    data = request.get_json()
    api_code = data.get('api_code', '')
    cert_data = data.get('cert_data', '')
    if not cert_data:
        result['error'] = _(
            'Account information is invalid. Please check again.')
    elif validate_certification(cert_data):
        result = save_api_certification(api_code, cert_data)
    else:
        result['error'] = _(
            'Account information is invalid. Please check again.')

    return jsonify(result)


@blueprint_api.route('/get_init_selection/<string:selection>', methods=['GET'])
def get_init_selection(selection=""):
    """Get initial data for unit and target.

    :param selection:
    """
    result = dict()
    try:
        if selection == 'target':
            result = get_initial_stats_report()
        elif selection == "":
            raise ValueError("Request URL is incorrectly")
        else:
            result = get_unit_stats_report(selection)
    except Exception as e:
        result['error'] = str(e)

    return jsonify(result)


@blueprint_api.route('/get_statistic_item_regis/<int:unit>/<int:page>',
                     methods=['GET'])
def get_statistic_item_regis(unit=1, page=1):
    """Get statistic item regis."""
    response_data = {
        'data': '',
        'num_page': 1,
        'page': 1
    }
    result = list()
    for i in range(1, 30):
        temp_data = dict()
        if unit == 1:
            temp_data['col1'] = "2019-04-" + str(i)
            temp_data['col2'] = i + 50
        elif unit == 2:
            temp_data['col1'] = "2019-01-01 - 2019-04-" + str(i)
            temp_data['col2'] = i + 50
        elif unit == 3:
            temp_data['col1'] = "20" + str(i).zfill(2)
            temp_data['col2'] = i + 50
        else:
            temp_data['col1'] = "User " + str(i)
            temp_data['col2'] = "192.168.1." + str(i)
            temp_data['col3'] = i + 50
        result.append(temp_data)
    page_result = list()
    i = 0
    temp_page_data = list()
    while i < len(result):
        if i % 10 == 0 or i == (len(result) - 1):
            page_result.append(temp_page_data)
            temp_page_data = list()
            temp_page_data.append(result[i])
        else:
            temp_page_data.append(result[i])
        i = i + 1

    print("----------====================------------")
    print(page - 1)
    print(page_result)
    response_data['data'] = page_result[page]
    response_data['num_page'] = math.ceil(len(result) / 10)
    response_data['page'] = page
    return jsonify(response_data)


@blueprint_api.route('/get_statistic_detail_view/<int:unit>/<int:page>',
                     methods=['GET'])
def get_statistic_detail_view(unit=1, page=1):
    """Get statistic detail view."""
    response_data = {
        'data': '',
        'num_page': 1,
        'page': 1
    }
    result = list()
    for i in range(1, 30):
        temp_data = dict()
        if unit == 1:
            temp_data['col1'] = "2019-05-" + str(i)
            temp_data['col2'] = i + 100
        elif unit == 2:
            temp_data['col1'] = "2019-01-01 - 2019-04-" + str(i)
            temp_data['col2'] = i + 100
        elif unit == 3:
            temp_data['col1'] = "20" + str(i).zfill(2)
            temp_data['col2'] = i + 100
        elif unit == 4:
            temp_data['col1'] = "100" + str(i)
            temp_data['col2'] = "Test Item " + str(i)
            temp_data['col3'] = i + 100
        else:
            temp_data['col1'] = "User " + str(i)
            temp_data['col2'] = "192.168.1." + str(i)
            temp_data['col3'] = i + 100
        result.append(temp_data)

    page_result = list()
    i = 0
    temp_page_data = list()
    while i < len(result):
        if i % 10 == 0 or i == (len(result) - 1):
            page_result.append(temp_page_data)
            temp_page_data = list()
            temp_page_data.append(result[i])
        else:
            temp_page_data.append(result[i])
        i = i + 1

    response_data['data'] = page_result[page]
    response_data['num_page'] = math.ceil(len(result) / 10)
    response_data['page'] = page
    return jsonify(response_data)
