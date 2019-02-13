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
import io, unicodedata, json
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import send_file, current_app
from weko_records.api import ItemsMetadata, ItemMetadata, ItemType
from invenio_pidstore.models import PersistentIdentifier
from invenio_db import db
from .models import PDFCoverPageSettings

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
    item_metadata = ItemsMetadata.get_record(pidObject.object_uuid)
    item_type = db.session.query(ItemType).filter(ItemType.id==ItemMetadata.item_type_id).first()


    """ Initialize Instance """
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_margins(20.0, 20.0)
    pdf.set_fill_color(100, 149, 237)

    pdf.add_font('IPAexg', '', current_app.config["JPAEXG_TTF_FILEPATH"], uni=True)
    pdf.add_font('IPAexm', '', current_app.config["JPAEXM_TTF_FILEPATH"], uni=True)

    # Parameters such as width and height of rows/columns
    w1 = 40  # width of the left column
    w2 = 130  # width of the right column
    footer_w = 90  # width of the footer cell
    #url_oapolicy_h = 7  # height of the URL & OA-policy
    url_oapolicy_h = current_app.config['URL_OA_POLICY_HEIGHT']  # height of the URL & OA-policy
    # title_h = 8  # height of the title
    title_h = current_app.config['TITLE_HEIGHT']  # height of the title
    # header_h = 20  # height of the header cell
    header_h = current_app.config['HEADER_HEIGHT'] # height of the header cell
    # footer_h = 4  # height of the footer cell
    footer_h = current_app.config['FOOTER_HEIGHT'] # height of the footer cell
    # meta_h = 9  # height of the metadata cell
    meta_h = current_app.config['METADATA_HEIGHT']  # height of the metadata cell
    max_letters_num = 51  # number of maximum letters that can be contained in the right column
    cc_logo_xposition = 160  # x-position where Creative Commons logos are placed

    """ Header """
    # Get the header settings
    record = PDFCoverPageSettings.find(1)
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
    title = item_metadata['title_en']
    pdf.set_font('IPAexm', '', 20)
    pdf.multi_cell(w1 + w2, title_h, title, 0, 'L', False)
    pdf.ln(h='15')

    """ Metadata """
    # publisher_parent_key = None
    # publisher_child_key = None
    # schema_prop = item_type.schema["properties"]
    # for parent_key in schema_prop:
    #     if "properties" in schema_prop[parent_key]:
    #         for child_key in schema_prop[parent_key]["properties"]:
    #             if schema_prop[parent_key]["properties"][child_key].get("title") != '出版者':
    #                 continue
    #             else:
    #                 publisher_parent_key = parent_key
    #                 publisher_child_key = child_key
    #
    # # print(publisher_parent_key, publisher_child_key)

    pdf.set_font('Arial', '', 14)
    pdf.set_font('IPAexg', '', 14)

    if item_metadata['lang'] == 'en':
        item_metadata['lang'] = 'English'
    elif item_metadata['lang']  == 'ja':
        item_metadata['lang'] = 'Japanese'

    try:
        lang = item_metadata.get('lang')
    except (KeyError, IndexError):
        lang = None
    try:
        publisher = item_metadata['item_1548661157806'].get('subitem_1522300316516')
        # publisher = item_metadata[publisher_parent_key].get(publisher_child_key)
    except (KeyError, IndexError):
        publisher = None
    try:
        pubdate = item_metadata.get('pubdate')
    except (KeyError, IndexError):
        pubdate = None
    try:
        keywords_ja = item_metadata.get('keywords')
    except (KeyError, IndexError):
        keywords_ja = None
    try:
        keywords_en = item_metadata.get('keywords_en')
    except (KeyError, IndexError):
        keywords_en = None
    try:
        creator_mail = item_metadata['item_1538028816158']['creatorMails'][0].get('creatorMail')
    except (KeyError, IndexError):
        creator_mail = None
    try:
        creator_name = item_metadata['item_1538028816158']['creatorNames'][0].get('creatorName')
    except (KeyError, IndexError):
        creator_name = None
    try:
        affiliation = item_metadata['item_1538028816158']['affiliation'][0].get('affiliationNames')
    except (KeyError, IndexError):
        affiliation = None

    metadata_dict = {
                     "lang": lang,
                     "publisher": publisher,
                     "pubdate": pubdate,
                     "keywords_ja": keywords_ja,
                     "keywords_en": keywords_en,
                     "creator_mail": creator_mail,
                     "creator_name": creator_name,
                     "affiliation": affiliation
                     }

    # Change the values from None to '' for printing
    for key in metadata_dict:
        if metadata_dict[key] == None:
            metadata_dict[key] = ''

    metadata_list = [
        "Language: {}".format(metadata_dict["lang"]),
        "Publisher: {}".format(metadata_dict["publisher"]),
        "Date of Publication: {}".format(metadata_dict["pubdate"]),
        "Keywords(Ja): {}".format(metadata_dict["keywords_ja"]),
        "Keywords(En): {}".format(metadata_dict["keywords_en"]),
        "Author: {}".format(metadata_dict["creator_name"]),
        "E-mail: {}".format(metadata_dict["creator_mail"]),
        "Affiliation: {}".format(metadata_dict["affiliation"])
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

    license =  item_metadata['item_1538028827221'][0].get('licensetype')
    if license == 'license_free':  #自由入力
        txt = item_metadata['item_1538028827221'][0].get('licensefree')
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

    """ Download the newly generated combined PDF file """
    try:
        combined_filename = 'CV_' + datetime.now().strftime('%Y%m%d') + '_' + item_metadata["item_1538028827221"][0].get("filename")
    except (KeyError, IndexError):
        combined_filename = 'CV_' + title + '.pdf'
    combined_filepath = "/code/combined-pdfs/{}.pdf".format(combined_filename)
    combined_file = open(combined_filepath, "wb")
    combined_pages.write(combined_file)
    combined_file.close()
    return send_file(combined_filepath, as_attachment = True, attachment_filename = combined_filename, mimetype ='application/pdf', cache_timeout = -1)
