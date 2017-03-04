from datetime import datetime
import mysql.connector, requests, configparser
from flask import Flask
from flask_slack import Slack
from flask_slack import SlackError
from slackclient import SlackClient
from random import randint
from threading import Thread
from flask import jsonify
import random
import bots

config = configparser.ConfigParser()
config.read('configs/config_the_bots.ini')

from scoreboard_renderer import renderBitch
app = Flask(__name__)

email_blacklist = ['vivi@slackfu.com']

slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)
#gisdevs points xxxx team_id = 'xxxx'
#the spatial ones flaskpaw xxxx team_id = 'xxxx'



