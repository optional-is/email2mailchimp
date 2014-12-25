# coding: utf-8

import os
import logging
import flask
import json
import flask_config
from flask import request
from werkzeug.datastructures import ImmutableMultiDict
from postmonkey import PostMonkey
from postmonkey import MailChimpException

app = flask.Flask(__name__)

app.static_folder = "templates"
app.SEND_FILE_MAX_AGE_DEFAULT = 0

@app.route('/lists')
def lists():
	pm = PostMonkey(os.environ.get('MAILCHIMP_API_KEY',''))
	lists = pm.lists()
	for list in lists['data']:
	    print list['id'], list['name']

	return file('templates/200.json').read(), 200

@app.route('/subscribe', methods=['POST'])
def subscribe():
	if os.environ.get('SECRET_KEY',None) != None or request.form.get('sk',None) != None:
		secret_key = os.environ.get('SECRET_KEY',None)
		if secret_key != request.form.get('sk',None):
			# We were expecting a secret key because one is set, but we didn't or it didn't match
			return file('templates/401.json').read(), 401
		
	# We have passed the shared secret or we didn't care about it
	pm = PostMonkey(os.environ.get('MAILCHIMP_API_KEY',''))
	
	# Get a posted email address
	email = request.form.get('email',None)
	if not email == None:
		# Send that off to Mailchimp
		pm = PostMonkey(os.environ.get('MAILCHIMP_API_KEY',''))
		try:
			pm.listSubscribe(id=os.environ.get('MAILCHIMP_LIST_ID',''),email_address=email,double_optin=False)
		except MailChimpException, e:
			print e.code  # 200
			print e.error # u'Invalid MailChimp List ID: 42'
			return file('templates/401.json').read(), 401

	return file('templates/200.json').read(), 200

@app.route('/webhook/gumroad', methods=['POST'])
def gumroad():
	# We have passed the shared secret or we didn't care about it
	pm = PostMonkey(os.environ.get('MAILCHIMP_API_KEY',''))

	# Get a posted email address
	email = request.form.get('email',None)
	if not email == None:
		# Send that off to Mailchimp
		pm = PostMonkey(os.environ.get('MAILCHIMP_API_KEY',''))
		try:
			pm.listSubscribe(id=os.environ.get('MAILCHIMP_LIST_ID',''),email_address=email,double_optin=False)
		except MailChimpException, e:
			print e.code  # 200
			print e.error # u'Invalid MailChimp List ID: 42'
			return file('templates/401.json').read(), 401

	return file('templates/200.json').read(), 200



@app.route('/webhook', methods=['POST'])
def strip2mailchimp():
	"""
	{
	  "created": 1326853478,
	  "livemode": false,
	  "id": "evt_00000000000000",
	  "type": "charge.succeeded",
	  "object": "event",
	  "request": null,
	  "data": {
	    "object": {
	      "id": "ch_00000000000000",
	      "object": "charge",
	      "created": 1412117456,
	      "livemode": false,
	      "paid": true,
	      "amount": 100,
	      "currency": "eur",
	      "refunded": false,
	      "card": {
	        "id": "card_00000000000000",
	        "object": "card",
	        "last4": "4242",
	        "brand": "Visa",
	        "funding": "credit",
	        "exp_month": 8,
	        "exp_year": 2015,
	        "fingerprint": "3WqOgApKDjCTvHEG",
	        "country": "US",
	        "name": null,
	        "address_line1": null,
	        "address_line2": null,
	        "address_city": null,
	        "address_state": null,
	        "address_zip": null,
	        "address_country": null,
	        "cvc_check": "pass",
	        "address_line1_check": null,
	        "address_zip_check": null,
	        "customer": null
	      },
	      "captured": true,
	      "refunds": {
	        "object": "list",
	        "total_count": 0,
	        "has_more": false,
	        "url": "/v1/charges/ch_14iZSOLQaIfBBJAWXuK7DE0I/refunds",
	        "data": []
	      },
	      "balance_transaction": "txn_00000000000000",
	      "failure_message": null,
	      "failure_code": null,
	      "amount_refunded": 0,
	      "customer": null,
	      "invoice": null,
	      "description": "My First Test Charge (created for API docs)",
	      "dispute": null,
	      "metadata": {},
	      "statement_description": null,
	      "receipt_email": null,
	      "receipt_number": null
	    }
	  }
	}
	"""

	# locally use .form
	#i = request.form
	#for k in i:
	#	event_json = json.loads(k)
		
	event_json = json.loads(request.data)

	# we have the data we are looking for
	if 'type' in event_json and event_json['type'] == 'charge.succeeded':
		# Get the email address
		email = event_json['data']['object']['receipt_email']
		
		if not email == None:
			# Send that off to Mailchimp
			pm = PostMonkey(os.environ.get('MAILCHIMP_API_KEY',''))
			try:
				pm.listSubscribe(id=os.environ.get('MAILCHIMP_LIST_ID',''),email_address=email,double_optin=False)
			except MailChimpException, e:
				print e.code  # 200
				print e.error # u'Invalid MailChimp List ID: 42'
				return file('templates/500.json').read(), 500
		
	
	return file('templates/200.json').read(), 200


@app.route('/')
def home():
	"""Returns html with an overview of shapes to compare the sizes-of """


	return file('templates/index.html').read()


if __name__ == '__main__':
	# Set up logging to stdout, which ends up in Heroku logs
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.WARNING)
	app.logger.addHandler(stream_handler)

	app.debug = False
	app.run(host='0.0.0.0', port=flask_config.port)
