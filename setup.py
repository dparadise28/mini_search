import pip, os, sys

def install(packages):
	for package in packages:
		pip.main(['install', package])

if __name__ == '__main__':
	#activate py env (needs to be rewritten)
	# from data_center.tools import utils
	# try:
		# os.system(utils.file_dir(['env', 'Scripts', 'Activate.ps1',]))
	# except:
		# try:
			# os.system(utils.file_dir(['env', 'Scripts', 'activate.bat']))
		# except:
			# print('please make sure there is an env or install the modules globally')
			# sys.exit()

	#install required modules (this really should be in a req txt file and properly packaged)
	install(['CherryPy', 'ngram', 'requests'])

	from data_center.data.data_import import Retriever
	#load data to disk
	Retriever().load_data()

	#run server
	os.system('python serve.py')