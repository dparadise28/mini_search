import requests, json, zlib, os

class Retriever:
	def __init__(self):
		#btr ways to do this but it works
		from data_center.tools import utils

		self.data_dir_pth = ['data_center', 'data',]
		self.platform_ids = [9, 21, 43] #desired platforms
		self.session = requests.session()
		self.utils = utils
		self.api = { 
			'base'   : 'http://www.giantbomb.com/api/games/',
			'payload': {
				#payload types (default inputs if one is not provided)
				'get': {
					'limit'    : '100',
					'format'   : 'json',
					'offset'   : '100', #max batch size set by external api
					'api_key'  : '84e4fdf8957ddf84247c3ea012a4773ffead8156', #should not be in code
					'platforms': None,
				},
				'post':{},
			},
			'pg_size_limits': {
				#for batching and possible pagination
				'min': 1,
				'max': 100,
			},
		}

	def retrieve(self, payload):
		return self.session.get(
			self.api['base'],
			params = payload,
			headers = {
				#spoof agent so external api thinks we are a browser (avoid 403's)
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
			}
		).json()

	def pg_size(self, platform):
		return self.retrieve(
			self.utils.update_dict(self.api['payload']['get'], {
				'limit': self.api['pg_size_limits']['min'],
				'platforms': platform,
			})
		)['number_of_total_results']

	def load_data(self):
		for platform in self.platform_ids:
			for offset in range(0, self.utils.roundup(self.pg_size(platform), 100), 100):
				batch = self.retrieve(
					self.utils.update_dict(
						self.api['payload']['get'], {
							'platforms': platform,
							'offset'   : offset,
							'limit'    : '100',
						}
					)
				)
				print([item['id'] for item in batch['results']])
				for item in batch['results']:
					with open(self.utils.file_dir(
						self.data_dir_pth + [self.utils.strip_punctuation(str(item['name']))+'.jb']
					), 'wb+') as out_file:
						out_file.write(zlib.compress(json.dumps(item).encode()))

if __name__ == "__main__":
	os.chdir(os.getcwd().split('mini_search')[0] + 'mini_search')
	Retriever().load_data()