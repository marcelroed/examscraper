from examscraper.__main__ import main
from examscraper.classify_text import _classify_class
from examscraper.classify_text import _classify_range
from examscraper.configure import read_configuration
from examscraper.scraper import Scraper

arguments = ['test_configuration.json']


class TestConfigure:
    def test_configure(self):
        configuration = read_configuration(arguments)
        assert configuration['jobs']['termisk']['fileType'] == 'pdf'
        # Test special character
        assert configuration['jobs']['termisk']['naming']['season']['classes']['V'][6] == 'vår'


class TestClassify:
    def test_classify_class(self):
        fragment = {
            'classes':
                {
                    '1': ['1'],
                    '2': ['2']
                },
            'default': 'UNDEFINED'
        }
        empty_names = ['']
        missing_text = '399479894879849387304985'
        contains_2 = '94385938475987987293847923874'
        more_1s_than_2s = '598794875911948598741394872293485211'
        equal_1s_and_2s = '4598649876111349875394857222'

        # Test standard cases
        assert _classify_class(fragment, missing_text, empty_names) == 'UNDEFINED'
        assert _classify_class(fragment, contains_2, empty_names) == '2'
        assert _classify_class(fragment, more_1s_than_2s, empty_names) == '1'
        # Indeterminate if two are as likely
        assert _classify_class(fragment, equal_1s_and_2s, empty_names) == 'UNDEFINED'

        # Test prioritization of names
        names = ['test', '1']
        conflicting_names = ['test', '11', '2']
        names_with_additional = ['test', 'additionalWord', 'argh', 'foo']
        fragment['prioritizeNames'] = True
        assert _classify_class(fragment, contains_2, names) == '1'
        # Don't use names when they conflict
        assert _classify_class(fragment, contains_2, conflicting_names) == '2'
        # Additional words for classes
        fragment['nameAdditions'] = {'ADD': ['additionalWord']}
        assert _classify_class(fragment, contains_2, names_with_additional) == 'ADD'

    def test_classify_range(self):
        fragment = {
            'min': 45,
            'max': 50,
            'default': '.XX',
            'prioritizeNames': True
        }
        # First with no names
        names = ['']
        text = 'as49dl46kj50als46kjdlqwej6634344750'
        assert _classify_range(fragment, text, names) == '46'
        # Now with names
        names = ['Eksamen 1949']
        assert _classify_range(fragment, text, names) == '49'
        # Use that failed
        failed_names = ['E-TFY4165-20aug2011', '5e86a46d-1d54-4df7-9393-2f4ba1519955']
        failed_text = 'ASDLKASLKSDKJLASKaskldjasldkjasASLjaslasASLkasdALKSjda'
        fragment = {
            'min': 1990,
            'max': 2019,
            "prioritizeNames": True,
            "default": ".XXXX"
        }
        # assert _classify_range(fragment, failed_text, failed_names) == '2011'


class TestScraper:
    def test_gather_exams(self):
        configuration = read_configuration(arguments)
        job = configuration['jobs']['termisk']
        scraper = Scraper(job['startUrl'])
        docs = scraper.find_urls('.' + job['fileType'])
        scraper.close()
        assert docs[0]['linkText'] == 'E-TFY4165-09aug2018'


class TestExamscraper:
    def test_gather_exams(self):
        main(arguments)
