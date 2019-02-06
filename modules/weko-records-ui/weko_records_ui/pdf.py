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

""" Utilities for making the PDF cover page and newly combined PDFs. """
import io, unicodedata, hashlib
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import send_file
from weko_records.api import ItemsMetadata
from invenio_pidstore.models import PersistentIdentifier
from weko_admin.models import PDFCoverPageSettings


""" Function counting numbers of full-width character and half-width character differently """
def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


""" Function making PDF cover page """
def make_combined_pdf(pid, obj_file_uri):
    """
    meke the cover-page-combined PDF file
    :param pid: PID object
    :param file_uri: URI of the file object
    :return: cover-page-combined PDF file object
    """

    pid = pid.pid_value
    pidObject = PersistentIdentifier.get('recid', pid)
    record_metadata = ItemsMetadata.get_record(pidObject.object_uuid)

    """ Initialize Instance """
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_margins(20.0, 20.0)
    pdf.set_fill_color(100, 149, 237)

    pdf.add_font('IPAexg', '', '/code/modules/weko-records-ui/weko_records_ui/fonts/ipaexg00201/ipaexg.ttf', uni=True)
    pdf.add_font('IPAexm', '', '/code/modules/weko-records-ui/weko_records_ui/fonts/ipaexm00201/ipaexm.ttf', uni=True)

    w1 = 40
    w2 = 130
    footer_w = 90
    url_oapolicy_h = 7
    title_h = 8
    header_h = 20
    footer_h = 4
    meta_h = 9
    max_letters_num = 51
    cc_logo_xposition = 160

    """ Header """
    # Get the header settings
    record = PDFCoverPageSettings.query.filter(PDFCoverPageSettings.id == 1).first()
    header_display_type = record.header_display_type
    header_output_string = record.header_output_string
    header_output_image = record.header_output_image
    header_display_position = record.header_display_position

    # Set the header position
    positions = {}
    if header_display_position == 'left':
        positions['str_position'] = 'L'
        positions['img_position'] = 20
    elif header_display_position == 'center' or header_display_position == None:
        positions['str_position'] = 'C'
        positions['img_position'] = 85
    elif header_display_position == 'right':
        positions['str_position'] = 'R'
        positions['img_position'] = 150

    # Show header(string or image)
    if header_display_type == 'string':
        pdf.set_font('IPAexm', '', 22)
        pdf.multi_cell(w1+w2, header_h, header_output_string, 0, positions['str_position'], False)
    else:
        pdf.image(header_output_image, x=positions['img_position'], y=None, w=0, h=30, type='')
        pdf.set_y(55)

    """ Title """
    title = record_metadata['title_en']
    pdf.set_font('IPAexm', '', 20)
    pdf.multi_cell(w1 + w2, title_h, title, 0, 'L', False)
    pdf.ln(h='15')

    """ Metadata """
    pdf.set_font('Arial', '', 14)
    pdf.set_font('IPAexg', '', 14)
    if record_metadata['lang'] == 'en':
        record_metadata['lang'] = 'English'
    elif record_metadata['lang']  == 'ja':
        record_metadata['lang'] = 'Japanese'

    lang = record_metadata.get('lang')
    publisher = record_metadata['item_1548661157806'].get('subitem_1522300316516')
    pubdate = record_metadata.get('pubdate')
    keywords_ja = record_metadata.get('keywords')
    keywords_en = record_metadata.get('keywords_en')
    creator_mail = record_metadata['item_1538028816158']['creatorMails'][0].get('creatorMail')
    creator_name = record_metadata['item_1538028816158']['creatorNames'][0].get('creatorName')
    affiliation = record_metadata['item_1538028816158']['affiliation'][0].get('affiliationNames')
    metadata_list_values = [lang, publisher, pubdate, keywords_ja, keywords_en, creator_name, creator_mail, affiliation]

    for i, item in enumerate(metadata_list_values):
        if item == None:
            metadata_list_values[i] = ''

    metadata_list = [
        "Language: {}".format(metadata_list_values[0]),
        "Publisher: {}".format(metadata_list_values[1]),
        "Date of Publication: {}".format(metadata_list_values[2]),
        "Keywords(Ja): {}".format(metadata_list_values[3]),
        "Keywords(En): {}".format(metadata_list_values[4]),
        "Author: {}".format(metadata_list_values[5]),
        "E-mail: {}".format(metadata_list_values[6]),
        "Affiliation: {}".format(metadata_list_values[7])
    ]

    metadata = '\n'.join(metadata_list)
    metadata_lfnum = int(metadata.count('\n'))
    for item in metadata_list:
            metadata_lfnum += int(get_east_asian_width_count(item)) // max_letters_num

    url = '' # will be modified later
    url_lfnum = int(get_east_asian_width_count(url)) // max_letters_num

    oa_policy = '' # will be modified later
    oa_policy_lfnum = int(get_east_asian_width_count(oa_policy)) // max_letters_num

    # Save top coordinate
    top = pdf.y
    # Calculate x position of next cell
    offset = pdf.x + w1
    pdf.multi_cell(w1, meta_h, 'Metadata' + '\n'*(metadata_lfnum+1), 1, 'C', True)
    # Reset y coordinate
    pdf.y = top
    # Move to computed offset
    pdf.x = offset
    pdf.multi_cell(w2, meta_h, metadata, 1, 'L', False)
    top = pdf.y
    pdf.multi_cell(w1, url_oapolicy_h, 'URL' + '\n'*(url_lfnum+1), 1, 'C', True)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(w2, url_oapolicy_h, url, 1, 'L', False)
    top = pdf.y
    pdf.multi_cell(w1, url_oapolicy_h, 'OA Policy' + '\n'*(oa_policy_lfnum+1), 1, 'C', True)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(w2, url_oapolicy_h, oa_policy, 1, 'L', False)
    pdf.ln(h=1)

    ### Footer ###
    pdf.set_font('Courier', '', 10)
    pdf.set_x(108)

    license =  record_metadata['item_1538028827221'][0].get('licensetype')
    if license == 'license_free':  #自由入力
        txt = record_metadata['item_1538028827221'][0].get('licensefree')
        if txt == None:
            txt = ''
        pdf.multi_cell(footer_w, footer_h, txt, 0, 'L', False)
    elif license == 'license_0': #Attribution
        txt = 'This work is licensed under a Creative Commons Attribution 4.0 International License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by.png"
        lnk = "http://creativecommons.org/licenses/by/4.0/"
        pdf.multi_cell(footer_w, footer_h, txt, 0, 1, 'L', False)
        pdf.ln(h=2)
        pdf.image(src, x = cc_logo_xposition, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_1': #Attribution-ShareAlike
        txt = 'This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.'
        src= "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-sa.png"
        lnk = "http://creativecommons.org/licenses/by-sa/4.0/"
        pdf.multi_cell(footer_w, footer_h, txt, 0, 1, 'L', False)
        pdf.ln(h=2)
        pdf.image(src, x = cc_logo_xposition, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_2': #Attribution-NoDerivatives
        txt = 'This work is licensed under a Creative Commons Attribution-NoDerivatives 4.0 International License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nd.png"
        lnk = "http://creativecommons.org/licenses/by-nd/4.0/"
        pdf.multi_cell(footer_w, footer_h, txt, 0, 'L', False)
        pdf.ln(h=2)
        pdf.image(src, x = cc_logo_xposition, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_3': #Attribution-NonCommercial
        txt = 'This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nc.png"
        lnk = "http://creativecommons.org/licenses/by-nc/4.0/"
        pdf.multi_cell(footer_w, footer_h, txt, 0, 'L', False)
        pdf.ln(h=2)
        pdf.image(src, x = cc_logo_xposition, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_4': #Attribution-NonCommercial-ShareAlike
        txt = 'This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nc-sa.png"
        lnk = "http://creativecommons.org/licenses/by-nc-sa/4.0/"
        pdf.multi_cell(footer_w, footer_h, txt, 0, 'L', False)
        pdf.ln(h=2)
        pdf.image(src, x = cc_logo_xposition, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_5': #Attribution-NonCommercial-NoDerivatives
        txt = 'This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nc-nd.png"
        lnk = "http://creativecommons.org/licenses/by-nc-nd/4.0/"
        pdf.multi_cell(footer_w, footer_h, txt, 0, 'L', False)
        pdf.ln(h=2)
        pdf.image(src, x = cc_logo_xposition, y = None, w = 0, h = 0, type = '', link = lnk)
    else:
        pdf.multi_cell(footer_w, footer_h, '', 0, 'L', False)

    """ Convert PDF cover page data as Bytecode """
    output = pdf.output(dest = 'S').encode('latin-1')
    b_output = io.BytesIO(output)

    """ Combining cover page and existing pages """
    cover_page = PdfFileReader(b_output)
    f = open(obj_file_uri, "rb")
    existing_pages = PdfFileReader(f)
    combined_pages = PdfFileWriter()
    combined_pages.addPage(cover_page.getPage(0))
    for page_num in range(existing_pages.numPages):
        existing_page = existing_pages.getPage(page_num)
        combined_pages.addPage(existing_page)
    combined_filename = record_metadata["item_1538028827221"][0]["filename"] + '_combined_' + datetime.now().strftime('%Y%m%d')
    combined_file_path = "/code/combined-pdfs/{}.pdf".format(combined_filename)
    combined_file = open(combined_file_path, "wb")
    combined_pages.write(combined_file)
    combined_file.close()

    """ Download the newly generated combined PDF file """
    download_file_name = 'CV_' + record_metadata["item_1538028827221"][0]["filename"] # Modified later
    return send_file(combined_file_path, as_attachment = True, attachment_filename = download_file_name, mimetype ='application/pdf', cache_timeout = -1)
