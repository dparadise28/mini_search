import os, glob, ngram, zlib, json
from data_center.tools import utils

class Search:
	def __init__(self):
		#path to searchable files
		self.data_dir_pth = ['data_center', 'data',]
		#get base names of all data files
		self.docs = [os.path.basename(x) for x in glob.glob(utils.file_dir(['data_center', 'data', '*.jb']))]
		
		#load names into ngrams
		self.grams = ngram.NGram(key = lambda s: s.lower())
		for doc in self.docs: self.grams.add(doc)
		del self.docs
	
	# returns an ordered list of ngram dict
	def order_ngrams(self, ngram_dict={}):
		ordered_ngrams = []
		if ngram_dict:
			ordered_ngrams = sorted(ngram_dict.items(), key=lambda x: x[1], reverse=True)
		return ordered_ngrams

	def find_matches(self, text, offset, batch_size, threshold = 0.0):
		#better logic can stem from here but for now simple ngram threshold is the only criteria
		return self.order_ngrams(
			dict(self.grams.search(text, threshold = threshold))
		)[offset:offset+batch_size]
	
	def retrieve(self, text, offset = 0, batch_size = 100):
		ret = []
		for result in self.find_matches(text, offset, batch_size):
			with open(utils.file_dir(self.data_dir_pth + [result[0]]), "rb") as fdata:
				ret.append(json.loads(zlib.decompress(fdata.read()).decode())) #should be utf8
		return ret