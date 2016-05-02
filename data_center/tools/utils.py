import string, functools, os

'''
		3310
	
	l   = len of token
	i   = number of tokens
	s_l = len of str         = sum (from j=0 to j=i-1) of l(j)
	tw  = token weight       = l(token)/s_l

		sum(from j=0 to j=i-1) of l(j)*tw(j) = 1
'''

def strip_punctuation(text):
	translator = str.maketrans({key: None for key in string.punctuation})
	return text.translate(translator).lower()

def tokenize(text):
	return strip_punctuation(text).split(' ')

def roundup(x, nearest):
	return (int(x/nearest)+1)*nearest

def set_params(original, update): #could be removed after addition of update_dict
	'''
		original
			purpose - payload with default params set on object creation
			example: {
				'a': 1,
				'b': 2,
			}
		update
			purpose - update payload
			example: {
				'b': 3,
				'd': 4,
			}

		result: {'a': 1, 'b': 3, 'd': 4} (given the sample payloads above)
	'''
	return dict(list(original.items()) + list(update.items()))

def update_and_return(original, key, val = None):
	'''
		adds a value to the "original" dict with the key being the input
	'''
	if val:
		original.update({key: val})
	else:
		original.update({key: {}})
	return original

def update_dict(original_dict, new_val, path = None):
	'''
		checks if path to the desired value already exists in
		the original_dict (if not it generates the desired path)
		and appends id to the original_dict values
		
		path = list of keys to traverse to get to desired location
		
		works for arbitrarily nested dicts
	'''
	if path:
		functools.reduce(lambda d, k: d.get(k) if d.get(k) else update_and_return(d, k)[k], path, original_dict)
		functools.reduce(lambda d, k: d[k], path[:-1], original_dict)[path[-1]].update(new_val)
	else:
		original_dict.update(new_val)
	return original_dict

def file_dir(path = None):
	dir_pth = os.getcwd().split('mini_search')[0] + 'mini_search'
	if path:
		for dir in path:
			dir_pth = os.path.join(dir_pth, dir)
	return dir_pth

#list(filter(lambda s: s if '123' in s else None, tokens))

