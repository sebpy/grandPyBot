#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.views import Answer
import json
import requests


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
