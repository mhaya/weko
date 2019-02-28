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

"""Item API."""

import re
from collections import OrderedDict

import pytz
from flask import current_app
from flask_security import current_user
from invenio_pidstore import current_pidstore
from invenio_pidstore.ext import pid_exists

from .api import ItemTypes, Mapping
from weko_schema_ui.schema import SchemaTree

import itertools

from flask import request
from invenio_search.api import RecordsSearch
from invenio_stats import current_stats

# from zenodo.modules.records.resolvers import record_resolver

# try:
#     from functools import lru_cache
# except ImportError:
#     from functools32 import lru_cache


def json_loader(data, pid):
    """
    Convert the item data and mapping to jpcoar
    :param data: json from item form post.
    :param pid: pid value.
    :return: dc, jrc, is_edit
    """
    dc = OrderedDict()
    jpcoar = OrderedDict()
    item = dict()
    ar = []

    if not isinstance(data, dict) or data.get("$schema") is None:
        return

    item_id = pid.object_uuid
    pid = pid.pid_value

    # get item type id
    index = data["$schema"].rfind('/')
    item_type_id = data["$schema"][index + 1:]

    # get item type mappings
    ojson = ItemTypes.get_record(item_type_id)
    mjson = Mapping.get_record(item_type_id)

    if ojson and mjson:
        mp = mjson.dumps()
        data.get("$schema")
        for k, v in data.items():
            if k != "pubdate":
                if k == "$schema" or mp.get(k) is None:
                    continue

            item.clear()
            item["attribute_name"] = ojson["properties"][k]["title"] \
                if ojson["properties"][k].get("title") is not None else k
            # set a identifier to add a link on detail page when is a creator field
            # creator = mp.get(k, {}).get('jpcoar_mapping', {})
            # creator = creator.get('creator') if isinstance(
            #     creator, dict) else None
            iscreator = False
            creator = ojson["properties"][k]
            if 'object' == creator["type"]:
                creator = creator["properties"]
                if 'iscreator' in creator:
                    iscreator = True
            elif 'array' == creator["type"]:
                creator = creator['items']["properties"]
                if 'iscreator' in creator:
                    iscreator = True
            if iscreator:
                item["attribute_type"] = 'creator'

            if isinstance(v, list):
                if len(v) > 0 and isinstance(v[0], dict):
                    item["attribute_value_mlt"] = v
                else:
                    item["attribute_value"] = v
            elif isinstance(v, dict):
                ar.append(v)
                item["attribute_value_mlt"] = ar
                ar = []
            else:
                item["attribute_value"] = v

            dc[k] = item.copy()
            if k != "pubdate":
                item.update(mp.get(k))
            else:
                pubdate = v
            jpcoar[k] = item.copy()

    if dc:
        # get the tile name to detail page
        title = data.get("title_ja") or data.get("title_en")

        if 'control_number' in dc:
            del dc['control_number']

        dc.update(dict(item_title=title))
        dc.update(dict(item_type_id=item_type_id))
        dc.update(dict(control_number=pid))

        # convert to es jpcoar mapping data
        jrc = SchemaTree.get_jpcoar_json(jpcoar)

        oai_value = current_app.config.get(
            'OAISERVER_ID_PREFIX', '') + str(pid)
        is_edit = pid_exists(oai_value, 'oai')
        if not is_edit:
            oaid = current_pidstore.minters['oaiid'](item_id, dc)
            oai_value = oaid.pid_value
        # relation_ar = []
        # relation_ar.append(dict(value="", item_links="", item_title=""))
        # jrc.update(dict(relation=dict(relationType=relation_ar)))
        # dc.update(dict(relation=dict(relationType=relation_ar)))
        jrc.update(dict(control_number=pid))
        jrc.update(dict(_oai={"id": oai_value}))
        jrc.update(dict(_item_metadata=dc))
        jrc.update(dict(itemtype=ojson.model.item_type_name.name))
        jrc.update(dict(publish_date=pubdate))

        # save items's creator to check permission
        user_id = current_user.get_id()
        if user_id:
            jrc.update(dict(weko_creator_id=user_id))
    del ojson, mjson, item
    return dc, jrc, is_edit


def set_timestamp(jrc, created, updated):
    jrc.update(
        {"_created": pytz.utc.localize(created)
            .isoformat() if created else None})

    jrc.update(
        {"_updated": pytz.utc.localize(updated)
            .isoformat() if updated else None})


