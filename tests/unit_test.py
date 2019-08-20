#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.views import Answer
from app.views import app
import json
import requests
import pytest


class MockRequestsResponse:
    def __init__(self, resp):
        self.text = resp
        self.url = "mock_url"


def test_requests_response(monkeypatch):

    results_map = '{"candidates": [{"formatted_address": "25460 Étupes, France", "geometry": {"location": ' \
                  '{"lat": 47.5070089, "lng": 6.862954}, "viewport": {"northeast": {"lat": 47.523487, ' \
                  '"lng": 6.903804999999999}, "southwest": {"lat": 47.487703, "lng": 6.843596}}}, "name": ' \
                  '"Étupes","place_id": "ChIJD4VFuMUZkkcRUvQHEm8Z1Z4"}], "status": "OK"}'

    results_wiki = '{"batchcomplete": "","continue": {"continue": "gsroffset||", "gsroffset": 1},"query": ' \
                   '{"pageids": ["399400"],"pages": {"399400": {"extract": "Étupes est une commune française' \
                   ' située dans le département du Doubs, en région Bourgogne-Franche-Comté.Ses habitants sont ' \
                   'appelés les Erbatons et Erbatonnes du patois, en Franc-comtois, Lai Herbatons : agneaux nés ' \
                   'en automne, ayant passé l\'hiver à l\'étable, découvrant avec étonnement le monde du printemps.", ' \
                   '"index": 1, "ns": 0, "pageid": 399400, "title": "Étupes"}}}}'

    def mockreturn(api_url, params):
        response = ""
        if api_url == 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json':
            response = MockRequestsResponse(results_map)
        if api_url == 'https://fr.wikipedia.org/w/api.php':
            response = MockRequestsResponse(results_wiki)

        return response

    monkeypatch.setattr(requests, 'get', mockreturn)

    bot_answer = Answer("etupes")

    assert bot_answer.answer_map == json.loads(results_map)
    assert bot_answer.wiki_result_json == json.loads(results_wiki)


def test_open_files():
    with open('app/swords.json') as sw:
        assert sw


def test_open_bot_txt():
    with open('app/bot_text.txt') as txt:
        assert txt


def test_parse_text():
    bot_answer = Answer("Salut GrandPy! est ce que tu connais l'adresse d'Openclassrooms ?")
    assert bot_answer.message_parsed == "adresse openclassrooms"


def test_parse_special_char():
    bot_answer = Answer("#;l'adresse d'Openclassrooms ?!")
    assert bot_answer.message_parsed == "adresse openclassrooms"


def test_get_coordonates():
    bot_answer = Answer("Etupes")
    assert bot_answer.maps_answer['status'] == "OK"
    assert bot_answer.answer_map['candidates'][0]['geometry']['location']['lat'] == 47.5070089
    assert bot_answer.answer_map['candidates'][0]['geometry']['location']['lng'] == 6.862954


def test_get_coordonates_error():
    bot_answer = Answer("Asqdfg")
    assert bot_answer.answer_map == "error"


def test_wiki_infos():
    bot_answer = Answer("openclassrooms")
    assert bot_answer.answer_wiki != "Not found"
    split_answer_wiki = bot_answer.answer_wiki.split('<br>')[1]
    assert split_answer_wiki[:126] == "OpenClassrooms est une école en ligne qui propose à ses membres des cours certifiants et des parcours débouchant sur un métier"


def test_wiki_error():
    bot_answer = Answer("Asqdfg")
    assert bot_answer.answer_wiki == "error"


@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_home_page(client):

    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'GrandPy Bot' in html
    assert '<input' in html


def test_about_page(client):

    rsp = client.get('/about')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'A propos' in html
