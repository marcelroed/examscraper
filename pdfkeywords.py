from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from io import BytesIO
import re

def convert_pdf_to_txt(data, binary = True):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = None
    if binary:
        fp = BytesIO(data)
    else:
        fp = data
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

# Names is a list of names that are appended to text of pdf. The first name is checked first, and used as a default file name if tests fail.
def classify_exam(data, names, binary=True, appendname=False):
    text = " ".join(names)+' '+convert_pdf_to_txt(data, binary)
    months = [('-1V', ['mai', 'juni', 'jun', 'may', 'june', 'spring', 'vår']),('-3H', ['november', 'desember', 'december', 'høst', 'fall', 'dec', 'des', 'nov']), ('-2K', ['august', 'aug', 'sommer', 'summer'])]
    years = '('+'|'.join(map(str, range(1990, 2020)))+')'
    year = month = solution = None
    done = False
    # Search titles for information
    for iteryear in range(1990, 2020):
        if done: break
        for itermonth in months:
            if re.search('(' + '|'.join(itermonth[1]) + ')'+str(iteryear), ' '.join(names), flags=re.IGNORECASE):
                year, month = str(iteryear), itermonth[0]
                done = True
                break
    if re.search('L-', names[0], flags=re.IGNORECASE):
        solution = True
    # Search the document for information.
    if year is None:
        yearcounts = [(count_matches(str(year), text), str(year)) for year in range(1990, 2020)]
        year = max(yearcounts, key=lambda yc: yc[0])[1]
    if month is None:
        monthcounts = [(count_matches('('+'|'.join(month[1])+')', text), month[0]) for month in months]
        month = max(monthcounts, key=lambda mc: mc[0])[1]

    if solution is None:
        solution = bool(re.search('(løsningsforslag|fasit)', text, flags=re.IGNORECASE))

    if year is not None:
        if month is not None:
            return year+month+'L'*solution+('('+names[0]+')')*appendname
        return year+'U'+'L'*solution+('('+names[0]+')')*appendname

    print("Couldn't classify {}.".format(names[0]))
    return names[0]

def count_matches(pattern, string):
    return len(re.findall(pattern, string, flags=re.IGNORECASE))

if __name__ == '__main__':
    fp = open('M:/OneDrive - NTNU/Subjects/15 Matte 4K/exams/verext.pdf', 'rb')
    print(classify_exam(fp, "Test exam", False))
