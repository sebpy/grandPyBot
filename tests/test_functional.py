#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test is ok

from splinter import Browser

URL = 'http://localhost:8080'


def test_app():
    bws = Browser()
    bws.visit(URL)
    assert bws.url
    bws.quit()
