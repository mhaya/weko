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

"""Utils for weko-records-ui."""
from flask import current_app
from flask_login import current_user


def can_download_original_pdf():
    """
    Check the role of user.
    :return: result
    """
    result = False
    user_id = current_user.get_id() if is_user_logged_in() else None
    if user_id:
        users = current_app.config['WEKO_PERMISSION_ROLE_USER_DOWNLOAD_ORIGINAL_PDF']
        print('--------users: ', users)
        for lst in list(current_user.roles or []):
            print('--------lst: ', lst.__dict__)
            if lst.name in users:
                result = True
    return result


def is_user_logged_in():
    return current_user and current_user.is_authenticated
