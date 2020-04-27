import telebot
import spotipy
from telebot import types
from spotipy.oauth2 import SpotifyClientCredentials

# Enter telegram bot token right here
TOKEN = '<token_string>'

commands = {
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'top10global': 'Lists the top 10 songs from Spotify\'s Global Top 50 chart',
    'top10sg'    : 'Lists the top 10 songs from Spotify\'s Singapore Top 50 chart'
}

def get_top_charts(context):
	spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
	if context == 'global':
		playlist_URI = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
	elif context == 'sg':
		playlist_URI = 'spotify:playlist:37i9dQZEVXbK4gjvS1FjPY'
	else:
		raise Exception('SyntaxError: invalid context')
	results = spotify.playlist_tracks(playlist_URI)
	track_count = 0
	string = ''
	for track in results['items'][:10]:
		track_count += 1
		string = string + str(track_count) + '. ' + track['track']['name'] + '\n'
		artist_count = 0
		for artist in track['track']['artists']:
			artist_count += 1
			string = string + artist['name']
			if len(track['track']['artists']) > artist_count:
				string = string + ', '
			else:
				string = string + '\n'
		if track_count < 10:
			string = string + '\n'
	return string

def listener(messages):
    for message in messages:
        if message.content_type == 'text':
            print(str(message.chat.first_name) + " [" + str(message.chat.id) + "]: " + message.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hi there, I am Spotibot. This bot lists the top 10 songs in Spotify's Global Top 50 and Singapore Top 50 charts.")
        command_help(message)

@bot.message_handler(commands=['help'])
def command_help(message):
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['top10global'])
def command_long_text(message):
    try:
    	bot.reply_to(message, get_top_charts('global'))
    except:
    	bot.reply_to(message, "Error getting charts. Please try again later.")

@bot.message_handler(commands=['top10sg'])
def command_long_text(message):
    try:
    	bot.reply_to(message, get_top_charts('sg'))
    except:
    	bot.reply_to(message, "Error getting rankings. Please try again later.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    bot.reply_to(message, "I don't understand \"" + message.text + "\"\nMaybe try the help page at /help")

bot.polling()
