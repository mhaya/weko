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

from flask import Flask, Blueprint, current_app, render_template, make_response
from reportlab.pdfgen import canvas
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

blueprint = Blueprint(
    'weko_deposit',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/pdf_test', methods=['GET'])

def pdf():
    output = io.BytesIO()
    fontname = "HeiseiMin-W3"
    pdfmetrics.registerFont(UnicodeCIDFont(fontname))
    p = canvas.Canvas(output)
    p.setFont(fontname, 30)
    p.drawString(10, 10, 'こんにちは、ReportLab!!')
    p.showPage()
    p.save()

    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
    response.mimetype = 'application/pdf'
    return response
