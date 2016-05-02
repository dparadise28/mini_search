from data_center.search import Search
import cherrypy

class Api(object):
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def find(self, **params):
		if params.get('text', False):
			return Search().retrieve(params['text'],
									 params.get('offset', 0),
									 params.get('batch_size', 100))
		else:
			return {"error": "please enter a search term"}

if __name__ == '__main__':
	cherrypy.quickstart(Api())