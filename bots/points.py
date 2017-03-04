@slack.command('points', config['points']['token'],
               config['DEFAULT']['team_id'], methods=['POST'])
def your_method(**kwargs):
    #get the kwargs
    text = kwargs.get('text')
    user_name = kwargs.get('user_name')
    user_id = kwargs.get('user_id')
    channel = kwargs.get("channel_name")
    channelID = kwargs.get("channel_id")
    responseURL = kwargs.get("response_url")
    #parse the natural language text kwarg and
    #deal with the returned dictionary.
    #dictionary keys dictate the action
    parameters = parse_validate_text_kwarg(text)
    _response_type = 'ephemeral'
    _attachments = ''
    for key in parameters:
        if key == "help":
            response_payload = return_help()[0]
        elif key == "points":
            response_payload = add_points(user_name,parameters[key][0],channel,parameters[key][1],parameters[key][2])
            _response_type = 'in_channel'
        elif key == "stats":
            response_payload= stat_query(parameters[key],user_name)
            _attachments = [renderBitch(response_payload)]
            response_payload=""
            print(_attachments)
        elif key == "error":
            response_payload = parameters[key]
        elif key == "rain":
            points = parameters[key]
            makeItRain(user_name,channelID,points,user_id,responseURL)
            response_payload = "And {0} makes it rain!!! http://i.giphy.com/y8Mz1yj13s3kI.gif".format(user_name)
            _response_type = 'in_channel'
        else:
            response_payload = "super crazy shit. call the Doctor"
    #final response from slack
    return slack.response(response_payload,response_type=_response_type,attachments=_attachments)
    #return slack.response("this is text")


# new natural language parameter parsing function
def parse_validate_text_kwarg(text):
    args_from_text = text.split(" ")
    args_from_text[2:]= [" ".join(args_from_text[2:])]
    if args_from_text[0] in ['me','top_5','low_5','givers','lasers','takers']:
        # found a valid statistic request return it
        return {"stats":args_from_text[0]}
    elif args_from_text[0].find("@",0)==0:
        #found an @ in the first position of the first split arg,
        #probably point allocation. test the 2nd arg for intiger correct if out
        #of bounds
        try:
            points = int(args_from_text[1])
            if points >100:
                points=100
            elif points < -100:
                points = -100
            else:
                points = points
        except:
            return {"error":"{0} is not a number Python can convert to an integer...Use /points ? for help....This is kinda awkward...".format(args_from_text[1])}
        getter = args_from_text[0]
        points = points
        reason = args_from_text[2]
        return {"points":[getter,points,reason]}
    elif args_from_text[0] in ["help","-h","?"]:
        return {"help":0}
    elif args_from_text[0] == "makeItRain":
        #Oooo someone is generious, found makeitrain in the first position of the first split arg,
        #test the 2nd arg for intiger correct if out
        #of bounds
        try:
            points = int(args_from_text[1])
            if points >100:
                points=100
            elif points < -100:
                points = -100
            else:
                points = points
        except:
            return {"error":"{0} is not a number Python can convert to an integer...Use /points ? for help....This is kinda awkward...".format(args_from_text[1])}
        return {"rain": points}
    else:
        # return a fuck you for trying to be a dick.
        return {"error":"ERROR: Parameters invalid please check your input:{0}. Use /points ? for help".format(text)}

#return help
def return_help():
    return ["/points @username(user to give points to) 50(points to give,"+
            "100 - -100) reason(optional)\n " +
            "/points me(your score)\n"+
            "/points top_5 (top 5 on the scoreboard)\n"+
            "/points low_5 (low 5 on the scoreboard)\n"+
            "/points givers (top 5 givers scoreboard)\n"+
            "/points takers (top 5 takers scoreboard)\n"]

