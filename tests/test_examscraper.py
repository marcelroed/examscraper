from examscraper.__main__ import main
from examscraper.classify_text import _classify_class
from examscraper.configure import read_configuration
from examscraper.scraper import Scraper

arguments = ["test_configuration.json"]


class TestConfigure:
    def test_configure(self):
        configuration = read_configuration(arguments)
        assert configuration['jobs']['termisk']['fileType'] == 'pdf'


class TestScraper:
    def test_gather_exams(self):
        configuration = read_configuration(arguments)
        job = configuration['jobs']['termisk']
        scraper = Scraper(job['startUrl'])
        docs = scraper.find_urls('.' + job['fileType'])
        scraper.close()
        assert docs[0]['linkText'] == 'E-TFY4165-09aug2018'


class TestClassify:
    def test_classify_class(self):
        fragment = {
            "classes":
                {
                    "1": ["1"],
                    "2": ["2"]
                },
            "default": "UNDEFINED"
        }
        empty_names = [""]
        missing_text = "399479894879849387304985"
        contains_2 = "94385938475987987293847923874"
        more_1s_than_2s = "598794875911948598741394872293485211"
        equal_1s_and_2s = "4598649876111349875394857222"

        # Test standard cases
        assert _classify_class(fragment, missing_text, empty_names) == "UNDEFINED"
        assert _classify_class(fragment, contains_2, empty_names) == "2"
        assert _classify_class(fragment, more_1s_than_2s, empty_names) == "1"
        # Indeterminate if two are as likely
        assert _classify_class(fragment, equal_1s_and_2s, empty_names) == "UNDEFINED"

        # Test prioritization of names
        names = ["test", "1"]
        conflicting_names = ["test", "11", "2"]
        names_with_additional = ["test", "additionalWord", "argh", "foo"]
        fragment['prioritizeNames'] = True
        assert _classify_class(fragment, contains_2, names) == "1"
        # Don't use names when they conflict
        assert _classify_class(fragment, contains_2, conflicting_names) == "2"
        # Additional words for classes
        fragment['nameAdditions'] = {"ADD": ["additionalWord"]}
        assert _classify_class(fragment, contains_2, names_with_additional) == "ADD"

    def test_classify_range(self):
        pass


class TestExamscraper:
    def test_gather_exams(self):
        main(arguments)
