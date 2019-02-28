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

"""weko records extension."""

from . import config
from .indexer import indexer_receiver
# from .utils import serialize_record
# from weko_records_ui.views import blueprint, record_communities

from invenio_pidrelations.contrib.versioning import versioning_blueprint
from invenio_indexer.signals import before_record_index


class WekoRecords(object):
    """weko-records extension."""

    def __init__(self, app=None):
        """Extension initialization.

        :param app: The Flask application.
        """
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization.

        :param app: The Flask application.
        """
        self.init_config(app)
        # Register context processors
        app.context_processor(record_communities)
        # Register blueprint
        app.register_blueprint(blueprint)
        # Add global record serializer template filter
        app.add_template_filter(serialize_record, 'serialize_record')

        # Register versioning blueprint
        app.register_blueprint(versioning_blueprint)


        before_record_index.connect(indexer_receiver, sender=app)
        app.extensions['weko-records'] = self



    def init_config(self, app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        # Use theme's base template if theme is installed
        if 'BASE_TEMPLATE' in app.config:
            app.config.setdefault(
                'WEKO_RECORDS_BASE_TEMPLATE',
                app.config['BASE_TEMPLATE'],
            )
        for k in dir(config):
            if k.startswith('WEKO_RECORDS_'):
                app.config.setdefault(k, getattr(config, k))
