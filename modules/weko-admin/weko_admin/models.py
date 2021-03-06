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

"""Database models for weko-admin."""

from datetime import datetime

from flask import current_app, json
from invenio_db import db
from sqlalchemy import asc
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from sqlalchemy_utils.types import JSONType


class SessionLifetime(db.Model):
    """Session Lifetime model.

    Stores session life_time create_date for Session.
    """

    __tablename__ = 'session_lifetime'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    _lifetime = db.Column('lifetime', db.Integer,
                          nullable=False, default=30)
    """ Session Life Time default units: minutes """

    create_date = db.Column(db.DateTime, default=datetime.now)

    is_delete = db.Column(db.Boolean(name='delete'),
                          default=False, nullable=False)

    @hybrid_property
    def lifetime(self):
        """
        Get lifetime.

        :return: Lifetime.
        """
        return self._lifetime

    @lifetime.setter
    def lifetime(self, lifetime):
        """
        Set lifetime.

        :param lifetime:
        :return: Lifetime.
        """
        self._lifetime = lifetime

    def create(self, lifetime=None):
        """
        Save session lifetime.

        :param lifetime: default None
        :return:
        """
        try:
            with db.session.begin_nested():
                if lifetime:
                    self.lifetime = lifetime
                self.is_delete = False
                db.session.add(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            raise
        return self

    @classmethod
    def get_validtime(cls):
        """Get valid lifetime.

        :returns: A :class:`~weko_admin.models.SessionLifetime` instance
            or ``None``.
        """
        return cls.query.filter_by(is_delete=False).one_or_none()

    @property
    def is_anonymous(self):
        """Return whether this UserProfile is anonymous."""
        return False


class SearchManagement(db.Model):
    """Search setting model."""

    __tablename__ = 'search_management'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    default_dis_num = db.Column(db.Integer, nullable=False, default=20)
    """ Default display number of search results"""

    default_dis_sort_index = db.Column(db.Text, nullable=True, default="")
    """ Default display sort of index search"""

    default_dis_sort_keyword = db.Column(db.Text, nullable=True, default="")
    """ Default display sort of keyword search"""

    sort_setting = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )
    """ The list of sort setting"""

    search_conditions = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )
    """ The list of search condition """

    search_setting_all = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )
    """ The list of search condition """

    create_date = db.Column(db.DateTime, default=datetime.now)
    """Create Time"""

    @classmethod
    def create(cls, data):
        """Create data."""
        try:
            dataObj = SearchManagement()
            with db.session.begin_nested():
                dataObj.default_dis_num = data.get('dlt_dis_num_selected')
                dataObj.default_dis_sort_index = data.get(
                    'dlt_index_sort_selected')
                dataObj.default_dis_sort_keyword = data.get(
                    'dlt_keyword_sort_selected')
                dataObj.sort_setting = data.get('sort_options')
                dataObj.search_conditions = data.get('detail_condition')
                dataObj.search_setting_all = data
                db.session.add(dataObj)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise
        return cls

    @classmethod
    def get(cls):
        """Get setting."""
        id = db.session.query(func.max(SearchManagement.id)).first()[0]
        if id is None:
            return None
        return cls.query.filter_by(id=id).one_or_none()

    @classmethod
    def update(cls, id, data):
        """Update setting."""
        try:
            with db.session.begin_nested():
                setting_data = cls.query.filter_by(id=id).one()
                setting_data.default_dis_num = data.get('dlt_dis_num_selected')
                setting_data.default_dis_sort_index = data.get(
                    'dlt_index_sort_selected')
                setting_data.default_dis_sort_keyword = data.get(
                    'dlt_keyword_sort_selected')
                setting_data.sort_setting = data.get('sort_options')
                setting_data.search_conditions = data.get('detail_condition')
                setting_data.search_setting_all = data
                db.session.merge(setting_data)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise
        return cls


