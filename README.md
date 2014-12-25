email2mailchimp
================

A simple Flask app that re-routes a Webhook from Stripe to subscribe the user to MailChimp

Stripe has a list of webhooks that can be pinged when an action occurs. This is available under "Account Settings"

For this application, we deployed to Heroku a small Flask app that is waiting for the POST request with a json payload. If it has the right transaction type of "charge.succeeded" we check the email address then, using the MailChimp API we add that to the mailing list for updates.

We have two enviornmental variables, the first is a MailChimp API Key. You can get this in the "Account"->"Extras" section of MailChimp. The next enviornmental variable is the MailChimp List ID. You can see your lists by using the /lists route. This will print to the logs your list names and IDs. You can then copy the correct list ID into the enviornmental variable.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Routes

###/list
This is a very simple route that takes the MAILCHIMP_API_KEY from the enviornmental variable and prints to the log your lists and their corresponding IDs. This is useful to set the MAILCHIMP_LIST_ID enviornmental variable

###/subscribe
If you want to subscribe an email directly to your mailing list, you POST two key value pairs to this route. &email=<email address>&sk=<secret key>

The email is the email address of the person you wish to add to the list set in the MAILCHIMP_LIST_ID enviornmental variable. The secret key is a shared secret that you have as a SECRET_KEY enviornmental variable. This is just to protect anyone from posting to this end-point and adding emails to your list.

###/webhook
This takes the Stripe JSON data and parses it to look for the right payload type of "charge.succeeded" and grabs an email address and posts it to the MailChimp Subscribe API.


## Notes

Be sure that you set your Stripe WebHook to LIVE, otherwise it will never send you any data.
