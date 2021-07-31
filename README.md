# VoteBot
A simple, free, easy-to-use Discord bot to enable voting on messages.

## Introduction
VoteBot has a very simple premise: watch a single Discord channel for new messages, and for every new message, add two emoji reactions; one indicating an "upvote", and one indicating a "downvote". Users can then click either reaction to show their support or anti-support for a new idea. 

For example, I use VoteBot in a server channel that revolves around server feedback (do users want a new role? a new text channel around a particular topic? etc). Anyone can suggest a new idea to implement on the server. As the mods and admins watch the reactions grow, they can quickly discern if an idea is overwhemingly desired, undesired, or contentious. They can then drive further conversation or just implement those ideas as they see fit.

## Table of Contents
    * [Creating a VoteBot instance](#creating-a-votebot-instance)
    * [Inviting VoteBot to your server](#inviting-votebot-to-your-server)
    * [Configuring VoteBot](#configuring-votebot)
    * [Developing new features](#developing-new-features)

## Creating a VoteBot instance
Currently, you cannot invite VoteBot to your server directly. There are multiple reasons for this:
1) I don't want to put in the effort to make just 1 instance of VoteBot safe to use on thousands of arbitrary Discord servers
2) It's relatively easy to just do it yourself (I have mine running on my Raspberry Pi 2 Model B)
3) Maintaining a large-scale Discord bot is a lot of work

Now that that is out of the way, you'll first need to decide how to host VoteBot. You have plenty of options; all you need is a computer or service with constant access to power and the internet. You could pay for a small server instance in the cloud, or do what I did and just plug your RaspberryPi into your router and forget about it. [I've even heard of people using Repl.it to host bots.](https://dev.to/fizal619/so-you-want-to-make-a-discord-bot-4f0n) Thankfully, Discord uses WebSockets and running the code is as easy as typing in one command, so don't worry about complex server configuration.

Once you have your server / computer / repl.it instance in place, let's get to actually creating the VoteBot instance.

1) Go to [Discord Developer Portal - My Applications](https://discord.com/developers/applications) and sign in with your Discord user.
2) Click "New Application" in the top-right.
3) Give your application a name. Obviously, I chose "VoteBot", which you are also free to use, or you can come up with something else clever if you'd like.
4) You should be presented with the general application summary screen. Give your new Discord application a description, if you'd like. 
5) Head over to the "Bot" tab on the left.
6) Click "Add Bot".
7) Confirm that you'd actually like to create a bot.
8) Click "Copy" to copy your bot's token to your clipboard.
9) Download this repo (optionally forking first) to the computer that will be running VoteBot
10) In the same directory as "votebot.py", create a new file called ".env" and add the contents:
```
# .env
DISCORD_TOKEN=<paste your bot token here>
```
(do not include spaces around the `=`)
11) Save and exit the file.
12) Go back to the computer that will be running VoteBot, and make sure that Python 3.7+ and pip3 are installed.
13) From a terminal window, type `pip3 install discord.py`
14) Again, type `pip3 install python-dotenv`
15) Finally, to start the bot running, run `python3 votebot.py`.
    * You should receive a message that says "VoteBot#1234 connected to Discord!"
    * The first time you run the bot, you might see a message that there was an error reading a file. That's because the file doesn't exist yet. Don't worry, that file is `server.json` and will be created for you by the program. As long as you don't delete this file, you shouldn't see that error again.
    * You will need to leave this process running for the bot to continue to operate. In order to kill the bot, just type `<CTRL-C>`. If you want to sign out of your computer but keep the process running, look into using `tmux` and creating, then detaching from sessions.
16) Congrats! You are ready to invite VoteBot to your server.

Note: you will only have to do this once, and then you can invite VoteBot to as many servers as you'd like. VoteBot's code is flexible enough to handle being in multiple servers simultaneously.

## Inviting VoteBot to your server
Inviting VoteBot should be fairly straight-forward. After creating your VoteBot instance:
1) Go to [Discord Developer Portal - My Applications](https://discord.com/developers/applications) and sign in with your Discord user.
2) Click on your new VoteBot application.
3) Head over to the "OAuth2" tab.
4) Under "SCOPES", click "bot", and under "BOT PERMISSIONS", click "Read Message History" and "Add Reactions". (NOTE: if you give your bot more permissions, you give the bot more permissions than it needs to function properly. Internet safety and security conventions state that you should never give something more permissions than is absolutely necessary)
5) Under "SCOPES", there should be a URL that was generated for you. Copy that URL, and paste it into a new tab in your browser.
6) Discord will ask you which server you'd like to invite VoteBot to. Select the desired server (make sure you have the "Manage Server" permission in the server you are adding VoteBot to).
7) If all goes well, VoteBot will now be in your server and ready for configuration!