class AdminLangSettings(db.Model):
    """System Language Display Setting.

    Stored target language and registered language
    """

    __tablename__ = 'admin_lang_settings'

    lang_code = db.Column(db.String(3), primary_key=True, nullable=False,
                          unique=True)

    lang_name = db.Column(db.String(30), nullable=False)

    is_registered = db.Column(db.Boolean(name='registered'), default=True)

    sequence = db.Column(db.Integer, default=0)

    is_active = db.Column(db.Boolean(name='active'), default=True)

    @classmethod
    def parse_result(cls, in_result):
        """Parse results."""
        obj = {}
        for k in in_result:
            record = dict()
            record['lang_code'] = k.lang_code
            record['lang_name'] = k.lang_name
            record['is_registered'] = k.is_registered
            record['sequence'] = k.sequence
            record['is_active'] = k.is_active
            obj[k.lang_code] = record

        json_list = []
        for key in obj:
            json_list.append({
                'lang_code': '{0}'.format(obj[key]['lang_code']),
                'lang_name': '{0}'.format(obj[key]['lang_name']),
                'is_registered': obj[key]['is_registered'],
                'sequence': obj[key]['sequence']
            })
        sorted_list = sorted(json_list, key=lambda k: k['sequence'])
        return sorted_list

    @classmethod
    def load_lang(cls):
        """Get language list.

        :return: A list of language
        """
        lang_list = cls.query.all()

        return cls.parse_result(lang_list)

    @classmethod
    def create(cls, lang_code, lang_name, is_registered, sequence, is_active):
        """Create language."""
        try:
            dataObj = AdminLangSettings()
            with db.session.begin_nested():
                dataObj.lang_code = lang_code
                dataObj.lang_name = lang_name
                dataObj.is_registered = is_registered
                dataObj.sequence = sequence
                dataObj.is_active = is_active
                db.session.add(dataObj)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise
        return cls

    @classmethod
    def update_lang(cls, lang_code=None, lang_name=None, is_registered=None,
                    sequence=None, is_active=None):
        """Save list language into database.

        :param lang_code: input language code
        :param lang_name: input language name
        :param is_registered: input boolean is language registered
        :param sequence: input order number of language
        :param is_active: input boolean is active of language
        :return: Updated record
        """
        with db.session.begin_nested():
            lang_setting_data = cls.query.filter_by(lang_code=lang_code).one()
            if lang_code is not None:
                lang_setting_data.lang_code = lang_code
            if lang_name is not None:
                lang_setting_data.lang_name = lang_name
            if is_registered is not None:
                lang_setting_data.is_registered = is_registered
            if sequence is not None:
                lang_setting_data.sequence = sequence
            if is_active is not None:
                lang_setting_data.is_active = is_active
            db.session.merge(lang_setting_data)

        db.session.commit()
        return cls

    @classmethod
    def get_lang_code(cls):
        """Get language code.

        :return: the language code
        """
        return cls.lang_code

    @classmethod
    def get_lang_name(cls):
        """Get language full name.

        :return: language full name
        """
        return cls.lang_name

    @classmethod
    def get_registered_language(cls):
        """Get registered languages.

        :return: All language have registered
        """
        result = cls.query.filter_by(is_registered=True)

        return cls.parse_result(result)

    @classmethod
    def get_active_language(cls):
        """Get active languages.

        :return: All languages have activated
        """
        result = cls.query.filter_by(is_active=True).order_by(
            asc('admin_lang_settings_sequence'))
        return cls.parse_result(result)


