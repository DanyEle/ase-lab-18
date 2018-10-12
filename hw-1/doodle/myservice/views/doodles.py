from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.poll import Poll, NonExistingOptionException, UserAlreadyVotedException

doodles = JsonBlueprint('doodles', __name__)

_ACTIVEPOLLS = {} # list of created polls
_POLLNUMBER = 0 # index of the last created poll


@doodles.route('/doodles', methods=['GET', 'POST'])
def all_polls():
    if request.method == 'POST':
        try:
            result = create_doodle(request)
        #in case the user entered some invalid input
        except NonExistingOptionException:
            abort(400)  # Bad Request

    elif request.method == 'GET':
        result = get_all_doodles(request)
    
    return result


@doodles.route('/doodles/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def single_poll(id):
    global _ACTIVEPOLLS
    result = ""
    exist_poll(id) # check if the Doodle is an existing one

    #retrieves a poll identified by the ID provided
    if request.method == 'GET':
        result = jsonify(_ACTIVEPOLLS[id].serialize())
    elif request.method == 'DELETE': 
        #firstly, get the winners of the poll being invoked
        result = jsonify(winners=_ACTIVEPOLLS[id].get_winners())
        #now, actually need to delete the poll with the index provided
        del(_ACTIVEPOLLS[id])


    elif request.method == 'PUT': 
        result = vote(id, request)


    return result

@doodles.route('/doodles/<int:id>/<person>', methods=['GET', 'DELETE'])
def person_poll(id, person):
    #check for the doodle to actually exist
    exist_poll(id)

    #Fine, the specified doodle does exist
    if request.method == 'GET':
        result = jsonify(votedoptions=_ACTIVEPOLLS[id].get_voted_options(person))

    if request.method == 'DELETE':
        cur_poll = _ACTIVEPOLLS[id]

        voted_options = cur_poll.get_voted_options(person)

        #and actually return False if no vote was found for this person!
        if len(voted_options) == 0:
            result = jsonify(removed=False)
        else:
            #only delete votes if the person has actually voted
            result = jsonify(removed=True)
            cur_poll.delete_voted_options(person)

    return result
       

def vote(id, request):
    result = ""
    request_data = request.get_json()


    person = request_data['person']
    option = request_data['option']
    # invalid input type provided
    if type(person) is not str:
        #invalid data structure provided for 'person'
        abort(400)
    if type(option) is not str:
        #invalid data structure for 'option'
        abort(400)

    try:
        # actually cast the vote
        _ACTIVEPOLLS[id].vote(person, option)
        result = jsonify(winners=_ACTIVEPOLLS[id].get_winners())

    except UserAlreadyVotedException:
        abort(400) # Bad Request
    #voting for a non-existing option
    except NonExistingOptionException:
        abort(400)

    return result


def create_doodle(request):
    global _ACTIVEPOLLS, _POLLNUMBER

    request_data = request.get_json()
    title = request_data['title']
    options = request_data['options']


    if not type(options) is list:
        #invalid data structure as options.
        abort(400)

    if not type(title) is str:
        #invalid data structure as title
        abort(400)
    #everything alright, then go ahead and actually create the poll!

    #now take the options and form an 'options dictionary'
    options_dictionary = {}
    empty_list = []

    for option in options:
        options_dictionary[option] = empty_list

    _POLLNUMBER += 1
    new_poll = Poll(_POLLNUMBER, title, options_dictionary)

    #now add the newly created object to the list of polls
    #the ID is the cur_poll_number. We'll need to number to retrieve the poll later on
    _ACTIVEPOLLS[_POLLNUMBER] = new_poll

    #finally, increment the poll number, but return the previous one

    return jsonify({'pollnumber': _POLLNUMBER})

#need to retrieve all current doodles as a list
def get_all_doodles(request):
    global _ACTIVEPOLLS
    return jsonify(activepolls=[e.serialize() for e in _ACTIVEPOLLS.values()])


def exist_poll(id):
    if int(id) > _POLLNUMBER:
        abort(404) # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(id in _ACTIVEPOLLS):
        abort(410) # error 410: Gone, i.e. it existed but it's not there anymore