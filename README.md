# auto-join-spam

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)

Automatically join links sent by spam bots.

Some time ago, I found one interesting link to private channel on Telegram, which led me to a bot,
that advertised dozens other channels. I tried to join them all for fun but was quickly rate limited.

So I came up with an idea to write a bot that will do this for me. Since then I discovered it is a huge
advertising company that works by this strategy:

- Channel A posts an ad for Channel B.
- When user tries to join Channel B, they send a request for join.
- For "verification", bot sends a bunch of links to other channels to the user, and user must join them all to join Channel B.
- After user tries to join a few of those channels, more bots start to adverise more channels.

So basically this bot functions like a spider, it collects all links bots and channels send it, and then
tries to join every single channel to collect even more links. I had similar project actually -
https://github.com/PerchunPak/the-war-tracker-bot

On the moment of writing, this bot discovered almost 1500 channels and joined 1000 links with a speed
of 5 links per 15 minutes (it's the maximum Telegram allows).

Most of those channels are news, there are some porn channels and many channels were advertised as "savage" channels
(though they are just news channels with ads of other "savage" channels). There are even a few bet channels!

## Things to improve

- Joining public channels.
- Sending message when ads bot asks for it.

  Bot writes messages to send into db, but it sends all of those messages only after
  we joined all links in db. Which may be impossible, because I didn't expect this
  network to be so huge.
- Would be cool to collect from where I got that link, so it would be possible to create web-graphs.

  But it would require to start joining links from scratch in which I am not really interested.

## Installing

https://hub.docker.com/r/perchunpak/auto-join-spam

### Configuration

All configuration happens in `/app/data/config.yml`.

### If something is not clear

You can always write me!

## Thanks

This project was generated with [python-template](https://github.com/PerchunPak/python-template).
