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

"""Utilities for download file."""

import mimetypes, unicodedata
from flask import abort, current_app, render_template, request
from invenio_records_files.utils import record_file_factory
from weko_records.api import FilesMetadata, ItemTypes
from .pdf import make_combined_pdf
from werkzeug.datastructures import Headers
from werkzeug.urls import url_quote
from invenio_files_rest.proxies import current_permission_factory
from .permissions import file_permission_factory
from .models import PDFCoverPageSettings
from invenio_files_rest.views import file_downloaded, check_permission
from invenio_files_rest.views import ObjectResource
from invenio_files_rest.models import ObjectVersion, FileInstance
from weko_deposit.api import WekoRecord


def weko_view_method(pid, record, template=None, **kwargs):
    r"""Display Weko view.

    Sends record_viewed signal and renders template.

    :param pid: PID object.
    :param record: Record object.
    :param template: Template to render.
    :returns: The rendered template.
    """
    flst = FilesMetadata.get_records(pid.pid_value)
    frecord = []

    if len(flst) > 0:
        for fj in flst:
            frecord.append(fj.dumps())

    item_type = ItemTypes.get_by_id(id_=record['item_type_id'])
    item_type_info = "{}({})".format(item_type.item_type_name.name,
                                     item_type.tag)
    return render_template(
        template,
        pid=pid,
        record=record,
        files=frecord,
        item_type_info=item_type_info
    )


def prepare_response(pid_value, fd=True):
    """
     prepare response data and header
    :param pid_value:
    :param fd:
    :return:
    """

    fn = request.view_args.get("filename")

    flst = FilesMetadata.get_records(pid_value)
    for fj in flst:
        if fj.dumps().get("display_name") == fn:
            stream = fj.model.contents[:]
            displaytype = fj.model.json.get("displaytype")
            file_name = fj.model.json.get("file_name")
            break

    headers = Headers()
    headers['Content-Length'] = len(stream)
    try:
        filenames = {'filename': fn.encode('latin-1')}
    except UnicodeEncodeError:
        filenames = {'filename*': "UTF-8''%s" % url_quote(fn)}
        encoded_filename = (unicodedata.normalize('NFKD', fn)
                            .encode('latin-1', 'ignore'))
        if encoded_filename:
            filenames['filename'] = encoded_filename

    if fd:
        headers.add('Content-Disposition', 'attachment', **filenames)
        mimetype = 'application/octet-stream'
    else:
        headers['Content-Type'] = 'text/plain; charset=utf-8'
        headers.add('Content-Disposition', 'inline')
        mimetype = mimetypes.guess_type(request.view_args.get("filename"))[0]
        # if 'detail' in displaytype and '.pdf' in file_name:
        #     from PyPDF2.pdf import PdfFileWriter, PdfFileReader
        #     import io
        #     source = PdfFileReader(io.BytesIO(stream), strict=True)
        #     fp = source.getPage(0)
        #     writer = PdfFileWriter()
        #     writer.addPage(fp)
        #     f = io.BytesIO()
        #     writer.write(f)
        #     stream = f.getvalue()

    rv = current_app.response_class(
        stream,
        mimetype=mimetype,
        headers=headers,
        direct_passthrough=True,
    )

    return rv


def file_preview_ui(pid, record, _record_file_factory=None, **kwargs):
    """File preview view for a given record.

    Plug this method into your ``RECORDS_UI_ENDPOINTS`` configuration:

    .. code-block:: python

        RECORDS_UI_ENDPOINTS = dict(
            recid=dict(
                # ...
                route='/records/<pid_value/file_preview/<filename>',
                view_imp='invenio_records_files.utils:file_preview_ui',
                record_class='invenio_records_files.api:Record',
            )
        )

    :param _record_file_factory:
    :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
        instance.
    :param record: The record metadata.
    """
    return file_ui(pid, record, _record_file_factory, is_preview=True, **kwargs)


def file_download_ui(pid, record, _record_file_factory=None, **kwargs):
    """File download view for a given record.

    Plug this method into your ``RECORDS_UI_ENDPOINTS`` configuration:

    .. code-block:: python

        RECORDS_UI_ENDPOINTS = dict(
            recid=dict(
                # ...
                route='/records/<pid_value/files/<filename>',
                view_imp='invenio_records_files.utils:file_download_ui',
                record_class='invenio_records_files.api:Record',
            )
        )

    :param _record_file_factory:
    :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
        instance.
    :param record: The record metadata.
    """
    return file_ui(pid, record, _record_file_factory, is_preview=False, **kwargs)


def file_ui(pid, record, _record_file_factory=None, is_preview=False, **kwargs):
    """
    :param is_preview: Determine the type of event. True: file-preview, False: file-download
    :param _record_file_factory:
    :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
        instance.
    :param record: The record metadata.
    """
    _record_file_factory = _record_file_factory or record_file_factory
    # Extract file from record.
    fileobj = _record_file_factory(
        pid, record, kwargs.get('filename')
    )

    if not fileobj:
        abort(404)

    obj = fileobj.obj

    # Check file contents permission
    if not file_permission_factory(record, fjson=fileobj).can():
        abort(403)

    # #Check permissions
    # ObjectResource.check_object_permission(obj)

    """ Send file without its pdf cover page """

    class ObjectResourceWeko(ObjectResource):

        # redefine `send_object` method to implement the no-cache function
        @staticmethod
        def send_object(bucket, obj, expected_chksum=None, logger_data=None, restricted=True, as_attachment=False, cache_timeout=-1):
            if not obj.is_head:
                check_permission(
                    current_permission_factory(obj, 'object-read-version'),
                    hidden=False
                )

            if expected_chksum and obj.file.checksum != expected_chksum:
                current_app.logger.warning(
                    'File checksum mismatch detected.', extra=logger_data)

            file_downloaded.send(current_app._get_current_object(), obj=obj)
            return obj.send_file(restricted=restricted, as_attachment=as_attachment)

    pdfcoverpage_set_rec = PDFCoverPageSettings.find(1)
    coverpage_state = WekoRecord.get_record_cvs(pid.object_uuid)

    if pdfcoverpage_set_rec.avail == 'disable' or coverpage_state == False: # Write this if statement later

        return ObjectResourceWeko.send_object(
        obj.bucket, obj,
        expected_chksum=fileobj.get('checksum'),
        logger_data={
            'bucket_id': obj.bucket_id,
            'pid_type': pid.pid_type,
            'pid_value': pid.pid_value,
        },
        as_attachment=False,
        cache_timeout=-1
        )

    """ Send file with its pdf cover page """
    object_version_record = ObjectVersion.query.filter_by(bucket_id= obj.bucket_id).first()
    file_instance_record = FileInstance.query.filter_by(id=object_version_record.file_id).first()
    obj_file_uri = file_instance_record.uri
    return make_combined_pdf(pid, obj_file_uri)
