#!/usr/bin/env python
# -*- coding: utf-8 -*-

from splinter import Browser

URL = 'http://localhost:5000'


def test_app():
    bws = Browser()
    bws.visit(URL)
    assert bws.url
    bws.quit()
