import requests, xmltodict
from flask import jsonify, current_app


romeo_api_base_url = 'http://www.sherpa.ac.uk/romeo/api29.php'


def search_romeo_jtitles(query):
    """
    Searching for journals with the input query
    to get their Romeo info
    """

    payloads = {
        'jtitle': query,
        'qtype': 'contains'
          # Journal title search - Multiple Result
    }

    response = requests.get(
        romeo_api_base_url,
        params=payloads
    )

    response_body = response.text
    dict_result = xmltodict.parse(response_body, encoding='utf-8')
    return dict_result, jsonify(dict_result)


def search_romeo_issn(query):
    """
    Searching for one journal with the ISSN selected by the user
    to get the journal's Romeo info
    """

    # ISSN contained in the query
    payloads = {
        'issn': query  # ISSN search - Single Result
    }

    response = requests.get(
        romeo_api_base_url,
        params=payloads
    )

    response_body = response.text
    dict_result = xmltodict.parse(response_body, encoding='utf-8')
    return dict_result, jsonify(dict_result)


def search_romeo_jtitle(query):
    """
    Searching for journals with the input query
    to get their Romeo info
    """

    payloads = {
        'jtitle': query
    }

    response = requests.get(
        romeo_api_base_url,
        params=payloads
    )

    response_body = response.text
    dict_result = xmltodict.parse(response_body, encoding='utf-8')
    return dict_result, jsonify(dict_result)
