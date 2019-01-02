import unittest
import examscraper.pipeline as pipeline
class TestTermisk(unittest.TestCase):
    def setUp(self):
        self.nice = True
        pipeline.main()

    def test_1(self):
        self.assertTrue(self.nice)

if __name__ == '__main__':
    unittest.main()
