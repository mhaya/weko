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

"""Utilities for convert response json."""
import copy
import json

from flask import current_app, jsonify, make_response
from sqlalchemy import asc
from weko_admin.models import AdminLangSettings

from .api import WidgetItems, WidgetMultiLangData
from .models import WidgetDesignSetting, WidgetType


def get_widget_type_list():
    """Get all Widget types.

    :param: None
    :return: options json
    """
    widget_types = WidgetType.get_all_widget_types()
    options = []
    if isinstance(widget_types, list):
        for widget_type in widget_types:
            option = dict()
            option["text"] = widget_type.type_name
            option["value"] = widget_type.type_id
            options.append(option)
    result = {"options": options}

    return result


def delete_item_in_preview_widget_item(data_id, json_data):
    """Delete item in preview widget design.

    Arguments:
        data_id {widget_item} -- [id of widget item]
        json_data {dict} -- [data to be updated]

    Returns:
        [data] -- [data after updated]

    """
    remove_list = []
    if isinstance(json_data, list):
        for item in json_data:
            if str(item.get('name')) == str(data_id.get('label')) and str(
                    item.get('type')) == str(data_id.get('widget_type')):
                remove_list.append(item)
    for item in remove_list:
        json_data.remove(item)
    data = json.dumps(json_data)
    return data


def update_general_item(item, data_result):
    """Update general field item.

    :param item: item need to be update
    :param data_result: result
    """
    item['frame_border'] = data_result.get('frame_border')
    item['frame_border_color'] = data_result.get(
        'frame_border_color')
    item['background_color'] = data_result.get('background_color')
    item['label_color'] = data_result.get('label_color')
    item['text_color'] = data_result.get('text_color')
    item['name'] = data_result.get('label')
    item['type'] = data_result.get('widget_type')
    item['multiLangSetting'] = data_result.get('multiLangSetting')
    settings = data_result.get('settings')
    if str(data_result.get('widget_type')) == "Access counter":
        update_access_counter_item(item, settings)
    if str(data_result.get('widget_type')) == "New arrivals":
        update_new_arrivals_item(item, settings)


def update_access_counter_item(item, data_result):
    """Update widget item type Access Counter.

    Arguments:
        item {WidgetItem} -- Item need to be update
        data_result {dict} -- [data to update]
    """
    item['access_counter'] = data_result.get('access_counter')


def update_new_arrivals_item(item, data_result):
    """Update widget item type New Arrivals.

    Arguments:
        item {WidgetItem} -- Item need to be update
        data_result {dict} -- [data to update]
    """
    item['new_dates'] = data_result.get('new_dates')
    item['display_result'] = data_result.get('display_result')
    item['rss_feed'] = data_result.get('rss_feed')


def validate_admin_widget_item_setting(widget_id):
    """Validate widget item.

    :param: widget id
    :return: true if widget item is used in widget design else return false
    """
    try:
        if (type(widget_id)) is dict:
            repository_id = widget_id.get('repository')
            widget_item_id = widget_id.get('id')
        else:
            repository_id = widget_id.repository_id
            widget_item_id = widget_id.id
        data = WidgetDesignSetting.select_by_repository_id(
            repository_id)
        if data.get('settings'):
            json_data = json.loads(data.get('settings'))
            for item in json_data:
                if str(item.get('widget_id')) == str(widget_item_id):
                    return True
        return False
    except Exception as e:
        current_app.logger.error('Failed to validate record: ', e)
        return True


def get_default_language():
    """Get default Language.

    :return:
    """
    result = get_register_language()
    if isinstance(result, list):
        return result[0]
    return


def get_unregister_language():
    """Get unregister Language.

    :return:
    """
    result = AdminLangSettings.query.filter_by(is_registered=False)
    return AdminLangSettings.parse_result(result)


def get_register_language():
    """Get register language."""
    result = AdminLangSettings.query.filter_by(is_registered=True).order_by(
        asc('admin_lang_settings_sequence'))
    return AdminLangSettings.parse_result(result)


def get_system_language():
    """Get system language for widget setting.

    Returns:
        result -- dictionary contains language list

    """
    result = {
        'language': [],
        'error': ''
    }
    try:
        sys_lang = AdminLangSettings.load_lang()
        result['language'] = sys_lang
    except Exception as e:
        result['error'] = str(e)

    return result


def build_data(data):
    """Build data get from client to dictionary.

    Arguments:
        data {json} -- Client data

    Returns:
        dictionary -- server data

    """
    result = dict()
    result['repository_id'] = data.get('repository')
    result['widget_type'] = data.get('widget_type')
    result['settings'] = json.dumps(build_data_setting(data))
    result['is_enabled'] = data.get('enable')
    result['multiLangSetting'] = data.get('multiLangSetting')
    result['is_deleted'] = False
    role = data.get('browsing_role')
    if isinstance(role, list):
        result['browsing_role'] = ','.join(str(e) for e in role)
    else:
        result['browsing_role'] = role
    role = data.get('edit_role')
    if isinstance(role, list):
        result['edit_role'] = ','.join(str(e) for e in role)
    else:
        result['edit_role'] = role
    return result