## Configuring VoteBot
VoteBot comes with a handful of features, all of which can be configured. VoteBot's prefix is `vb!`, which is used to avoid collision with other common Discord bots.

### VoteBot's features:
    * Watching channels and adding upvote / downvote reactions to every message in that channel. _By default, **no channels** are watched_.
    * Mentioning VoteBot's user in _any_ message, regardless of channel, will add upvote / downvote reactions to that message. _By default, this feature is turned **off**_.
    * Configuring VoteBot can be done server-wide, or in one specific channel of that server. _By default, **all channels** can be used to configure VoteBot_. (It is **HIGHLY** recommended you restrict this to a single channel after inviting VoteBot to your server, ideally a channel that only mods and admins have access to, to prevent trolls from configuring VoteBot.)
    * Custom server emojis can be used as upvotes / downvotes. _By default, VoteBot will use :arrow_up: and :arrow_down:_. (You can only use **custom server emotes local to the server VoteBot is a user in**. Attempting to use other Unicode emojis or emojis from other servers will result in an error)

### VoteBot Commands:
(NOTE: `<channel_mention>` must be a valid channel within the server; it's easiest to do this by typing a hashtag, and then the channel name `#channel-name`. Discord will automatically format this into a channel mention for you.)
    * `vb!help`: Displays a helpful prompt with this list of commands in a Discord message
    * `vb!show`: Displays all of the currently configured options.
    * `vb!watch <channel_mention>`: Start watching a channel and adding emojis to every message posted. 
    * `vb!unwatch <channel_mention>`: Stop watching a channel.
    * `vb!vote-on-mention <decision>`: Enable or disable adding emojis to any message in the server that mentions VoteBot's user. `<decision>` must be either the value `yes` or `no`.
    * `vb!upd-conf-channel <channel_mention>`: Set or update the channel used to configure VoteBot. After running this, only the channel mentioned will be used to configure VoteBot, and any commands with the `vb!` prefix will be ignored unless posted in the configured channel.
    * `vb!clr-conf-channel`: Removes any configured channel and returns VoteBot to a state of listening for configuration commands (`vb!` commands) in **every channel in the server.**
    * `vb!use-custom-emoji <upordown> <emoji>`: Sets a custom, local server emoji to be the reaction used for either upvotes or downvotes. `<upordown>` must either be the value `up` or `down`. `<emoji>` must be a valid emoji mention (i.e. `:EMOJI_NAME:`).
    * `vb!del-custom-emoji <upordown>`: Returns VoteBot to using the default Unicode emojis :arrow_up: and :arrow_down: for the specified reaction. `<upordown>` must either be the value `up` or `down`.

## Developing new features
In order to contribute to this body of code (thank you!), please fork this repository, make the changes desired, and then create a pull-request back to this repository. I'll try to review the pull-request in a timely manner and give feedback. You will need:
    * Python 3.7 (or greater)
    * pip3
    * `pip3 install discord.py`
    * `pip3 install python-dotenv`

(COMING SOON: an easier way to set up a development environment).

In order to test your changes, I recommend creating a [new Discord application](#creating-a-votebot-instance) called "VoteBot(dev)" or something similar. This way, you can invite a development version of the bot to a private server and test new features without affecting your production version of the bot. Just make sure the `DISCORD_TOKEN` in your .env file is the development token.

To run the bot locally, just do the same as before: `python3 votebot.py`. You must be connected to the internet to do this. In order to refresh the code, kill the bot (`<CTRL-C>`) and start it up again.

If you'd like to suggest new features but don't want / know how to code them, please create a new issue on this repository so we can work on it!

Here is a list of helpful development resources:
    * [General Discord API](https://discordpy.readthedocs.io/en/stable/api.html)
    * [Discord ext.commands API](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html)
    * [Discord Cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)
    * [Python 3](https://docs.python.org/3/library/)
