import sys

from examscraper.classify_text import generate_name
from examscraper.configure import read_configuration
from examscraper.extract_text import extract
from examscraper.scraper import Scraper
from examscraper.write import write_binary

vprint = None


def main(argv=sys.argv[1:]):
    # Read config file
    config = read_configuration(argv)
    verbose = True
    global vprint
    vprint = print if verbose else lambda *a, **k: None
    print("Read config!")
    for name, job in config['jobs'].items():
        print("Executing job '{}'".format(name))
        scraper = Scraper(job['startUrl'])
        scraper.find_urls('.' + job['fileType'])
        matches = scraper.read()
        scraper.close()
        vprint(list(map(lambda match: (match['linkText']), matches)))
        for match in matches:
            text = extract(match['data'], job['fileType'])
            filename = generate_name(job['naming'], text=text, names=[
                match['linkText'], match['filename']])
            vprint('Classified {} as {}.'.format(match['linkText'], filename))
            write_binary(job['destinationDir'], filename + '.pdf', match['data'], overwrite=False)


# def lectures():
#     directory = 'M:/OneDrive - NTNU/Subjects/20 Termisk fysikk/lectures/'
#     starturl = "http://folk.ntnu.no/martifja/"
#     scraper = Scraper(starturl)
#     scraper.add_filters([lambda x: "uke" in x['filename'].lower()])
#     scraper.find_urls('.pdf')
#     files = scraper.read()
#     print(len(files))
#     for file in files:
#         filename = file['filename']
#         write_binary(directory, filename, file['data'])

if __name__ == "__main__":
    main(sys.argv[1:])
