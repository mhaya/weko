import os
from flask import url_for
from flask_wtf import FlaskForm
from invenio_db import db
from datetime import datetime
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class PDFCoverPageSettings(db.Model):
    #availability = StringField()
    __tablename__ = 'pdfcoverpage_settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """  """
    avail = db.Column(db.Text, nullable=False, default="disable")
    """  """

    header_display = db.Column(db.Text, nullable=True, default='')
    """ Default display number of search results"""

    header_output_string = db.Column(db.Text, nullable=True, default='')
    """ Default display sort of index search"""

    header_output_image = db.Column(db.Text, nullable=True, default="string")
    """ Default display sort of keyword search"""

    header_display_position = db.Column(db.Text, nullable=True, default='center')
    """ Default display sort of keyword search"""

    # def __init__(self, avail, header_display, header_output_string, header_output_image, header_display_position):
    #     self.avail = avail
    #     self.header_display = header_display
    #     self.header_output_string = header_output_string
    #     self.header_output_image = header_output_image
    #     self.header_display_position = header_display_position

class StringHeaderForm(FlaskForm):
    pass
    #string = StringField('')

class ImageHeaderForm(FlaskForm):
    pass
    #image = FileField(validators=[FileRequired()])
