import json
import concurrent.futures
import boto3

def merge_sorted_lists(list1, list2):
    merged_list = []
    i, j = 0, 0

    # Iterate through both lists and append the smaller element to the merged list
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    # If there are remaining elements in list1, append them
    while i < len(list1):
        merged_list.append(list1[i])
        i += 1

    # If there are remaining elements in list2, append them
    while j < len(list2):
        merged_list.append(list2[j])
        j += 1

    return merged_list


def get_functions_to_call(lang_list, collection_list):
    with open('hadith_map.json', 'r') as infile:
        hadith_map = json.load(infile)

    filtered_list = []
    for key, value_list in hadith_map.items():
        if any(value.startswith(lang) and value.endswith(collection) for value in value_list for lang in lang_list for collection in collection_list):
            filtered_list.append(key)
    return filtered_list


def invoke_lambda(client, function_name, query, lang, collection):
    from simplify_arabic import simplify_arabic_text
    query = simplify_arabic_text(query)

    response = client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Synchronous invocation
        Payload=json.dumps({'query': query, 'lang': lang, 'collection': collection})
    )
    response_payload = json.loads(response['Payload'].read())
    return {
        'function': function_name,
        'response': response_payload
    }


def lambda_handler(event, context):
    print(event)
    client = boto3.client('lambda')

    query_params = event.get('queryStringParameters', {})
    # if(query_params.get('type') == 'search'):
    return search(query_params, client)
    # elif(query_params.get('type') == 'random'):
    #     return random(query_params, all_function_names, client)

def search(query_params, client):
    lang = query_params.get('language_code')
    if not lang or lang == '':
        lang_list = ['']
    else:
        lang_list = lang.strip(' ,').split(',')

    collection = query_params.get('collection')
    if not collection or collection == '':
        collection_list = ['']
    else:
        collection_list = collection.strip(' ,').split(',')

    function_names = get_functions_to_call(lang_list, collection_list)
    # The query parameter from the input event
    if function_names == []:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Check lang or collections parameters.'
            })
        }
    query = query_params.get('query')

    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing query parameter in the input.'
            })
        }

    results = []
    failed_invocations = []

    # Use ThreadPoolExecutor to manage concurrent threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_function = {
            executor.submit(invoke_lambda, client, function_name, query, lang, collection): function_name
            for function_name in function_names
        }

        for future in concurrent.futures.as_completed(future_to_function):
            function_name = future_to_function[future]
            try:
                result: dict[str, tuple] = future.result()
                # results = list(heapq.merge(results, result["response"], key=lambda x: x[9]))
                results = results + result["response"]
                # results = list(heapq.merge(results, result, key=lambda x: x[8]))
                # results.append(result)
            except Exception as e:
                failed_invocations.append({
                    'function': function_name,
                    'error': str(e)
                })
    return sorted(results, key=lambda x: x[9])

# def random(query_params, all_function_names, client):
#     length = 99999
#     queryParam = query_params.get("l")
#     if (not(queryParam is None or queryParam == '')):
#         length = int(queryParam)
#     cursor = conn.execute(randomQuery(length))
#     data = cursor.fetchall()
#     return data

if __name__ == '__main__':
    print(lambda_handler({
        "queryStringParameters": {
            "query": "Allah",
            "language_code": ",ind",
            "collection": ","
        }
    }, None))