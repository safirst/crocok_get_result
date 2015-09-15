#!/usr/bin/env python
# coding: utf-8
#
# Server-side component for crocok_get_results


import sys
import pymongo
from bson.son import SON


conn = pymongo.Connection('localhost', 27017)

db = conn['rts']

coll = db['exams']

pipe = [
        {'$project': { '_id':0, 'owner_name': 1, 'owner_id':1, 'name': 1, 'qs_points':1 } },
        {'$unwind': '$qs_points'},
        {'$match': {'name': sys.argv[1]}},
        {'$group': {'_id': {'owner_id': '$owner_id', 'owner_name': '$owner_name'}, 'number': {'$sum': "$qs_points"}}}
]


query = coll.aggregate(pipeline=pipe)

for req in query['result']:
        owner_name = req['_id']['owner_name']
        owner_id = req['_id']['owner_id']
        right_answers = req['number']
        print u'{0};{1};{2}'.format(owner_id, owner_name, right_answers)
