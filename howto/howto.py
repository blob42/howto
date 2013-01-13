#!/usr/bin/env python


import argparse
from stackexchange import *
from pyquery import PyQuery as pq
import sys


class NoResult(Exception):
    pass

class SOSearch(Site):
    def __init__(self, qs, tags=None, **kw):
        self.qs = qs
        self.tags = '' if tags == None else tags
        self.domain = 'api.stackoverflow.com'
        super(SOSearch, self).__init__(self.domain, **kw)
        self.qs = self.search(order=DESC, sort='votes', tagged=self.tags,
                    intitle=self.qs, filter='!-u2CTCMX')
        if self.qs.total == 0:
            raise NoResult

    def first_q(self):
        self._populate_one_question(self.qs[0])
        return self.qs[0]

    def has_code(self, answer):
        return '<code>' in answer.body

    def _find_best_answer(self, question):
        if hasattr(question, 'is_accepted_id'):
            for a in question.answers:
                if not self.has_code(a):
                    continue
                if a.id == question.is_accepted_id:
                    question.best_answer = a
        else:
            for a in question.answers:
                if self.has_code(a):
                    question.best_answer = question.answers[0]
                else:
                    continue


    def _order_answers(self, qs):
        ordered = sorted(qs.answers, key=lambda a: a.score, reverse=True)
        qs.answers = ordered

    def _populate_one_question(self, qs):
        qs.fetch()
        qs.answers = self.answers([a.id for a in qs.answers], order=DESC, body='true')
        for a in qs.answers:
            html = pq(a.body)
            el = html('code')
            a.code = el.text()
        self._order_answers(qs)
        self._find_best_answer(qs)





def main(args):
    """docstring for main"""
    try:
        args.query = ' '.join(args.query).replace('?', '')
        so = SOSearch(args.query, args.tags)
        result =  so.first_q().best_answer.code
        if result != None:
            print result
        else:
            print("Sorry I can't find your answer, try adding tags")
    except NoResult, e:
        print("Sorry I can't find your answer, try adding tags")


def cli_run():
    """docstring for argparse"""
    parser = argparse.ArgumentParser(description='Stupidly simple code answers from StackOverflow')
    parser.add_argument('query', help="What's the problem ?", type=str, nargs='+')
    parser.add_argument('-t','--tags', help='semicolon separated tags -> python;lambda')
    args = parser.parse_args()
    main(args)



if __name__ == '__main__':
    cli_run()