class ApiCertificate(db.Model):
    """Database for API Certificate."""

    __tablename__ = 'api_certificate'

    api_code = db.Column(db.String(3), primary_key=True, nullable=False,
                         unique=True)

    api_name = db.Column(db.String(25), nullable=False, unique=True)

    cert_data = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )

    @classmethod
    def select_all(cls):
        """Get all information about certificates in database.

        :return: list of pair (api short name, api full name, certificate data)
        """
        query_result = cls.query.all()
        result = []
        for record in query_result:
            data = dict()
            data['api_code'] = record.api_code
            data['api_name'] = record.api_name
            data['cert_data'] = record.cert_data
            result.append(data)
        return result

    @classmethod
    def select_by_api_code(cls, api_code):
        """Get certificate value by certificate type.

        :param api_code: input api short name
        :return: certificate data corresponding with api code
        """
        query_result = cls.query.filter_by(api_code=api_code).one_or_none()
        data = {}
        if query_result is not None:
            data['api_code'] = query_result.api_code
            data['api_name'] = query_result.api_name
            data['cert_data'] = query_result.cert_data

            return data
        else:
            return None

    @classmethod
    def update_cert_data(cls, api_code, cert_data):
        """Update certification data.

        Overwrite if certificate existed,
        otherwise insert new certificate into database.

        :param api_code: input api short name
        :param cert_data: input certificate value
        :return: true if success, otherwise false
        """
        query_result = cls.query.filter_by(api_code=api_code).one_or_none()
        # Update in case certificate already existed in database
        if query_result is None:
            return False
        else:
            try:
                with db.session.begin_nested():
                    query_result.cert_data = cert_data
                    db.session.merge(query_result)
                db.session.commit()
                return True
            except Exception as ex:
                current_app.logger.debug(ex)
                db.session.rollback()
                return False

    @classmethod
    def insert_new_api_cert(cls, api_code, api_name, cert_data=None):
        """Insert new certificate.

        :param api_code: input api code
        :param api_name: input api name
        :param cert_data: input certificate value with json format
        :return: True if success, otherwise False
        """
        try:
            dataObj = ApiCertificate()
            with db.session.begin_nested():
                if api_code is not None:
                    dataObj.api_code = api_code
                    dataObj.api_name = api_name
                if cert_data is not None:
                    dataObj.cert_data = cert_data
                db.session.add(dataObj)
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            return False

    @classmethod
    def update_api_cert(cls, api_code, api_name, cert_data):
        """Update API certification.

        Overwrite if certificate existed,
        otherwise insert new certificate into database.

        :param api_code: input api code
        :param api_name: input api name
        :param cert_data: input certificate value
        :return: true if success, otherwise false
        """
        # Get current api data
        query_result = cls.query.filter_by(api_code=api_code).one_or_none()

        if query_result is None:
            return False
        else:
            try:
                with db.session.begin_nested():
                    query_result.api_name = api_name
                    query_result.cert_data = cert_data
                    db.session.merge(query_result)
                db.session.commit()
                return True
            except Exception as ex:
                current_app.logger.debug(ex)
                db.session.rollback()
                return False


class StatisticUnit(db.Model):
    """Statistic Report Unit."""

    __tablename__ = 'stats_report_unit'

    unit_id = db.Column(db.String(100), primary_key=True, nullable=False,
                        unique=True)

    unit_name = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_all_stats_report_unit(cls):
        """Get all stats report unit.

        :return: List of unit
        """
        query_result = cls.query.all()
        result = []
        for res in query_result:
            data = dict()
            data['id'] = res.unit_id
            data['data'] = res.unit_name
            result.append(data)
        return result

    @classmethod
    def create(cls, unit_id, unit_name):
        """Create new unit.

        :param unit_id: The unit ID
        :param unit_name: The unit name
        :return: Unit if create succesfully
        """
        try:
            dataObj = StatisticUnit()
            with db.session.begin_nested():
                dataObj.unit_id = unit_id
                dataObj.unit_name = unit_name
                db.session.add(dataObj)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise

        return cls


class StatisticTarget(db.Model):
    """Statistic Report Target."""

    __tablename__ = 'stats_report_target'

    target_id = db.Column(db.String(100), primary_key=True, nullable=False,
                          unique=True)

    target_name = db.Column(db.String(255), nullable=False)

    target_unit = db.Column(db.String(100), nullable=True)

    @classmethod
    def get_all_stats_report_target(cls):
        """Get all stats report target.

        :return: List of target
        """
        query_result = cls.query.all()
        result = []
        for res in query_result:
            data = dict()
            data['id'] = res.target_id
            data['data'] = res.target_name
            data['unit'] = res.target_unit
            result.append(data)
        return result

    @classmethod
    def get_target_by_id(cls, target_id):
        """Get target by ID.

        :param target_id: the target ID
        :return: the target
        """
        query_result = cls.query.filter_by(target_id=target_id).one_or_none()
        return query_result

    @classmethod
    def create(cls, target_id, target_name, target_unit):
        """Create new target.

        :param target_id: The target ID
        :param target_name: The target name
        :return: The Target if create succesfully
        """
        try:
            dataObj = StatisticTarget()
            with db.session.begin_nested():
                dataObj.target_id = target_id
                dataObj.target_name = target_name
                dataObj.target_unit = target_unit
                db.session.add(dataObj)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise

        return cls


