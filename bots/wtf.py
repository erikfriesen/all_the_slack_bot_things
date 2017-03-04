@slack.command('wtf', config['wtf']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def s20(**kwargs):
    return slack.response('http://media1.giphy.com/media/aZ3LDBs1ExsE8/giphy.gif',response_type='in_channel')
