#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module used for GrandPy Bot  """

import json
import os
import requests
import re
import wikipedia
from config import API_KEY_MAPS


class Answer:
    """ Class for grandPy bot """

    def __init__(self, user_msg):
        self.user_post = user_msg
        self.message_parsed = self.parse_text()
        self.maps_answer = 'Not found'
        self.answer_map = ''
        self.answer_wiki = 'Je n\'ai pas compris la demande ou je ne connais pas d\'histoire sur ce lieu.'
        self.name_place = 'Not found'
        self.address_place = 'Not found'
        self.lat = 47.5070089
        self.lon = 6.862954

        if self.message_parsed != "":
            self.maps_answer = self.get_maps()
            self.wiki_answer = self.get_wikipedia()

    def parse_text(self):
        """Get message entering by user"""
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/swords.json') as sw:
                swords = json.load(sw)
        except IOError as error:
            print('Error loading stopwords file : ' + str(error))
            swords = 'Error!'

        clean_swords = re.sub(r"[-,.;@#?!&$'()<>/]+ *", " ", self.user_post.lower(), )

        words_split = clean_swords.split()
        result_word = []

        for word in words_split:
            if word not in swords:
                result_word.append(word)
        text_parsed = ' '.join(result_word)

        return text_parsed

    def get_maps(self):
        """Gets the information from maps about the parsed text, then display the result in the map"""

        #search_coordonate = "https://maps.googleapis.com/maps/api/geocode/json?address=" + self.message_parsed +"&key=" + API_KEY_MAPS
        search_coordonate = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        datas = {
                   'language': 'fr',
                   'inputtype': 'textquery',
                   'locationbias': 'point:47.523487,6.903804999',
                   'input': self.message_parsed,
                   'type': 'street_address',
                   'fields': 'formatted_address,geometry,name,place_id',
                   'key': API_KEY_MAPS
                   }
        response = requests.get(search_coordonate, params=datas)
        result = json.loads(response.text)

        self.answer_map = result

        if result['status'] != "ZERO_RESULT":
            try:
                self.name_place = result['candidates'][0]['name']
                self.address_place = result['candidates'][0]['formatted_address']
                self.lat = result['candidates'][0]['geometry']['location']['lat']
                self.lon = result['candidates'][0]['geometry']['location']['lng']

            except IndexError:
                return 'No result'
            return 200
        else:
            return 'No result'

    def get_wikipedia(self):
        """ Get description of city
        https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&indexpageids=1&generator=search&gsrlimit=1&gsrsearch=ville%20etupes
        """

        wikipedia.set_lang("fr")
        try:
            self.answer_wiki = wikipedia.summary(self.message_parsed)
        except wikipedia.exceptions.PageError:
            self.answer_wiki = 'Not found'

        return self.answer_wiki
