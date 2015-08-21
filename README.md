<<<<<<< HEAD
# Microbiome bhp077

Microbiome
=======
[![Build Status](https://travis-ci.org/botswana-harvard/getresults-receive.svg?branch=develop)](https://travis-ci.org/botswana-harvard/getresults-receive)
[![Coverage Status](https://coveralls.io/repos/botswana-harvard/getresults-receive/badge.svg?branch=develop&service=github)](https://coveralls.io/github/botswana-harvard/getresults-receive?branch=develop)

# getresults-receive

The `Receive` model automatically allocates a unique receiving identifier for a new specimen.

	>>>receive = Receive.objects.create(patient=self.patient)
    >>>receive.receive_identifier
    'AAA0001'

In settings, add:

	RECEIVE_IDENTIFIER_SEED = ('AAA', '0000')
	RECEIVE_IDENTIFIER_ALPHA_PATTERN = r'^[A-Z]{3}$'
	RECEIVE_IDENTIFIER_NUMERIC_PATTERN = r'^[0-9]{4}$'

Identifiers
-----------

With the above attributes in `settings` your identifier will start with 'AAA0001'. For example:

	>>> from getresults_receive.receive_identifier import ReceiveIdentifier
	>>> new_id = ReceiveIdentifier(None)
	>>> print(new_id)
	'AAA0001'

The identifier increments on the numeric sequence then the alpha:

	>>> new_id = ReceiveIdentifier('AAZ9998)
	>>> print(new_id)
	'AAA9999'	

	>>> new_id.increment()
	>>> print(new_id)
	'AAB9999'	

	>>> new_id = ReceiveIdentifier('AAZ9998)
	>>> print(new_id)
	'AAZ9999'	
	>>> new_id.increment()
	>>> print(new_id)
	'ABA0001'	

See `getresults-identifier` for more details.
>>>>>>> 345a94d0603327bfc7ff82ca640eae2836723cf9
