@slack.command('call_admin', config['call_admin']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def s21(**kwargs):
    text = kwargs.get('text')
    user_name = kwargs.get('user_name')
    user_id = kwargs.get('user_id')
    from_channel = kwargs.get("channel_name")
    channel = 'admin_team'
    bot_token = 'xxxx'
    bot_username = 'admin_assistant'
    parameters = {'token':bot_token, 'text':"user: {0}, channel: {1}, message: {2}".format(user_name,from_channel, text), 'channel':channel,
                    'username':bot_username,'as_user':'true'}
    requests.get("https://slack.com/api/chat.postMessage",params=parameters)
    return slack.response('admin called',response_type='ephemeral')
