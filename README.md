OTSE-ELUST
==========

**otse-elust** is an extremely simple filemanager for serving static files through Google App Engine. 

This app provides a upload interface to store and serve files and was initially developed for [otseelust.com](http://www.otseelust.com).

It's kind of a *poor man's CDN* solution. You can set a custom domain for the app (like *static.mydomain.com*), upload files, get serving URL's in return and use them in your webpage
(extremely useful if you want to use images etc. in an environment where you can alter the template files but can't upload any additional files).

Maximum size for a single uploaded file - 2GB

Installation
----

Update *app.yaml* with a correct app-id. Deploy to Google App Engine. Start using.

NB
----

In the App authentication options allow users only from a specific domain OR update app.yaml to allow only admin logins (change *login: required* to *login: admin*).