def make_itemlist_desc(es_record):
    rlt = ""
    src = es_record
    op = src.pop("_options", {})
    ignore_meta = ('title', 'alternative', 'fullTextURL')
    if isinstance(op, dict):
        src["_comment"] = []
        for k, v in sorted(op.items(),
                           key=lambda x: x[1]['index'] if x[1].get(
                               'index') else x[0]):
            if k in ignore_meta:
                continue
            # item value
            vals = src.get(k)
            if isinstance(vals, list):
                # index, options
                v.pop('index', "")
                for k1, v1 in sorted(v.items()):
                    i = int(k1)
                    if i < len(vals):
                        crtf = v1.get("crtf")
                        showlist = v1.get("showlist")
                        hidden = v1.get("hidden")
                        is_show = False if hidden else showlist
                        # list index value
                        if is_show:
                            rlt = rlt + ((vals[i] + ",") if not crtf
                            else vals[i] + "\n")
            elif isinstance(vals, str):
                crtf = v.get("crtf")
                showlist = v.get("showlist")
                hidden = v.get("hidden")
                is_show = False if hidden else showlist
                if is_show:
                    rlt = rlt + ((vals + ",") if not crtf
                    else vals + "\n")
        if len(rlt) > 0:
            if rlt[-1] == ',':
                rlt = rlt[:-1]
            src['_comment'] = rlt.split('\n')
            if len(src['_comment'][-1]) == 0:
                src['_comment'].pop()


def sort_records(records, form):
    """
    sort records
    :param records:
    :param form:
    :return:
    """
    odd = OrderedDict()
    if isinstance(records, dict) and isinstance(form, list):
        for k in find_items(form):
            val = records.get(k[0])
            if val:
                odd.update({k[0]: val})
        # save schema link
        odd.update({"$schema": records.get("$schema")})
        del records
        return odd
    else:
        return records


def sort_op(record, kd, form):
    """
    sort options dict
    :param record:
    :param kd:
    :param form:
    :return:
    """
    odd = OrderedDict()
    if isinstance(record, dict) and isinstance(form, list):
        index = 0
        for k in find_items(form):
            # mapping target key
            key = kd.get(k[0])
            if not odd.get(key) and record.get(key):
                index += 1
                val = record.pop(key, {})
                val['index'] = index
                odd.update({key: val})

        record.clear()
        del record
        return odd
    else:
        return record


def find_items(form):
    """
    find sorted items into a list
    :param form:
    :return: lst
    """
    lst = []

    def find_key(node):
        if isinstance(node, dict):
            key = node.get('key')
            title = node.get('title')
            # type = node.get('type')
            if key:
                # title = title[title.rfind('.')+1:]
                yield [key, title or ""]
            for v in node.values():
                if isinstance(v, list):
                    for k in find_key(v):
                        yield k
        elif isinstance(node, list):
            for n in node:
                for k in find_key(n):
                    yield k

    for x in find_key(form):
        lst.append(x)

    return lst


def get_all_items(nlst, klst):
    """
    convert and sort item list
    :param nlst:
    :param klst:
    :return: alst
    """
    alst = []

    # def get_name(key):
    #     for lst in klst:
    #         k = lst[0].split('.')[-1]
    #         if key == k:
    #             return lst[1]
    def get_items(nlst):
        if isinstance(nlst, dict):
            for k, v in nlst.items():
                if isinstance(v, str):
                    alst.append({k: v})
                else:
                    get_items(v)
        elif isinstance(nlst, list):
            for lst in nlst:
                get_items(lst)

    to_orderdict(nlst, klst)
    get_items(nlst)
    return alst


def to_orderdict(alst, klst):
    """
    sort item list
    :param alst:
    :param klst:
    """
    if isinstance(alst, list):
        for i in range(len(alst)):
            if isinstance(alst[i], dict):
                alst.insert(i, OrderedDict(alst.pop(i)))
                to_orderdict(alst[i], klst)
    elif isinstance(alst, dict):
        nlst = []
        if isinstance(klst, list):
            for lst in klst:
                key = lst[0].split('.')[-1]
                val = alst.pop(key, {})
                if val:
                    if isinstance(val, dict):
                        val = OrderedDict(val)
                    nlst.append({key: val})
                if not alst:
                    break

            while len(nlst) > 0:
                alst.update(nlst.pop(0))

            for k, v in alst.items():
                if not isinstance(v, str):
                    to_orderdict(v, klst)


def get_options_and_order_list(item_type_id):
    """
     Get Options by item type id
    :param item_type_id:
    :return: options dict and sorted list
    """
    ojson = ItemTypes.get_record(item_type_id)
    solst = find_items(ojson.model.form)
    meta_options = ojson.model.render.pop('meta_fix')
    meta_options.update(ojson.model.render.pop('meta_list'))
    return solst, meta_options


