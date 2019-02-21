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

"""Record UI models."""

from invenio_db import db

class InstitutionName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(255), default='')

    @classmethod
    def get_institution_name(cls):
        if len(cls.query.all()) < 1:
            db.session.add(cls())
            db.session.commit()
        return cls.query.get(1).institution_name

    @classmethod
    def set_institution_name(cls, new_name):
        cfg = cls.query.get(1)
        cfg.institution_name = new_name
        db.session.commit()
