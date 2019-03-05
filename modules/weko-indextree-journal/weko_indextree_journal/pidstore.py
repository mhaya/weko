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

"""Weko Indextree Journal Pid Store."""

from invenio_pidstore.fetchers import FetchedPID
from invenio_pidstore.models import (
    PersistentIdentifier, PIDStatus, RecordIdentifier)


def weko_indextree_journal_minter(record_uuid, data):
    """"""

    id_ = RecordIdentifier.next()
    recid = PersistentIdentifier.create(
        'recid',
        str(id_),
        object_type='rec',
        object_uuid=record_uuid,
        status=PIDStatus.REGISTERED
    )

    # Create ipid with same pid_value of the recid
    ipid = PersistentIdentifier.create(
        'ipid',
        str(recid.pid_value),
        object_type='rec',
        object_uuid=record_uuid,
        status=PIDStatus.REGISTERED,
    )

    data.update({
        '_indextree_journal': {
            'id': ipid.pid_value,
            'status': 'draft',
        },
    })

    return ipid


def weko_indextree_journal_fetcher(record_uuid, data):
    """Fetch a deposit identifier."""
    pid_value = data.get('_indextree_journal', {}).get('id')
    return FetchedPID(
        provider=None,
        pid_type='ipid',
        pid_value=pid_value,
    ) if pid_value else None
