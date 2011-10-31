#!/usr/bin/env python
# -*- coding: utf-8 -*-

# braveicon – retrieves web page favicons
# Copyright (C) 2011  Barry Melton  <http://sympodial.com/>
# Copyright (C) 2011  Nils Dagsson Moskopp  <nils@dieweltistgarnichtso.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from werkzeug.contrib.cache import SimpleCache
from html5lib.html5parser import HTMLParser
from base64 import b64encode

import requests

url_cache = SimpleCache(3600)

def get_favicon(page_url, use_data_uri=False):
	"""Fetches a site's favicon URL. Respects link rel="" declarations
most importantly, per W3C spec, however, it favors 'shortcut icon'
over /favicon.ico, as many software packages explicitly declare
via shortcut icon, and W3C snubs /favicon.ico, generally speaking."""
	def create_data_uri(url):
		data = requests.get(url).content
		return 'data:image/png;base64,' + b64encode(data)

	def cache_url(key, value):
		if use_data_uri:
			value = create_data_uri(value)
		url_cache.set(key, value)

	if page_url.endswith("/"):
		page_url = page_url[0:len(page_url)-1]

	cached_url = url_cache.get(page_url)
	if cached_url:
		return cached_url

	html = requests.get(page_url).content

	p = HTMLParser()
	tree = p.parse(html)
	links = [e for e in tree if (e.name == 'link')]

	for link in links:
		attributes = link.attributes

		if attributes['rel'] == 'icon' or attributes['rel'] == 'shortcut icon':
			if attributes['href'].startswith("http"):
				favicon_url = attributes['href']
			if attributes['href'].startswith("//"):
				favicon_url = "%s/%s" % \
					(page_url, attributes['href'][2:len(attributes['href'])])
			if attributes['href'].startswith("/"):
				favicon_url = "%s/%s" % \
					(page_url, attributes['href'][1:len(attributes['href'])])

			if requests.head(favicon_url).ok:
				cache_url(page_url, favicon_url)
				return create_data_uri(favicon_url)

	favicon_url = "%s/favicon.ico" % page_url
	if requests.head(favicon_url).ok:
		cache_url(page_url, favicon_url)
		return create_data_uri(favicon_url)

	return False
