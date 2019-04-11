from bottle import post, run, response, request
import json
import validate

# define configuration
config_file = 'service_config.json'
host_addr = '143.248.135.20'
port_num = 2848

# base class
entity_linker = None

# for CORS (to solve cross-domain issue)
def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		# set CORS headers
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if request.method != 'OPTIONS':
			return fn(*args, **kwargs)

	return _enable_cors

@post('/validate', method=['OPTIONS', 'POST'])
@enable_cors
def EL_validate():
	if not request.content_type.startswith('application/json'):
		return 'Content-type:application/json is required.'

	request_str = request.body.read()
	try :
		request_str = request_str.decode('utf-8')
	except :
		pass
	request_json = json.loads(request_str)

	result_str = json.dumps(validator.validate(request_json))

	return result_str


validator = validate.validator(config_file)
print('validation service....')
run(host=host_addr, port=port_num, debug=True)
#except KeyError as keyerr:
#	print 'given configuration is not suitable.'
#	print keyerr
#except IOError as ioerr:
#	print 'no such file'
#	print ioerr
#except Exception as exception:
#	print exception
