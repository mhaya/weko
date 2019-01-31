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

"""Bundles for weko-index-tree."""

from flask_assets import Bundle
from invenio_assets import NpmBundle

style = Bundle(
    'css/weko_index_tree/styles.bundle.css',
    filters='cleancss',
    output="gen/index_tree_view.%(version)s.css"
)

js_treeview = NpmBundle(
    'js/weko_index_tree/inline.bundle.js',
    'js/weko_index_tree/polyfills.bundle.js',
    'js/weko_index_tree/main.bundle.js',
    output="gen/index_tree_view.js"
)

js = Bundle(
    'js/weko_index_tree/app.js',
    filters='requirejs',
    output="gen/index_tree.%(version)s.js"
)
js_dependecies_schema_form = NpmBundle(
    'node_modules/objectpath/lib/ObjectPath.js',
    'node_modules/tv4/tv4.js',
    'node_modules/angular-schema-form/dist/schema-form.js',
    'node_modules/angular-schema-form/dist/bootstrap-decorator.js',
    'node_modules/invenio-records-js/dist/invenio-records-js.js',
    npm={
        'angular-schema-form': '~0.8.13',
        'invenio-records-js': '~0.0.8',
        'objectpath': '~1.2.1',
        'tv4': '~1.2.7',
    }
)
