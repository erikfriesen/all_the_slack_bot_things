@app.route('/dicks/<how_many_disks>')
def dicks(how_many_disks):
    d = "8====D"
    bag_of_dicks =[]
    for x in range(int(how_many_disks)):
        bag_of_dicks.append(d)
    string_dicks = ",".join(bag_of_dicks)
    return '{"dicks":{'+ string_dicks+'}}'
