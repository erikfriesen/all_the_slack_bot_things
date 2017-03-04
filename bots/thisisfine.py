@slack.command('thisisfine', config['thisisfine']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def sl8(**kwargs):
    return slack.response('http://gph.is/1IPoO7R',response_type='in_channel')