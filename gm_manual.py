import http.client
import urllib.parse
import json

class ManualIndex:
	def __init__(self):
		self.map = {}
	def load():
		conn = http.client.HTTPConnection('docs.yoyogames.com')
		conn.request('GET', '/files/helpindexdat.js')
		res = conn.getresponse()
		if res.status != 200:
			return {}

		# Skip JS parts of the file (resulting parts should contain only valid JSON).
		index_text = res.read()[16:-3].decode("utf-8")
		index_obj = json.loads(index_text)

		yyg_docs = 'http://docs.yoyogames.com/'
		index_list = ManualIndex()
		for index_pair in index_obj:
			if not isinstance(index_pair[1], list):
				# Scalar value. Value contains single URL.
				url = yyg_docs + urllib.parse.quote(index_pair[1])
				index_list.insert(index_pair[0], url)
			else:
				# Value contains multiple URL possibilities.
				for possible_pair in index_pair[1]:
					url = yyg_docs + urllib.parse.quote(possible_pair[1])
					index_list.insert(index_pair[0], url, possible_pair[0])

		return index_list
	def find(self, keyword, index = 0):
		if keyword in self.map:
			max_index = str(len(self.map[keyword]))
			if index >= len(self.map[keyword]):
				return "End of list (max {}).".format(max_index)
			val = self.map[keyword][index]
			return  "\x02{}\x02: {} ({} of {})".format(val[0], val[1], str(index + 1), max_index)
		return "Not found"
	def insert(self, keyword, url, description = "Result"):
		if keyword in self.map:
			self.map[keyword].append((description, url))
		else:
			self.map[keyword] = [(description, url)]