class LogAnalysisRestrictedIpAddress(db.Model):
    """Represent restricted addresses to be restricted from logging.

    The SiteLicenseIpAddress object contains a ``created`` and  a
    ``updated`` properties that are automatically updated.
    """

    __tablename__ = 'loganalysis_restricted_ip_address'

    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True
    )

    ip_address = db.Column(
        db.String(16),
        nullable=False,
        unique=True
    )

    @classmethod
    def get_all(cls):
        """Get all Ip Addresses.

        :return:  list.
        """
        try:
            all = cls.query.all()
        except Exception as ex:
            current_app.logger.debug(ex)
            all = []
            raise
        return all

    @classmethod
    def update_table(cls, ip_addresses):
        """Delete all rows and insert new ones."""
        try:
            with db.session.begin_nested():
                all_addresses = [LogAnalysisRestrictedIpAddress(ip_address=i)
                                 for i in ip_addresses]
                LogAnalysisRestrictedIpAddress.query.delete()
                db.session.add_all(all_addresses)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise
        return cls

    def __iter__(self):
        """TODO: __iter__."""
        for name in dir(LogAnalysisRestrictedIpAddress):
            if not name.startswith('__') and not name.startswith('_'):
                value = getattr(self, name)
                if isinstance(value, str):
                    yield (name, value)


class LogAnalysisRestrictedCrawlerList(db.Model):
    """Represent restricted users from txt list to be restricted from logging.

    The LogAnalysisRestrictedCrawlerList object contains a ``created`` and  a
    ``updated`` properties that are automatically updated.
    """

    __tablename__ = 'loganalysis_restricted_crawler_list'

    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True
    )

    list_url = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean(name='activated'),
        default=True
    )

    @classmethod
    def get_all(cls):
        """Get all crawler lists.

        :return: All crawler lists.
        """
        try:
            all = cls.query.order_by(asc(cls.id)).all()
        except Exception as ex:
            current_app.logger.debug(ex)
            all = []
            raise
        return all

    @classmethod
    def get_all_active(cls):
        """Get all active crawler lists.

        :return: All active crawler lists.
        """
        try:
            all = cls.query.filter(cls.is_active.is_(True)) \
                .filter(func.length(cls.list_url) > 0).all()
        except Exception as ex:
            current_app.logger.debug(ex)
            all = []
            raise
        return all

    @classmethod
    def add_list(cls, crawler_lists):
        """Add all crawler lists."""
        for list_url in crawler_lists:
            try:
                with db.session.begin_nested():
                    record = LogAnalysisRestrictedCrawlerList(
                        list_url=list_url)
                    db.session.add(record)
                db.session.commit()
            except Exception as ex:
                current_app.logger.debug(ex)
                db.session.rollback()
                raise
        return cls

    @classmethod
    def update_or_insert_list(cls, crawler_list):
        """Update or insert LogAnalysisRestrictedCrawlerList list."""
        for data in crawler_list:
            try:
                new_list = data.get('list_url', '')
                id = data.get('id', 0)
                is_active = data.get('is_active', True)
                with db.session.begin_nested():
                    current_record = cls.query.filter_by(id=id).one()
                    if current_record:
                        current_record.list_url = new_list
                        current_record.is_active = is_active
                        db.session.merge(current_record)
                    else:
                        db.session.add(
                            LogAnalysisRestrictedCrawlerList(list_url=new_list))
                db.session.commit()
            except BaseException as ex:
                current_app.logger.debug(ex)
                db.session.rollback()
                raise
        return cls

    def __iter__(self):
        """TODO: __iter__."""
        for name in dir(LogAnalysisRestrictedCrawlerList):
            if not name.startswith('__') and not name.startswith('_'):
                value = getattr(self, name)
                if isinstance(value, str):
                    yield (name, value)


