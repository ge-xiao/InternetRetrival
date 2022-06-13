import json
from xml.dom.minidom import Document
import pandas as pd
from core import Query

import os

from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging

app = Flask(__name__)
CORS(app, supports_credentials=True)

documents = pd.read_csv('./data.csv')

@app.route('/boolQuery', methods=['GET'])
def bool_query():
    str = request.args.get("str")
    documents = pd.read_csv('./data.csv')

    query = Query(
        str,
        ignore_case=True,
        ignore_accent=False,
        match_word=False)
    # print(query)
    df1 = documents[documents.title.apply(query)]
    # print(df1)
    df2 = documents[documents.content.apply(query)]
    # print(df2)
    df = pd.concat([df1, df2])
    df.drop_duplicates(inplace=True)
    print(df)
    res=df.to_dict('records')
    return json.dumps(res)
    #df.to_csv('./data_retrival/boolean_search.csv')

@app.route('/zoneSpecificQuery', methods=['GET'])
def zone_specific_query():
    documents = pd.read_csv('./data.csv')

    title = request.args.get("title")
    author = request.args.get("author")
    dynasty = request.args.get("dynasty")
    content = request.args.get("content")
    df = documents
    if title != '':
        query_title = Query(
            title,
            ignore_case=True,
            ignore_accent=False,
            match_word=False
        )
        df1 = documents[documents.title.apply(query_title)]
        df = pd.merge(df, df1, how='inner')
    if content != '':
        query_content = Query(
            content,
            ignore_case=True,
            ignore_accent=False,
            match_word=False
        )
        df2 = documents[documents.content.apply(query_content)]
        df = pd.merge(df, df2, how='inner')
    if dynasty != '':
        query_dynasty = Query(
            dynasty,
            ignore_case=True,
            ignore_accent=False,
            match_word=False
        )
        df3 = documents[documents.dynasty.apply(query_dynasty)]
        df = pd.merge(df, df3, how='inner')
    if author != '':
        query_author = Query(
            author,
            ignore_case=True,
            ignore_accent=False,
            match_word=False
        )
        df4 = documents[documents.author.apply(query_author)]
        df = pd.merge(df, df4, how='inner')
    df.drop_duplicates(inplace=True)
    # df = df.drop(df[(df.author != author) | (df.dynasty != dynasty)].index)
    if author != '':
        df = df.drop(df[(df.author != author)].index)

    if dynasty != '':
        df = df.drop(df[(df.dynasty != dynasty)].index)

    res = df.to_dict('records')
    return json.dumps(res)
    #df.to_csv('/home/a3sh/data_retrival/zone_specific_query.csv')

@app.route('/fuzzySearch', methods=['GET'])
def fuzzy_search():
    documents = pd.read_csv('./data.csv')

    str = request.args.get("str")
    query = Query(
        str,
        ignore_case=True,
        ignore_accent=True,
        match_word=False)
    df1 = documents[documents.title.apply(query)]
    df2 = documents[documents.author.apply(query)]
    df3 = documents[documents.dynasty.apply(query)]
    df4 = documents[documents.content.apply(query)]
    df = pd.concat([df1, df2, df3, df4])
    df.drop_duplicates(inplace=True)
    res = df.to_dict('records')
    return json.dumps(res)
    #df.to_csv('/home/a3sh/data_retrival/fuzzy_search.csv')


@app.route('/dianzan', methods=['GET'])
def dianzan():
    index = request.args.get("index")
    index=int(index)
    doc = pd.read_csv('./data.csv')
    doc.loc[index, 'favor'] = doc.loc[index, 'favor'] + 1
    doc.to_csv('./data.csv',index=None)
    return {"data":"success"}

@app.route('/rankedsearch', methods=['GET'])
def rankedSearch():
    documents = pd.read_csv('./data.csv')
    authorCnt = pd.read_csv('./authorCnt.csv', index_col=0)
    documents.loc[:, 'score'] = 0
    for i in range(len(documents)):
        documents.loc[i,'score']=documents.loc[i,'favor']*(authorCnt.to_dict()['authorCnt'][documents.loc[i,'author']])/(len(documents))
    str = request.args.get("str")
    print(str)
    query = Query(
        str,
        ignore_case=True,
        ignore_accent=False,
        match_word=False)
    df1 = documents[documents.title.apply(query)]
    df2 = documents[documents.author.apply(query)]
    df3 = documents[documents.dynasty.apply(query)]
    df4 = documents[documents.content.apply(query)]
    df = pd.concat([df1, df2, df3, df4])
    df.drop_duplicates(inplace=True)
    df=df.sort_values(by="score",ascending=False)
    print(df)
    res = df.to_dict('records')
    return json.dumps(res)

if __name__ == '__main__':
    str = '("安定" OR "丁")'
    bool_query(str)


