from scraper import Scraper
from write import write_binary
from pdfkeywords import classify_exam

def main():
    directory = 'M:/OneDrive - NTNU/Subjects/20 Termisk fysikk/exams/'
    starturl = "https://www.ntnu.no/web/fysikk/eksamen/-/asset_publisher/mQ9ArUokS3mD/content/tfy4165-termisk-fysikk"
    scraper = Scraper(starturl)
    scraper.find_urls('.pdf')
    exams = scraper.read()
    print(len(exams))
    print(list(map(lambda exam: (exam['text']), exams)))
    for exam in exams:
        filename = classify_exam(data=exam['data'], names=[exam['text'], exam['filename']], binary=True)
        print('Classified {} as {}.'.format(exam['text'], filename))
        write_binary(directory, filename+'.pdf', exam['data'], overwrite=False)

def lectures():
    directory = 'M:/OneDrive - NTNU/Subjects/20 Termisk fysikk/lectures/'
    starturl = "http://folk.ntnu.no/martifja/"
    scraper = Scraper(starturl)
    scraper.add_filters([lambda x: "uke" in x['filename'].lower()])
    scraper.find_urls('.pdf')
    files = scraper.read()
    print(len(files))
    for file in files:
        filename = file['filename']
        write_binary(directory, filename, file['data'])

if __name__ == '__main__':
    #main()
    lectures()
