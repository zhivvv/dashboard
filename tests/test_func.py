from unittest import TestCase
import func


class TestMatchingProcess(TestCase):

    def setUp(self) -> None:
        self.choices = ['aaa', 'bbb', 'ccc']
        self.Matching = func.MatchingProcess(self.choices)

    def test_single_match(self):
        # query = 'aaa'
        # res = self.Matching.single_match(query)
        # self.assertEqual(res, "aaa")

        # query = 'aab'
        # res = self.Matching.single_match(query)[1]
        # self.assertEqual(res, "aaa")

        query = 'abb'
        res = self.Matching.single_match(query)
        self.assertEqual(res, "bbb")



    def test_sequence_match(self):
        query = ['a', 'b', 'c']
        res = self.Matching.sequence_match(query)
        self.assertEqual(res, self.choices)