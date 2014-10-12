iPhone 6 and 6 Plus availability watcher
========================================

So, you want an iPhone 6 or 6 Plus, you don't want to wait 7-10 days for delivery, and you're fed up with hammering on the [Apple in-store pickup reservation tool](https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability) only to be told again and again that the one you want is out of sock? 

I can help. In this repo you'll find a robust script to watch for availability of a given iPhone 6 or 6 Plus model in the UK, alerting you the very moment when the model you want is in stock.

How to use this script to get an iPhone 6
=========================================

1. If you don't live in the UK: figure out how to modify it to work with your country.
1. The script should run as-is on a Mac, without you needing to install anything else. On other platforms you'll need a Python runtime.
1. Configure the variables at the start of the script for the codes for the Apple Stores you can travel to and the iPhone model number you want. 
1. Optionally, configure the script to email you (see below.)
1. ./apple-watch.py 
1. Watch the output until your chosen model comes into stock
1. Reserve, go to Apple Store, enjoy your new phone!
  
Sending email
=============

By default, when the script finds stock, it won't do anything other than print a message.

If you want to get it to send an email, you'll need to provide a Gmail (or other auth-SMTP service provider) username and password in the script. Obvious,y embedding your password in a script is a terrible idea that I do not endorse. If you do go down this road you'll need to [enable support for less secure apps](https://www.google.com/settings/security/lesssecureapps) in your Google account. As an extra precaution, don't use your main Gmail account, and when you're done with the script change the password.

Other notification options are left as an exercise for the reader.

When is the best time to try and get an iPhone 6?
=================================================

I ran this script for several weeks, and collated, each time it ran, the total count of iPhone 6 and 6 Plus availability. Now, Apple doesn't tell us how many actual phones are in stock at each location; but it does tell us which exact SKU (combination of model, capacity, and colour) is in stock at each of the UK stores.

Using this we can calculate a simple fraction of how many different models are in stock in across all UK stores. This allows us to see one important thing: when Apple releases new stock allocation, which is the best time to be ready to try and reserve your model. You can see the [data and a graph of it here][graph].

From this we can make a couple of observations:

1. The reservation system goes offline each day at 7pm. 
1. It comes online every day at a couple of minutes past midnight. This is when stock allocation it at its highest i.e. your best time to try and reserve the model you want.
1. That stock declines rapidly over the hour -- lots of people are hammering away at the system at this time, reserving phones as fast as they can.
1. During the day, new stock allocation is brought online at random-seeming intervals. So keep watching the script.

[graph]: https://docs.google.com/spreadsheets/d/1BF5Daye2aDSOmq7qrbr8iMyRyoQHJZ3uc6V2e9sv7Ys/pubhtml