def build_data_setting(data):
    """Build setting pack.

    Arguments:
        data {json} -- client data

    Returns:
        dictionary -- setting pack

    """
    result = dict()
    result['background_color'] = data.get('background_color')
    result['frame_border'] = data.get('frame_border')
    result['frame_border_color'] = data.get('frame_border_color')
    result['label_color'] = data.get('label_color')
    result['text_color'] = data.get('text_color')
    if str(data.get('widget_type')) == 'Access counter':
        result['access_counter'] = data['settings'] \
            .get('access_counter') or '0'
    if str(data.get('widget_type')) == 'New arrivals':
        result['new_dates'] = data['settings'].get('new_dates') or '5'
        result['display_result'] = data['settings'].get(
            'display_result') or '5'
        result['rss_feed'] = data['settings'].get('rss_feed') or False

    return result


def build_multi_lang_data(widget_id, multi_lang_json):
    """Build multiple language data.

    Arguments:
        widget_id {sequence} -- id of widget
        multi_lang_json {json} -- multiple language data as json

    Returns:
        dictionary -- multiple language data

    """
    if not multi_lang_json:
        return None

    result = list()
    for k, v in multi_lang_json.items():
        new_lang_data = dict()
        new_lang_data['widget_id'] = widget_id
        new_lang_data['lang_code'] = k
        new_lang_data['label'] = v.get('label')
        new_lang_data['description_data'] = json.dumps(v.get('description'))
        result.append(new_lang_data)
    return result


def convert_widget_data_to_dict(widget_data):
    """Convert widget data object to dict.

    Arguments:
        widget_data {object} -- Object data

    Returns:
        dictionary -- dictionary data

    """
    result = dict()
    settings = json.loads(widget_data.settings)

    result['widget_id'] = widget_data.widget_id
    result['repository_id'] = widget_data.repository_id
    result['widget_type'] = widget_data.widget_type
    result['settings'] = settings
    result['browsing_role'] = widget_data.browsing_role
    result['edit_role'] = widget_data.edit_role
    result['is_enabled'] = widget_data.is_enabled
    result['is_deleted'] = widget_data.is_deleted
    return result


def convert_widget_multi_lang_to_dict(multi_lang_data):
    """Convert multiple language data object to dict.

    Arguments:
        multi_lang_data {object} -- object data

    Returns:
        dictionary -- dictionary data

    """
    result = dict()
    description = json.loads(multi_lang_data.description_data)

    result['id'] = multi_lang_data.id
    result['widget_id'] = multi_lang_data.widget_id
    result['lang_code'] = multi_lang_data.lang_code
    result['label'] = multi_lang_data.label
    result['description_data'] = description
    return result


def convert_data_to_desgin_pack(widget_data, list_multi_lang_data):
    """Convert loaded data to widget design data pack.

    Arguments:
        widget_data {dict} -- widget data
        list_multi_lang_data {list} -- List of multiple language data

    Returns:
        dictionary -- widget design data pack

    """
    if not widget_data or not list_multi_lang_data:
        return None
    result = dict()
    result['widget_id'] = widget_data.get('widget_id')
    result['repository_id'] = widget_data.get('repository_id')
    result['widget_type'] = widget_data.get('widget_type')
    result['browsing_role'] = widget_data.get('browsing_role')
    result['edit_role'] = widget_data.get('edit_role')
    result['is_enabled'] = widget_data.get('is_enabled')
    result['is_deleted'] = widget_data.get('is_deleted')

    multi_lang_setting = dict()
    for data in list_multi_lang_data:
        new_data = dict()
        converted_data = convert_widget_multi_lang_to_dict(data)
        new_data['label'] = converted_data.get('label')
        new_data['description'] = converted_data.get('description_data')
        multi_lang_setting[converted_data.get('lang_code')] = new_data
    settings = widget_data.get('settings')
    settings['multiLangSetting'] = multi_lang_setting
    result['settings'] = settings

    return result


def convert_data_to_edit_pack(data):
    """Convert loaded data to edit data pack.

    Arguments:
        data {dict} -- loaded data

    Returns:
        dictionary -- edit data pack

    """
    if not data:
        return None
    result = dict()
    result_settings = dict()
    settings = copy.deepcopy(data.get('settings'))
    result['widget_id'] = data.get('widget_id')
    result['background_color'] = settings.get('background_color')
    result['browsing_role'] = data.get('browsing_role')
    result['edit_role'] = data.get('edit_role')
    result['is_enabled'] = data.get('is_enabled')
    result['enable'] = data.get('is_enabled')
    result['frame_border'] = settings.get('frame_border')
    result['frame_border_color'] = settings.get('frame_border_color')
    result['label_color'] = settings.get('label_color')
    result['multiLangSetting'] = settings.get('multiLangSetting')
    result['repository_id'] = data.get('repository_id')
    result['text_color'] = settings.get('text_color')
    result['widget_type'] = data.get('widget_type')
    if str(data.get('widget_type')) == 'Access counter':
        result_settings['access_counter'] = settings.get('access_counter')
    if str(data.get('widget_type')) == 'New arrivals':
        result_settings['new_dates'] = settings.get('new_dates')
        result_settings['display_result'] = settings.get('display_result')
        result_settings['rss_feed'] = settings.get('rss_feed')
    result['settings'] = result_settings
    return result
