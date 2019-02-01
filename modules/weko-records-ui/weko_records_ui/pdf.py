import io
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import send_file
from weko_records.api import ItemsMetadata
from invenio_pidstore.models import PersistentIdentifier
from weko_admin.models import PDFCoverPageSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_wtf import FlaskForm

def make_combined_pdf(pid):

    pid = pid.pid_value
    pidObject = PersistentIdentifier.get('recid', pid)
    record_metadata = ItemsMetadata.get_record(pidObject.object_uuid)

    """ Initialize Instance """
    pdf = FPDF('P', 'mm', (222.2, 282.9))
    pdf.add_page()
    pdf.set_margins(20.0, 35.0, 20.0)
    pdf.set_fill_color(100, 149, 237)
    w1 = 40
    w2 = 142
    h = 7
    header_h = 20
    meta_h = 10

    """ Header """
    # Get the header settings
    engine = create_engine('postgresql+psycopg2://invenio:dbpass123@postgresql:5432/invenio')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    record = session.query(PDFCoverPageSettings).filter(PDFCoverPageSettings.id == 1).first()
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
        positions['img_position'] = 95
    elif header_display_position == 'right':
        positions['str_position'] = 'R'
        positions['img_position'] = 175

    # Show header(string or image)
    if header_display_type == 'string':
        pdf.set_font('Courier', 'I', 22)
        #pdf.set_x(60)
        # pdf.cell(100, 20, header, 1, 1, 'C')
        pdf.multi_cell(w1+w2, header_h, header_output_string, 0, positions['str_position'], False)
        # pdf.image()  # If a image is used
    else:
        pdf.image(header_output_image, x=positions['img_position'], y=None, w=30, h=30, type='')
        pdf.set_y(50.0)

    """ Title """
    title = record_metadata['title_en']
    pdf.set_font('Times', 'B', 20)
    pdf.multi_cell(w1+w2, h, title, 0, 'L', False)
    pdf.ln(h='15')

    """ Metadata """
    pdf.set_font('Arial', '', 14)
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

    url = ''
    url_lfnum = int(len(url)) // 51 #+ int(url.count('\n'))# 51 is the max letter number within a line

    oa_policy = ''

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
    pdf.multi_cell(w1, h, 'URL' + '\n'*(url_lfnum+1), 1, 'C', True)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(w2, h, url, 1, 'L', False)
    top = pdf.y
    pdf.multi_cell(w1, h, 'OA Policy', 1, 'C', True)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(w2, h, oa_policy, 1, 'L', False)

    ### Footer ###
    pdf.set_font('Helvetica', '', 11)
    pdf.set_x(100)

    license =  record_metadata['item_1538028827221'][0].get('licensetype')
    if license == 'license_free':  #自由入力
        txt = record_metadata['item_1538028827221'][0].get('licensefree')
        if txt == None:
            txt = ''
        pdf.multi_cell(80, h, txt, 0, 'R', False)
    elif license == 'license_0': #表示
        txt = 'This work is licensed under a Creative Commons Attribution 2.1 Japan License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by.png"
        lnk = "http://creativecommons.org/licenses/by/2.1/jp/"
        pdf.multi_cell(50, h, txt, 0, 1, 'R', False)
        pdf.image(src, x = 170, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_1': #表示 - 継承
        txt = 'This work is licensed under a Creative Commons Attribution-ShareAlike 2.1 Japan License.'
        src= "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-sa.png"
        lnk = "http://creativecommons.org/licenses/by-sa/2.1/jp/"
        pdf.multi_cell(0, h, txt, 0, 1, 'R', False)
        pdf.image(src, x = 170, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_2': #表示 - 改変禁止
        txt = 'This work is licensed under a Creative Commons Attribution-NoDerivs 2.1 Japan License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nd.png"
        lnk = "http://creativecommons.org/licenses/by-nd/2.1/jp/"
        pdf.multi_cell(0, h, txt, 0, 'R', False)
        pdf.image(src, x = 170, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_3': #表示 - 非営利
        txt = 'This work is licensed under a Creative Commons Attribution-NonCommercial 2.1 Japan License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nc.png"
        lnk = "http://creativecommons.org/licenses/by-nc/2.1/jp/"
        pdf.multi_cell(0, h, txt, 0, 'R', False)
        pdf.image(src, x = 170, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_4': #表示 - 非営利 - 継承
        txt = 'This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 2.1 Japan License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nc-sa.png"
        lnk = "http://creativecommons.org/licenses/by-nc-sa/2.1/jp/"
        pdf.multi_cell(0, h, txt, 0, 'R', False)
        pdf.image(src, x = 170, y = None, w = 0, h = 0, type = '', link = lnk)
    elif license == 'license_5': #表示 - 非営利 - 改変禁止
        txt = 'This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivs 2.1 Japan License.'
        src = "modules/weko-records-ui/weko_records_ui/static/images/creative_commons/by-nc-nd.png"
        lnk = "http://creativecommons.org/licenses/by-nc-nd/2.1/jp/"
        pdf.multi_cell(100, 5, txt, 0, 'R', False)
        pdf.image(src, x = 170, y = None, w = 0, h = 0, type = '', link = lnk)
    else:
        pdf.multi_cell(0, h, '', 0, 'R', False)

    ### Export as PDF ###
    output = pdf.output('test_fpdf.pdf', dest = 'S').encode('latin-1')
    b_output = io.BytesIO(output)

    ### Combining cover page and existing pages ###
    cover_page = PdfFileReader(b_output)
    obj_file_uri = '/var/tmp/16/b5/bab6-51b6-4429-8967-7211e5b84260/data' #Modified later
    f = open(obj_file_uri, "rb")
    existing_pages = PdfFileReader(f)
    combined_pages = PdfFileWriter()
    combined_pages.addPage(cover_page.getPage(0))
    for page_num in range(existing_pages.numPages):
        existing_page = existing_pages.getPage(page_num)
        combined_pages.addPage(existing_page)
    combined_file_path ='/code/combined-pdfs/combined-file.pdf'  # Modified later
    combined_file = open(combined_file_path, "wb")
    combined_pages.write(combined_file)
    combined_file.close()

    ### Download the newly generated combined PDF file ###
    download_file_name = 'combined-file.pdf' # Modified later
    return send_file(combined_file_path, as_attachment = False, attachment_filename = download_file_name, mimetype ='application/pdf', cache_timeout = -1)


# ## Another Draft ###
# def make_combined_pdf2(pid):
#     ###
#     pid = pid.pid_value
#     pidObject = PersistentIdentifier.get('recid', pid)
#     record_metadata = ItemsMetadata.get_record(pidObject.object_uuid)
#
#     ### Initialize Instance ###
#     pdf = FPDF('P', 'mm', (222.2, 282.9))
#     pdf.add_page()
#     pdf.set_margins(20.0, 20.0)
#     pdf.set_fill_color(10, 210, 100)
#
#     ### Header ###
#     header = '<Header Inserted Here>'
#     pdf.set_font('Courier', 'I', 16)
#     pdf.set_x(62)
#     pdf.cell(100, 20, header, 1, 1, 'C')
#     #pdf.image()  # If a image is used
#
#     ### Title ###
#     title = record_metadata['title_en']
#     pdf.set_font('Times', 'B', 16)
#     pdf.multi_cell(0, 20, title, 0, 'C', 'F')
#
#     ### Metadata ###
#     w1 = 58
#     w2 = 135
#     h = 10
#
#     metadata_list = [record_metadata['lang'], record_metadata['pubdate'], '']
#     metadata = '\n'.join(metadata_list)
#     metadata_lfnum = int(metadata.count('\n'))
#     print(type(metadata_lfnum))
#     print(metadata_lfnum)
#
#     url = '<URL Inserted Here>'
#
#     oa_policy = '<OA Policy Inserted Here>'
#
#     pdf.set_font('Arial', '', 14)
#     pdf.cell(w1, h, 'Metadata' + '\n'*metadata_lfnum, 1, 0, 'C', True)
#     pdf.cell(w2, h, metadata, 1, 1, 'C')
#     pdf.cell(w1, h, 'URL', 1, 0, 'C', True)
#     pdf.cell(w2, h, url, 1, 1, 'C')
#     pdf.cell(w1, h, 'OA Policy', 1, 0, 'C', True)
#     pdf.cell(w2, h, oa_policy, 1, 1, 'C')
#
#
#     # pdf.cell(w1, h, 'Author', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Author Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Affiliation', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Affiliation Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Journal / Magazine', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Journal/Magazine>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Publisher', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Publisher Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Publication Year', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Publication Year Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Volume', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Volume Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Issue', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Issue Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'Page Number', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<Page Number Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'URL', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<URL Inserted Here>', 1, 1, 'C')
#     # pdf.cell(w1, h, 'OA Policy', 1, 0, 'C', True)
#     # pdf.cell(w2, h, '<OA Policy Inserted Here>', 1, 1, 'C')
#
#     ### Footer ###
#     pdf.set_font('Helvetica', '', 11)
#     pdf.multi_cell(0, 10, '<Footer Inserted Here>', 0, 'R', 'F')
#
#     ### Export as PDF ###
#     output = pdf.output('test_fpdf.pdf', dest = 'S').encode('latin-1')
#     b_output = io.BytesIO(output)
#
#     ### Combining cover page and existing pages ###
#     cover_page = PdfFileReader(b_output)
#     obj_file_uri = '/var/tmp/16/b5/bab6-51b6-4429-8967-7211e5b84260/data' #Modified later
#     f = open(obj_file_uri, "rb")
#     existing_pages = PdfFileReader(f)
#     combined_pages = PdfFileWriter()
#     combined_pages.addPage(cover_page.getPage(0))
#     for page_num in range(existing_pages.numPages):
#         existing_page = existing_pages.getPage(page_num)
#         combined_pages.addPage(existing_page)
#     combined_file_path ='/code/combined-file.pdf'  # Modified later
#     combined_file = open(combined_file_path, "wb")
#     combined_pages.write(combined_file)
#     combined_file.close()
#
#     ### Download the newly generated combined PDF file ###
#     download_file_name = 'combined-file.pdf' # Modified later
#     response = send_file(combined_file_path, as_attachment = True, attachment_filename = download_file_name, mimetype ='application/pdf', cache_timeout = -1)
#     response.headers['Content-Disposition'] = "attachment; filename='PD1-paper.pdf"
#     return  response
