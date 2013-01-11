from stackexchange import *
from pyquery import PyQuery as pq
import sys

if __name__ == '__main__':
    tag = sys.argv[2]
    query = sys.argv[1]
    so = StackOverflow()
    questions = so.search(order='desc', sort='votes', tagged=tag, intitle=query, filter='!-u2CTCMX')
    [q.fetch() for q in questions]

    answers = [answer for sublist in
            [answer_list for answer_list in
                [filter(lambda x: x.accepted, q.answers) for q in questions]
                ]
            for answer in sublist
            ]

    answers_wbody = so.answers([a.id for a in answers],order='desc',sort='votes', body='true', filter='!-u2CTCMX')
    answers_wbody = sorted(answers_wbody, key=lambda ans: ans.score, reverse=True)


    answers_wbody.reverse()
    for a in answers_wbody:
        html = pq(a.body)
        el = html('code')
        print el.text()
        print '================\n'

