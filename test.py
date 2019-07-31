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
                    '"Étupes", "place_id": "ChIJD4VFuMUZkkcRUvQHEm8Z1Z4"}], "status": "OK"}'

    results_wiki = '{"batchcomplete": "", "continue": {"gsroffset": 1, "continue": "gsroffset||"}, "warnings": ' \
                   '{"extracts": {"*": "\'exlimit\' was too large for a whole article extracts request, lowered to 1."}}, ' \
                   '"query": {"pageids": ["3990173"], "pages": {"3990173": {"pageid": 3990173, "ns": 0, ' \
                   '"title": "Club cycliste Étupes", "index": 1, "extract": "Le Club cycliste d\'Étupes (' \
                   'CC Étupes) est un club de cyclisme basé à Étupes, dans le département du Doubs en France. ' \
                   'Il a été fondé en 1974 par Robert Orioli et fait partie de la Division nationale 1 de la ' \
                   'Fédération française de cyclisme en cyclisme sur route. Il a remporté sept fois la coupe de ' \
                   'France des clubs de la FFC : en 1996, 1997, 1998, 1999, 2003, 2004 et 2009. Ses coureurs ' \
                   'Ludovic Turpin et Nicolas André ont été champions de France amateurs, ' \
                   'respectivement en 1999 et 2001."}}}}'

    def mockreturn(api_url, params):
        response = ""
        if api_url == 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json':
            response = MockRequestsResponse(results_map)
        if api_url == 'https://fr.wikipedia.org/w/api.php':
            response = MockRequestsResponse(results_wiki)

        return response

    monkeypatch.setattr(requests, 'get', mockreturn)

    bot_answer = Answer("etupes")

    assert bot_answer.answer_map == json.load(results_map)
    assert bot_answer.answer_map == json.load(results_wiki)
