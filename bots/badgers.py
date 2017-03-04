@slack.command('badgers', config['badgers']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def bum(**kwargs):
    #get the kwargs
    text = kwargs.get('text')
    user_name = kwargs.get('user_name')
    user_id = kwargs.get('user_id')
    channel = kwargs.get("channel_name")

    #parse the natural language text kwarg and
    #deal with the returned dictionary.
    #dictionary keys dictate the action
    parameters = parse_validate_text_kwarg(text)
    _response_type = 'ephemeral'
    return slack.response("https://www.youtube.com/watch?v=gx6TBrfCW54&feature=youtu.be&t=16s",response_type="in_channel")