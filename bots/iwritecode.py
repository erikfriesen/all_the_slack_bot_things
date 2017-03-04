@slack.command('iwritecode', config['iwritecode']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def sl9(**kwargs):
    return slack.response('http://resguru.com/wp-content/uploads/2011/05/angry-keyboard-user.gif',response_type='in_channel')
