#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.views import Answer
import json
import requests


def test_requests_response(monkeypatch):

    results_map = '{"candidates": [{"formatted_address": "25460 Étupes, France", "geometry": {"location": ' \
                    '{"lat": 47.5070089, "lng": 6.862954}, "viewport": {"northeast": {"lat": 47.523487, ' \
                    '"lng": 6.903804999999999}, "southwest": {"lat": 47.487703, "lng": 6.843596}}}, "name": ' \
                    '"Étupes", "place_id": "ChIJD4VFuMUZkkcRUvQHEm8Z1Z4"}], "status": "OK"}'

    def mockreturn():
        return results_map

    monkeypatch.setattr(requests, 'get', mockreturn)

    bot_answer = Answer("etupes")

    assert bot_answer.answer_map == json.load(results_map)


def test_open_files():
    with open('app/swords.json') as sw:
        assert sw


def test_parse_text():
    bot_answer = Answer("Salut GrandPy! est ce que tu connais l'adresse d'Openclassrooms ?")
    assert bot_answer.message_parsed == "adresse openclassrooms"


def test_get_coordonates():
    bot_answer = Answer("Etupes")
    assert bot_answer.maps_answer == 200
    assert bot_answer.answer_map['candidates'][0]['geometry']['location']['lat'] == 47.5070089
    assert bot_answer.answer_map['candidates'][0]['geometry']['location']['lng'] == 6.862954


def test_wiki_infos():
    bot_answer = Answer("Etupes")
    assert bot_answer.wiki_answer != "Not found"
    assert bot_answer.wiki_answer == "Étupes est une commune française située dans le département du Doubs, en région Bourgogne-Franche-Comté.\n" \
                                     "Ses habitants sont appelés les Erbatons et Erbatonnes du patois, en Franc-comtois, Lai Herbatons : agneaux " \
                                     "nés en automne, ayant passé l'hiver à l'étable, découvrant avec étonnement le monde du printemps."


def test_wiki_error():
    bot_answer = Answer("Asqdfg")
    assert bot_answer.wiki_answer == "Ah bizarre, je ne sais rien à ce sujet..."
