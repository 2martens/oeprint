"""merge.py: Provides functionality to merge PDF files"""

__author__ = 'Jim Martens'

from server.pypdf2.PyPDF2 import PdfFileReader, PdfFileMerger


def merge_pdf_files(name, files):
    merger = PdfFileMerger()
    for file in files:
        merger.append(PdfFileReader(file['path']))

    merger.write(name)
