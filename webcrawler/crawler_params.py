import sys

class ParamsEntry:

	def __init__(self, value, descr, is_mandatory):
		self.value = value
		self.descr = descr
		self.is_mandatory = is_mandatory

	def __str__(self):
		return 'value={}, descr={}, is_mandatory={}'.format(self.value, self.descr, self.is_mandatory)

class ParamsManager:
	PARAM_INIT_URL = 'init_url'

	_BOOLEAN_PARAMS = []

	default_params = {
			PARAM_INIT_URL			:	ParamsEntry(None, 'Initial url which the crawling starts from', True)
	}

	def __init__(self, cmd_args):

		self.params = dict(self.default_params)

		for arg in cmd_args:
			if '=' in arg:
				key_value = arg.split('=')
				assert len(key_value) == 2, 'wrong argument: {}'.format(arg)

				key = key_value[0]
				new_value = key_value[1]
				def_entry = self.params.get(key)

				if def_entry is None:
					continue

				if key in ParamsManager._BOOLEAN_PARAMS:
					self.params[key] = ParamsEntry(self.__to_bool(new_value), def_entry.descr, def_entry.is_mandatory)
				else:
					self.params[key] = ParamsEntry(new_value, def_entry.descr, def_entry.is_mandatory)

			if arg in ['-?', '-h', '--help']:
				self.print_help()

		for key, entry in self.params.iteritems():
			if entry.is_mandatory and entry.value is None:
				print ('Mandatory parameter "{}" not provided'.format(key))
				self.print_help()


	def __format_key(self, key, is_mandatory):
		return '{}{}{}'.format('<' if is_mandatory else '[', key, '>' if is_mandatory else ']')

	def __to_bool(self, str_val):
		return str_val in ['True', 'true', '1', 't', 'T']

	def get(self, key):
		entry = self.params.get(key)
		assert entry is not None, 'Key {} not found'.format(key)
		return entry.value

	def __print_params_iter(self, dict_iter):
		for key, entry in sorted(dict_iter):
			print '{} ({}) - {}'.format(self.__format_key(key, entry.is_mandatory), entry.value, entry.descr)

	def __print_params(self, params_map):
		self.__print_params_iter(filter(lambda x: x[1].is_mandatory, params_map.iteritems()))
		self.__print_params_iter(filter(lambda x: not x[1].is_mandatory, params_map.iteritems()))

	def print_help(self):
		print 'Parameters: '
		self.__print_params(self.default_params)
		sys.exit(0)

	def print_params(self):
		self.__print_params(self.params)
