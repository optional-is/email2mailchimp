stripe2mailchimp
================

A simple Flask app that re-routes a Webhook from Stripe to subscribe the user to MailChimp

Stripe has a list of webhooks that can be pinged when an action occurs. This is available under "Account Settings"

For this application, we deployed to Heroku a small Flask app that is waiting for the POST request with a json payload. If it has the right transaction type of "charge.succeeded" we check the email address then, using the MailChimp API we add that to the mailing list for updates.

We have two enviornmental variables, the first is a MailChimp API Key. You can get this in the "Account"->"Extras" section of MailChimp. The next enviornmental variable is the MailChimp List ID. You can see your lists by using the /lists route. This will print to the logs your list names and IDs. You can then copy the correct list ID into the enviornmental variable.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)
