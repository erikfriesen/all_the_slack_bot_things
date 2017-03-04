@app.route('/newuser/<email>')
def newuser(email):
    if email not in email_blacklist:
        try:
            channel = 'admin_team'
            bot_token = 'xxxx'
            bot_username = 'xxxx'
            parameters = {'token':bot_token, 'text':email, 'channel':channel,
                    'username':bot_username,'as_user':'true'}
            requests.get("https://slack.com/api/chat.postMessage",params=parameters)
            return jsonify({"status":200})
        except:
            return {"status": "well fuck"}
    else:
        return {"status": "EMAIL BLACKLISTED"}
    #requests.get("https://slack.com/api/chat.postMessage?token=xoxb-105417684083-kJyxsrt0bdFldkROAkfd31Ng&channel=admin_team&text={0}".format(email))
