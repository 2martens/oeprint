"""merge.py: Provides functionality to merge PDF files"""
import itertools

from tool.pypdf2.PyPDF2 import PdfFileReader, PdfFileMerger

__author__ = 'Jim Martens'


def merge_pdf_files(filename, merge_data):
    merger = PdfFileMerger()
    for merge_info in merge_data:
        material = merge_info['material']
        page_ranges = None # type: list
        add_empty_page = False
        pdf_file = PdfFileReader(material['filename'])
        if 'pages' in material:
            pages = material['pages']
            page_ranges = list(determine_ranges(pages))
            if len(pages) % 2 != 0:
                add_empty_page = True
        else:
            if pdf_file.getNumPages() % 2 != 0:
                # the pdf file has an odd number of pages
                add_empty_page = True

        for x in range(merge_info['amount']):  # print material x amount of times
            if page_ranges is not None:
                for start, stop in page_ranges:
                    merger.append(pdf_file, pages=(start - 1, stop - 1))
            else:
                merger.append(pdf_file)

            if add_empty_page:
                merger.append('build/emptypage.pdf')

    merger.write(filename)


def determine_ranges(source: list):
    """
    Determines the existing ranges in the list of pages.
    :param source:
    :type source: list
    """
    for a, b in itertools.groupby(enumerate(source), lambda x: x[1] - x[0]):
        b = list(b)
        yield b[0][1], b[-1][1]
