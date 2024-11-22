import io
import csv

import openpyxl
from rest_framework import renderers

COMMENTS_DATA_FILE_HEADERS = ['id', 'email','created','comment', 'car', 'about_car']


class CSVCommentsRenderer(renderers.BaseRenderer):
    media_type = "text/csv"
    format = "csv"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        csv_buffer = io.StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=COMMENTS_DATA_FILE_HEADERS, extrasaction="ignore")
        csv_writer.writeheader()

        for comments_data in data:
            csv_writer.writerow(comments_data)

        return csv_buffer.getvalue()


class ExcelCommentsRenderer(renderers.BaseRenderer):

    media_type = "application/vnd.ms-excel"
    format = "xls"

    def render(self, data, accepted_media_type=None, renderer_context=None):

        workbook = openpyxl.Workbook()
        buffer = io.BytesIO()
        worksheet = workbook.active
        worksheet.append(COMMENTS_DATA_FILE_HEADERS)

        for comments_data in data:
            worksheet.append(list(comments_data.values()))

        workbook.save(buffer)

        return buffer.getvalue()