def sort_meta_data_by_options(record_hit):
    """
    reset metadata by '_options'
    :param record_hit:
    """
    try:

        src = record_hit['_source'].pop('_item_metadata')
        item_type_id = record_hit['_source'].get('item_type_id') \
                       or src.get('item_type_id')
        if not item_type_id:
            return

        items = []
        solst, meta_options = get_options_and_order_list(item_type_id)

        newline = True
        for lst in solst:
            key = lst[0]

            val = src.get(key)
            option = meta_options.get(key, {}).get('option')
            if not val or not option:
                continue

            hidden = option.get("hidden")
            multiple = option.get('multiple')
            crtf = option.get("crtf")
            showlist = option.get("showlist")
            is_show = False if hidden else showlist

            if not is_show:
                continue

            mlt = val.get('attribute_value_mlt')
            if mlt:
                data = list(map(lambda x: ''.join(x.values()),
                                get_all_items(mlt, solst)))
            else:
                data = val.get('attribute_value')

            if data:
                if isinstance(data, list):
                    data = ",".join(data) if multiple else \
                        (data[0] if len(data) > 0 else "")

                if newline:
                    items.append(data)
                else:
                    items[-1] += "," + data

            newline = crtf

        if items:
            record_hit['_source']['_comment'] = items
    except Exception:
        current_app.logger.exception(
            u'Record serialization failed {}.'.format(
                str(record_hit['_source'].get('control_number'))))
    return


def get_keywords_data_load(str):
    """
     Get a json of item type info
    :return: dict of item type info
    """
    try:
        return [(x.name, x.id) for x in ItemTypes.get_latest()]
    except:
        pass
    return []


def get_record_from_context(**kwargs):
    """Get the cached record object from kwargs or the request context."""
    if 'record' in kwargs:
        return kwargs['record']
    else:
        if request and \
                hasattr(request._get_current_object(), 'current_file_record'):
            return request.current_file_record


def extract_event_record_metadata(record):
    """Extract from a record the payload needed for a statistics event."""
    return dict(
        record_id=str(record.id),
        recid=str(record['recid']) if record.get('recid') else None,
        conceptrecid=record.get('conceptrecid'),
        doi=record.get('doi'),
        conceptdoi=record.get('conceptdoi'),
        access_right=record.get('access_right'),
        resource_type=record.get('resource_type'),
        communities=record.get('communities'),
        owners=record.get('owners'),
    )


def build_record_stats(recid, conceptrecid):
    """Build the record's stats."""
    stats = {}
    stats_sources = {
        'record-view': {
            'params': {'recid': recid},
            'fields': {
                'views': 'count',
                'unique_views': 'unique_count',
            },
        },
        'record-download': {
            'params': {'recid': recid},
            'fields': {
                'downloads': 'count',
                'unique_downloads': 'unique_count',
                'volume': 'volume',
            },
        },
        'record-view-all-versions': {
            'params': {'conceptrecid': conceptrecid},
            'fields': {
                'version_views': 'count',
                'version_unique_views': 'unique_count',
            }
        },
        'record-download-all-versions': {
            'params': {'conceptrecid': conceptrecid},
            'fields': {
                'version_downloads': 'count',
                'version_unique_downloads': 'unique_count',
                'version_volume': 'volume',
            },
        },
    }
    for query_name, cfg in stats_sources.items():
        try:
            query_cfg = current_stats.queries[query_name]
            query = query_cfg.query_class(**query_cfg.query_config)
            result = query.run(**cfg['params'])
            for dst, src in cfg['fields'].items():
                stats[dst] = result.get(src)
        except Exception:
            pass
    return stats


def get_record_stats(recordid, throws=True):
    """Fetch record statistics from Elasticsearch."""
    try:
        res = (RecordsSearch()
               .source(include='_stats')  # only include "_stats" field
               .get_record(recordid)
               .execute())
        return res[0]._stats.to_dict() if res else None
    except Exception:
        if throws:
            raise
        pass


def chunkify(iterable, n):
    """Create equally sized tuple-chunks from an iterable."""
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


# @lru_cache(maxsize=1024)
# def fetch_record(recid):
#     """Cached record fetch."""
#     return record_resolver.resolve(recid)


# @lru_cache(maxsize=1024)
# def fetch_record_file(recid, filename):
#     """Cached record file fetch."""
#     _, record = fetch_record(recid)
#     return record.files[filename].obj
