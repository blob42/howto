import unittest
from stackexchange import StackOverflow
import stackexchange
from pyquery import PyQuery as pq
from howto.howto import SOSearch
from random import choice


class SOSearchTests(unittest.TestCase):
    '''Test case for Stackoverflow searches'''

    def setUp(self):
        self.so_search = SOSearch('singleton pattern', 'java')

    def test_issubclass_of_stackexchangeSite(self):
        self.assertIsInstance(self.so_search, stackexchange.Site)

    def test_init_values(self):
        with self.assertRaises(Exception):
            so = SOSearch()

    def test_fist_question(self):
        first = self.so_search.first_q()
        self.assertEqual(first, self.so_search.qs[0])

    def test_questions_ordered_by_votes(self):
        for (qs, next) in zip(self.so_search.qs[:-2], self.so_search.qs[1:]):
            self.assertGreaterEqual(qs.score,
                             next.score)

    def test_extracted_code(self):
        question = self.so_search.first_q()
        answer = choice(question.answers)
        html = pq(answer.body)
        el = html('code')
        code = el.text()
        self.assertEqual(code, answer.code)

    def test_has_code(self):
        q = self.so_search.first_q()
        a = choice(q.answers)
        a.body = 'This is a test<code>Magic</code>'
        self.assertEqual(self.so_search.has_code(a), True)
        a.body = 'This is a test'
        self.assertEqual(self.so_search.has_code(a), False)

    def test_best_answer(self):
        question = self.so_search.first_q()
        best = question.best_answer
        for answer in question.answers:
            self.assertGreaterEqual(best.score, answer.score)


    def test_get_next_answer(self):
        self.failUnless(False)


def main():
    """docstring for main"""
    unittest.main()

if __name__ == '__main__':
    main()
