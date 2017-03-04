@slack.command('tteesstt', config['tteesstt']['token'],
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
    return slack.response("its working",response_type=_response_type)
    for key in parameters:
        if key == "help":
            response_payload = return_help()[0]
        elif key == "points":
            response_payload = add_points(user_name,parameters[key][0],channel,parameters[key][1],parameters[key][2])
            _response_type = 'in_channel'
        elif key == "stats":
            response_payload= stat_query.renderBitch(parameters[key],user_name)
        elif key == "error":
            response_payload = parameters[key]
        else:
            response_payload = "super crazy shit. call the Doctor"
    #final response from slack

    #return slack.response("this is text")