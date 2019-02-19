# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 National Institute of Informatics.
#
# WEKO-Indextree-Journal is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module of weko-indextree-journal."""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template, current_app
from flask_babelex import gettext as _
from weko_records.api import ItemTypes

blueprint = Blueprint(
    'weko_indextree_journal',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/indextree/journal',
)


@blueprint.route("/")
def index():
    """Render a basic view."""
    item_type_id = 1
    lists = ItemTypes.get_latest()
    if lists is None or len(lists) == 0:
        return render_template(
            current_app.config['WEKO_ITEMS_UI_ERROR_TEMPLATE']
        )
    item_type = ItemTypes.get_by_id(item_type_id)
    if item_type is None:
        return
    json_schema = '/items/jsonschema/{}'.format(item_type_id)
    schema_form = '/items/schemaform/{}'.format(item_type_id)

    return render_template(
        # "weko_indextree_journal/index.html",
        current_app.config['WEKO_INDEXTREE_JOURNAL_INDEX_TEMPLATE'],
        get_tree_json=current_app.config['WEKO_INDEX_TREE_LIST_API'],
        upt_tree_json='',
        mod_tree_detail=current_app.config['WEKO_INDEX_TREE_API'],
        record=None,
        jsonschema=json_schema,
        schemaform=schema_form,
        lists=lists,
        links=None,
        id=item_type_id,
        files=None,
        pid=None
    )
    """
    return render_template(
        "weko_indextree_journal/index.html",
        module_name=_('WEKO-Indextree-Journal'))
    """