class BillingPermission(db.Model):
    """Database for Billing Permission."""

    __tablename__ = 'billing_permission'

    user_id = db.Column(
        db.Integer(),
        primary_key=True,
        nullable=False,
        unique=True
    )

    is_active = db.Column(
        db.Boolean(name='active'),
        default=True,
        nullable=False
    )

    @classmethod
    def create(cls, user_id, is_active=True):
        """Create new user can access billing file.

        :param user_id: user's id
        :param is_active: access state
        :return: Unit if create succesfully
        """
        try:
            obj = BillingPermission()
            with db.session.begin_nested():
                obj.user_id = user_id
                obj.is_active = is_active
                db.session.add(obj)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise

        return cls

    @classmethod
    def activation(cls, user_id, is_active):
        """Change access state of user.

        :param user_id: user's id
        :param is_active: access state
        :return: Updated records
        """
        try:
            with db.session.begin_nested():
                billing_data = cls.query.filter_by(
                    user_id=user_id).one_or_none()
                if billing_data:
                    billing_data.is_active = is_active
                    db.session.merge(billing_data)
                else:
                    cls.create(user_id, is_active)
                    current_app.logger.info('New user is created!')
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise

        return cls

    @classmethod
    def get_billing_information_by_id(cls, user_id):
        """Get billing information by user id.

        :param user_id: user's id
        :return: Record or none
        """
        try:
            billing_information = cls.query.filter_by(
                user_id=user_id).one_or_none()
        except Exception as ex:
            current_app.logger.debug(ex)
            raise
        return billing_information


class StatisticsEmail(db.Model):
    """Save Email Address."""

    __tablename__ = 'stats_email_address'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_address = db.Column(db.String(255), nullable=False)

    @classmethod
    def insert_email_address(cls, email_address):
        """Insert Email Address."""
        try:
            dataObj = StatisticsEmail()
            with db.session.begin_nested():
                dataObj.email_address = email_address
                db.session.add(dataObj)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise ex
        return cls

    @classmethod
    def get_all_emails(cls):
        """Get all recepient emails as a list."""
        all_objects = cls.query.all()
        return [row.email_address for row in all_objects]

    @classmethod
    def get_all(cls):
        """Get all email address."""
        try:
            all = cls.query.all()
        except Exception as ex:
            current_app.logger.debug(ex)
            all = []
            raise
        return all

    @classmethod
    def delete_all_row(cls):
        """Delete all."""
        try:
            with db.session.begin_nested():
                delete_all = cls.query.delete()
            db.session.commit()
        except Exception as ex:
            current_app.logger.debug(ex)
            db.session.rollback()
            raise ex
        return delete_all


class RankingSettings(db.Model):
    """Ranking settings."""

    __tablename__ = 'ranking_settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    is_show = db.Column(db.Boolean(name='show'), nullable=False, default=False)

    new_item_period = db.Column(db.Integer, nullable=False, default=14)

    statistical_period = db.Column(db.Integer, nullable=False, default=365)

    display_rank = db.Column(db.Integer, nullable=False, default=10)

    rankings = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )

    @classmethod
    def get(cls, id=0):
        """Get ranking settings."""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def update(cls, id=0, data=None):
        """Update/Create ranking settings."""
        try:
            with db.session.begin_nested():
                new_data_flag = False
                settings = cls.query.filter_by(id=id).first()
                if not settings:
                    settings = RankingSettings()
                    new_data_flag = True
                settings.id = id
                settings.is_show = data.is_show
                settings.new_item_period = data.new_item_period
                settings.statistical_period = data.statistical_period
                settings.display_rank = data.display_rank
                settings.rankings = data.rankings
                if new_data_flag:
                    db.session.add(settings)
                else:
                    db.session.merge(settings)
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise
        return cls

    @classmethod
    def delete(cls, id=0):
        """Delete settings."""
        try:
            with db.session.begin_nested():
                cls.query.filter_by(id=id).delete()
            db.session.commit()
        except BaseException as ex:
            db.session.rollback()
            current_app.logger.debug(ex)
            raise ex
        return cls


class Settings(db.Model):
    """settings."""

    __tablename__ = 'admin_settings'

    id = db.Column(db.Integer, primary_key=True)

    def __setattr__(self, name, value):
        """Setattr."""
        db.Model.__setattr__(self, name, value)
        db.session.commit()

    items_search_author = db.Column(db.String(5), default='name')
    items_display_email = db.Column(db.Boolean(name='items_display_email'), default=True)


__all__ = ([
    'SearchManagement',
    'AdminLangSettings',
    'ApiCertificate',
    'StatisticUnit',
    'StatisticTarget',
    'LogAnalysisRestrictedIpAddress',
    'LogAnalysisRestrictedCrawlerList',
    'StatisticsEmail',
    'RankingSettings',
    'BillingPermission',
    'Settings'
])