#statistic functions
def stat_query(stat,user_name):
    # connect to database, determine the query to run, run that shit, return the rows.
    # NEED TO FORMAT THE RESPONSE AS AN ATTACHMENT. LOOK AT THE FIELDS ATTACHMENT PARAMETER IN THE SLACK API
    try:
        cnx = mysql.connector.connect(user='xxxx', password='xxxx', host ='xxxx', database='xxxx')
        cursor = cnx.cursor()
    except Exception as e:
        return "Error connecting to the SEGA database. " + str(e)
    if stat == "me":
        # return the me query.
        cursor.execute('select getter, sum(points) as points from points_raw where getter = "@{0}";'.format(user_name))
        #return "me stat"
    elif stat == "top_5":
        #return the top_5 query
        cursor.execute('select getter, sum(points) as points from points_raw where getter <> "@robodonut" group by getter order by points DESC limit 5;')
    elif stat == "low_5":
        #return the low 5 query
        cursor.execute('select getter, sum(points) as points from points_raw group by getter order by points ASC limit 5;')
    elif stat == "givers":
        #return the top 5 givers query
        cursor.execute('select giver, sum(points) as points from points_raw where points >0 group by giver order by points DESC limit 5;')
    elif stat == "takers":
        #return the low 5 givers query
        cursor.execute('select giver, sum(points) as points from points_raw where points <0 group by giver order by points ASC limit 5')
    elif stat == "lasers":
        return "http://i.giphy.com/xhbBLTLh9Ep8Y.gif"
    else:
        return "Crazy stats shit whent down"
    query_results = cursor.fetchall()
    cnx.commit()
    cnx.close()
    return query_results

#insert row containing points into database
def add_points(giver, getter, channel, points,reason):
    if points <0:
        verb = "deprived"
        verb2 = "of"
    elif points > 0:
        verb = "awarded"
        verb2 = ""
    else:
        return "https://www.youtube.com/watch?v=LQCU36pkH7c&feature=youtu.be&t=4s"
        #return "https://www.youtube.com/watch?v=M5QGkOGZubQ"
    if ("@"+giver) == getter:
        points = abs(points)*-1
        verb = "deprived"
        verb2 = "of"
    else:
        pass
    try:
        cnx = mysql.connector.connect(user='xxxx',
                              password='xxxx',
                              host ='xxxx',
                              database='xxxx')

        add_raw = ("INSERT INTO points_raw "
                    " (ID, giver, getter, channel_name, time, points, reason)"
                    "VALUES (%s,%s,%s,%s,%s,%s,%s)")
        payload = (1,giver,getter,channel,datetime.now(),points, reason)
        cur = cnx.cursor()
        cur.execute(add_raw,payload)
        cnx.commit()
        cnx.close()
        return "{0} has {1} {2} {3} {4} points".format(giver,verb,getter,verb2,abs(points))
    except Exception as e:
        return "Sorry, I can't add points right now. " + str(e)

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@async
def makeItRain(giver,channelID,points,user_id,responseURL):
    with app.app_context():
        token = config['points']['token']
        sc = SlackClient(token)
        #sc.api_call("channels.info", channel=channelID)
        memberIDs = sc.api_call("channels.info", channel=channelID)['channel']['members']
        memberIDs.remove(user_id)
        points_array = moneyOnTheFloor(len(memberIDs),points)
        memberNames = ["@"+ sc.api_call("users.info",user = x)['user']['name'] for x  in memberIDs]
        #getter ="@"+sc.api_call("users.info",user = member)['user']['name']
        member_points_list = list(zip([1]*len(memberIDs),[giver]*len(memberIDs),memberNames,[channelID]*len(memberIDs),
                                    [datetime.now()]*len(memberIDs), points_array,["rain"]*len(memberIDs)))
        cnx = mysql.connector.connect(user='xxxx',
                                  password='xxxx',
                                  host ='xxxx',
                                  database='xxxx')

        add_raw = ("INSERT INTO points_raw "
                    " (ID, giver, getter, channel_name, time, points, reason)"
                    "VALUES (%s,%s,%s,%s,%s,%s,%s)")
        payload = member_points_list
        cur = cnx.cursor()
        cur.executemany(add_raw,payload)
        cnx.commit()
        cnx.close()
        #precipitate(member_points_list)
        #member_points_dict = dict(zip(memberIDs, points_array,))
        # we'll
        #for member in member_points_dict:
            #print(member)
            #getter ="@"+sc.api_call("users.info",user = member)['user']['name']
            #add_points(giver,getter,channelID,member_points_dict[member],"")
        #requests.post(responseURL, data = {"And {0} makes it rain!!! http://i.giphy.com/y8Mz1yj13s3kI.gif".format(giver),response_type="in_channel"})
        #return "And {0} makes it rain!!! http://i.giphy.com/y8Mz1yj13s3kI.gif".format(giver)

def moneyOnTheFloor(n, r):
    numbers = list()
    h = r
    while (h != 0):
        x = randint(0,h)
        numbers.append(x)
        h = h-x
    y = n - len(numbers)
    for i in range(y):
        numbers.append(0)
    return numbers