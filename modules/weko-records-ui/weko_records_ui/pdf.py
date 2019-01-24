import io
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import send_file

def make_combined_pdf():
    ### Initialize Instance ###
    pdf = FPDF('P', 'mm', (222.2, 282.9))
    pdf.add_page()
    pdf.set_margins(20.0, 20.0)
    pdf.set_fill_color(10, 210, 100)

    ### Header ###
    pdf.set_font('Courier', 'I', 16)
    pdf.set_x(60)
    pdf.cell(100, 30, '<Header Inserted Here>', 1, 1, 'C')
    # pdf.image()  # If a image is used

    ### Title ###
    pdf.set_font('Times', 'B', 16)
    pdf.multi_cell(0, 50, '<Title of the Article Inserted Here>', 0, 'C', 'F')

    ### Items ###
    w = 182
    h1 = 10
    h2 = 40
    pdf.set_font('Arial', '', 14)
    pdf.multi_cell(w, h1, 'Metadata', 1, 'L', True)
    pdf.multi_cell(w, h2, '<Metadata Incerted Here>', 1, 'C', False)
    pdf.multi_cell(w, h1, 'URL', 1, 'L', True)
    pdf.multi_cell(w, h2, '<URL Inserted Here>', 1, 'C', False)
    pdf.multi_cell(w, h1, 'OA Policy', 1, 'L', True)
    pdf.multi_cell(w, h2, '<OA Policy Inserted Here>', 1, 'C', False)

    ### Footer ###
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 10, '<Footer Inserted Here>', 0, 'R', 'F')

    ### Export as PDF ###
    output = pdf.output('test_fpdf.pdf', dest = 'S').encode('latin-1')
    b_output = io.BytesIO(output)

    ### Combining cover page and existing pages ###
    cover_page = PdfFileReader(b_output)
    obj_file_uri = '/var/tmp/31/e8/8811-171f-4aa5-ba83-e9b01bfeac29/data' #Modified later
    f = open(obj_file_uri, "rb")
    existing_pages = PdfFileReader(f)
    combined_pages = PdfFileWriter()
    combined_pages.addPage(cover_page.getPage(0))
    for page_num in range(existing_pages.numPages):
        existing_page = existing_pages.getPage(page_num)
        combined_pages.addPage(existing_page)
    combined_file_path ='/var/tmp/combined-pdfs/combined-file.pdf'  # Modified later
    combined_file = open(combined_file_path, "wb")
    combined_pages.write(combined_file)
    combined_file.close()

    ### Download the newly generated combined PDF file ###
    download_file_name = 'combined-file.pdf' # Modified later
    return send_file(combined_file_path, as_attachment = False, attachment_filename = download_file_name, mimetype ='application/pdf')


### Another Draft ###
# def make_combined_pdf():
#     ### Initialize Instance ###
#     pdf = FPDF('P', 'mm', (222.2, 282.9))
#     pdf.add_page()
#     pdf.set_margins(14.5, 14.5)
#     pdf.set_fill_color(10, 210, 100)
#
#     ### Header ###
#     pdf.set_font('Courier', 'I', 16)
#     pdf.set_x(62)
#     pdf.cell(100, 20, '<Header Inserted Here>', 1, 1, 'C')
#     #pdf.image()  # If a image is used
#
#     ### Title ###
#     pdf.set_font('Times', 'B', 16)
#     pdf.multi_cell(0, 20, '<Title of the Article Inserted Here>', 0, 'C', 'F')
#
#     ### Items ###
#     w1 = 58
#     w2 = 135
#     h = 20
#     pdf.set_font('Arial', '', 14)
#     pdf.cell(w1, h, 'Author', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Author Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Affiliation', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Affiliation Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Journal / Magazine', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Journal/Magazine>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Publisher', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Publisher Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Publication Year', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Publication Year Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Volume', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Volume Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Issue', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Issue Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'Page Number', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<Page Number Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'URL', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<URL Inserted Here>', 1, 1, 'C')
#     pdf.cell(w1, h, 'OA Policy', 1, 0, 'C', True)
#     pdf.cell(w2, h, '<OA Policy Inserted Here>', 1, 1, 'C')
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
#     obj_file_uri = '/var/tmp/31/e8/8811-171f-4aa5-ba83-e9b01bfeac29/data' #Modified later
#     f = open(obj_file_uri, "rb")
#     existing_pages = PdfFileReader(f)
#     combined_pages = PdfFileWriter()
#     combined_pages.addPage(cover_page.getPage(0))
#     for page_num in range(existing_pages.numPages):
#         existing_page = existing_pages.getPage(page_num)
#         combined_pages.addPage(existing_page)
#     combined_file_path ='/var/tmp/combined-pdfs/combined-file.pdf'  # Modified later
#     combined_file = open(combined_file_path, "wb")
#     combined_pages.write(combined_file)
#     combined_file.close()
#
#     ### Download the newly generated combined PDF file ###
#     download_file_name = 'combined-file.pdf' # Modified later
#     return send_file(combined_file_path, as_attachment = False, attachment_filename = download_file_name, mimetype ='application/pdf')
