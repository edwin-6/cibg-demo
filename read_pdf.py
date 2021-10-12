# pip install PyPDF2
# pip install pdfminer.six
import os
import PyPDF2
from pdfminer.high_level import extract_text
from more_itertools import windowed

input_dir = 'pdf'

for file in os.listdir(input_dir):
    pdf_file = os.path.join(input_dir, file)

    # example with PyPDF2
    reader = PyPDF2.PdfFileReader(pdf_file)
    print(f"numPages: {reader.numPages} documentInfo: {reader.documentInfo}")
    print(repr(reader.getPage(0).extractText()))
    print()

    # example with pdfminer.six
    text = extract_text(pdf_file)

    part_size = 2000  # 60000
    overlap = 200  # 500
    step_size = part_size - overlap
    offset = 0

    for sliding_text in map("".join, windowed(text, n=part_size, step=step_size, fillvalue='')):
        print(offset, repr(sliding_text))
        offset += step_size
    print()
