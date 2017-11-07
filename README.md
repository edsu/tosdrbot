This is a little project for expressing the terms of service documents tracked
by the [Terms of Service; Didn't Read Project](https://tosdr.org) as RSS so that
they can be tracked by a [diffengine](https://github.com/docnow/diffengine)
instance.

Specifically the rules xml documents found in the
[tosdr/tosback2](https://github.com/tosdr/tosback2/tree/master/rules) project
are downloaded, parsed and written out as an RSS file that are available at:

https://edsu.github.io/tosdrbot/rss.xml

Converting the rules to RSS may seem like a step backwards but it is just a
necessary step to get a diffengine instance to monitor the URLs it contains.
With the generated RSS you can then install and run diffengine:

```
% pip install diffengine
% diffengine ~/.diffengine-tosdrbot
What RSS/Atom feed would you like to monitor? https://edsu.github.io/tosdrbot/rss.xml
Would you like to set up tweeting edits?  [Y/n] Y
Go to https://apps.twitter.com and create an application.
What is the consumer key? eif99jslkjs9fsjslk 
What is the consumer secret? slk93kdj02lpxmmvkski393jmslsi3jl
Log in to https://twitter.com as the user you want to tweet as and hit enter.
Visit https://api.twitter.com/oauth/authorize?oauth_token=Vq20BAAAAAAAzqBnAAAKX5gbgI0 in your browser and hit enter.
What is your PIN? 4522830
Saved your configuration in /home/ed/.diffengine-tosdrbot/config.yaml
Fetching initial set of entries.
```

Then create a cron job to run diffengine periodically to check for changes.

```
0 * * * * /usr/bin/flock -xn /home/ed/.diffengine/lock -c "/usr/local/bin/diffengine /home/ed/.diffengine-tosdrbot"
```

