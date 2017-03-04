@slack.command('thumbsup', config['thumbsup']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def sl4(**kwargs):
    return slack.response("https://imgur.com/uKL8tJg.gif",response_type='in_channel')

@slack.command('believe', config['believe']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def sl5(**kwargs):
    return slack.response("https://youtu.be/YLO7tCdBVrA?t=2s",response_type='in_channel')

@slack.command('hi', config['hi']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def sl6(**kwargs):
    return slack.response("https://media.giphy.com/media/SYhK02vJMUeL6/giphy.gif",response_type='in_channel')