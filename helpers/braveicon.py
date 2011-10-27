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

import sys
from BeautifulSoup import BeautifulSoup
import requests


def get_favicon(url):
	"""Fetches a site's favicon URL. Respects link rel="" declarations
most importantly, per W3C spec, however, it favors 'shortcut icon'
over /favicon.ico, as many software packages explicitly declare
via shortcut icon, and W3C snubs /favicon.ico, generally speaking."""

	if url.endswith("/"):
		url = url[0:len(url)-1]

	html = requests.get(url).content
	soup = BeautifulSoup(html)
	head = soup.html.head

	head_links = head.findAll('link')
	for link in head_links:
		sys.stderr.write(url + str(link) + link['rel'] + '\n')

		if link['rel'] == 'icon' or link['rel'] == 'shortcut icon':
			if requests.head(url).ok:
				return link['href']
			else:
				if link['href'].startswith("//"):
					link['href'] = url + link['href'][2:len(link['href'])]
				if link['href'].startswith("/"):
					link['href'] = url + link['href'][1:len(link['href'])]
				absolute_url = "http://%s/%s" % (url, link['href'])
				if requests.head(absolute_url).ok:
					return absolute_url

	url = "%s/favicon.ico" % url
	if requests.head(url).ok:
		return url

	return false
