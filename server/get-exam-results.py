#!/usr/bin/env python
# coding: utf-8
# There are Python 2.x at the Server side

import sys
import pymongo
from bson.son import SON


conn = pymongo.Connection('localhost', 27017)
db = conn['rts']
coll = db['exams']


exam = sys.argv[1]
attempts = sys.argv[2]

# Default number of attempts
pipe = [
        {'$match': { '$or': [{'name': exam}, {'name': exam+'2'}, {'name': exam+'3'}, {'name': exam+'4'}, {'name': exam+'5'}]}},
        {'$sort': {'name': 1}},
        {'$project': { '_id':0, 'owner_id':1, 'name': 1, 'qs_points':1 } },
        {'$unwind': '$qs_points'},
        {'$group': {'_id': {'owner_id': '$owner_id'}, 'name': {'$first': '$name' }, 'number': {'$push': "$qs_points"}}}
        ]


if attempts == '5':
        print u'{0};{1};{2};{3};{4};{5};{6}'.format('Name', 'att_1', 'att_2', 'att_3', 'att_4', 'att_5', 'MAX')
if attempts == '4':
        print u'{0};{1};{2};{3};{4};{5}'.format('Name', 'att_1', 'att_2', 'att_3', 'att_4', 'MAX')
if attempts == '3':
        print u'{0};{1};{2};{3};{4}'.format('Name', 'att_1', 'att_2', 'att_3', 'MAX')


query = coll.aggregate(pipeline=pipe)

for req in query['result']:
        s1 = s2 = s3 = s4 = s5 = 0
        t = 0
        for i in req['number']:
                if t < 25:
                        s1 = s1 + i
                if (t > 24 and t < 50):
                        s2 = s2 + i
                if (t > 49 and t < 75):
                        s3 = s3 + i
                if attempts == 4:
                        if (t > 74 and t < 100):
                                s4 = s4 + i
                if attempts == 5:
                        if (t > 99 and t < 125):
                                s5 = s5 + i
                t = t + 1
        if attempts == '5':
                print u'{0};{1};{2};{3};{4};{5};{6}'.format(req['_id']['owner_id'], s1, s2, s3, s4, s5, max(s1,s2,s3,s4,s5))
        if attempts == '4':
                print u'{0};{1};{2};{3};{4};{5}'.format(req['_id']['owner_id'], s1, s2, s3, s4, max(s1,s2,s3,s4))
        if attempts == '3':
                print u'{0};{1};{2};{3};{4}'.format(req['_id']['owner_id'], s1, s2, s3, max(s1,s2,s3))
