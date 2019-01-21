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

"""Blueprint for weko-deposit."""

from flask import Flask, Blueprint, current_app, render_template, make_response, send_file
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from fpdf import FPDF
import io

blueprint = Blueprint(
    'weko_deposit',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/pdf_test', methods=['GET'])

def pdf():
    # output = io.BytesIO()
    # fontname = "HeiseiMin-W3"
    # pdfmetrics.registerFont(UnicodeCIDFont(fontname))
    # p = canvas.Canvas(output)
    # p.setFont(fontname, 30)
    # p.drawString(10, 10, 'こんにちは、ReportLab!!')
    # p.showPage()
    # p.save()
    #
    # pdf_out = output.getvalue()
    # output.close()
    #
    # response = make_response(pdf_out)
    #response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
    # response.mimetype = 'application/pdf'
    # return response

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    fontname = "HeiseiMin-W3"
    pdfmetrics.registerFont(UnicodeCIDFont(fontname))
    can = canvas.Canvas(packet)
    can.setFont(fontname, 30)
    content = "こんにちは、ReportLab"
    can.drawString(10, 100, content)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(blueprint.root_path + "/original.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    #finally, write "output" to a real file
    outputStream = open(blueprint.root_path + "/destination2.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    download_file_name = 'test.pdf'
    download_file = blueprint.root_path + '/destination2.pdf'
    # response = make_response()
    # response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
    # response.data = open("destination.pdf", "rb").read()
    # response.mimetype = 'application/pdf'
    # return response
    return send_file(download_file, as_attachment = True, attachment_filename = download_file_name, mimetype ='application/pdf')
