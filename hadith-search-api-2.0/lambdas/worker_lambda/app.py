import re
from query import *

def removeSpecialChars(query_param):
    query_param = re.sub(
        r'[\u0000-\u002F \u003A-\u0040 \u005B-\u0060 \u007B-\u007F]', ' ', query_param)
    query_param = query_param.strip()
    query_param = re.sub(r'[ ]+', ' OR ', query_param)
    return query_param

def searchData(query_param):
    if not query_param:
        return {'statusCode': 400, 'body': 'Invalid search word'}
    return searchQueryData(removeSpecialChars(query_param))


def lambda_handler(event, context):
    return searchData(event.get('query'))

if __name__ == '__main__':
    print(lambda_handler({"type": "search","query": "الرحمن"}, None))
