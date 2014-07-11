example_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

def create_data_structure(string_input):
#   Takes a standardized string and creates a network dictionary containing a 
#   user key, and two separate arrays for values. {user: [friends], [games]}
    #   Initializes a new, empty network data structure.
    network = {}

	# bool to stop searching when no more periods are found
    search = True

    # keeps track of the string index to search from
    search_point = 0

    while (search == True):
        # if there is no period remaining then stop searching
        if string_input.find(".", search_point) == -1:
            search = False
            break

        # initialize the user arrays
        user_friends = []
        user_games = []
 
		# find the name of the user
        name_end = string_input.find(" ", search_point)
        user = string_input[search_point:name_end]

        # find the user's friends, add to the array, update the search point
        friends, point = segment_parser(string_input[search_point:], [",", " "], "to", ".")
        for each in friends:
            user_friends.append(each)
        search_point += point

        # find the user's games, add to the array, update the search point
        games, point = segment_parser(string_input[search_point:], [","],  "play", ".")
        for each in games:
            # if the first character of an entry is a space, ignore the space
            if each[0] == " ":
                user_games.append(each[1:])
            else:
                user_games.append(each)
        search_point += point

        # add the user entry to the network
        network[user] = [user_friends, user_games]

    return network

def get_connections(network, user):
#   A list of all connections the user has. If the user has no connections, 
#   an empty list is returned. If the user is not in network, None is returned.  

    if user not in network:
        return None

    connections = network[user][0]
    if len(connections) == 0:
        return []
    else:
        return connections

def add_connection(network, user_A, user_B):
#   Adds a connection from user_A to user_B. If one or both users does not
#   exist in the network then False is returned. If user_B is already in 
#   user_A's connections then the network is returned untouched.

    if (user_A not in network) and (user_B not in network):
        return False

    connections = network[user_A][0]
    if user_B not in connections:
        connections.append(user_B)
    return 

def add_new_user(network, user, games):
#   Creates a new user profile and adds that user to the network, along with
#   any game preferences specified in games. The user has no connections to
#   begin with.    

    # if the user is already in the network, update their games
    if user in network:
        network[user][1] = games
    # create a new user with no friends and specified games
    else:
        network[user] = [[], games]
    return network

def get_secondary_connections(network, user):
#   Finds all the secondary connections, i.e. connections of connections, of a 
#   given user. 

    if user not in network:
        return None

    connections = network[user][0]

    secondary_connections = []

    for friend in connections:
        connections_friends = get_connections(network, friend)
        for friends_friend in connections_friends:
            if friends_friend not in secondary_connections:
                secondary_connections.append(friends_friend)
    return secondary_connections

def connections_in_common(network, user_A, user_B):
#   Finds the number of people that user_A and user_B have in common.

    if (user_A not in network) or (user_B not in network):
        return False

    common = []
    a_friends = get_connections(network, user_A)
    b_friends = get_connections(network, user_B)
    for friend in a_friends:
        if friend in b_friends:
            common.append(friend)

    return len(common)

def get_connections(network, user):
#   A list of all connections the user has. If the user has no connections, 
#   an empty list is returned. If the user is not in network, None is returned.  

    if user not in network:
        return None

    connections = network[user][0]
    if len(connections) == 0:
        return []
    else:
        return connections

def path_to_friend(network, user_A, user_B):
#   Calls a recursive function with one more argument.

    return path_to_friend_2(network, user_A, user_B, [], [])

def path_to_friend_2(network, user_A, user_B, history, output):
#   Finds a connection path from user_A to user_B using recursion.

    # add the current user to the output
    output.append(user_A)

    # add the connection to history in order to avoid infinite loops
    history.append(user_A)

    # get the connections of the current user
    connections = get_connections(network, user_A)

    # if a user has no connections, then remove the user from the output and break
    if len(connections) == 0:
        output.remove(user_A)
        return None

    # loop through each connection, checking for the second user
    for each in connections:

        # if the connection is the user we are looking for, add it to output
        if each == user_B:
            output.append(each)
            return output

        # if this connection has not already been checked, check its own connections
        elif each not in history:
            path = path_to_friend_2(network, each, user_B, history, output)

            # as long as this path has more connections it's possible it's connectected to
            # user_B
            if path != None:
                return output

    # since no connection found remove the current user from the output array
    output.remove(user_A)

    return None

def suggested_friend_and_game(network, user):
#   Returns a suggestion for a friend and a game based on other user data.
    
    # create dictionarys with all relevant possible friends and games
    suggested_friends = get_hits(network, user, "Friend")
    suggested_games = get_hits(network, user, "Game")

    # get the most relevant entry
    suggested_friend = get_max_dictionary(suggested_friends)
    suggested_game = get_max_dictionary(suggested_games)

    return suggested_friend, suggested_game

# HELPER FUNCTIONS
def segment_parser(source, splitlist, start_word, end_word):
#   Takes a string input, and two key words.
#   Returns the desired segment and the end point of search

    start = source.find(start_word) + len(start_word) + 1
    end = source.find(end_word)
    segment = (split_string(source[start:end], splitlist))

    return segment, end+1

def split_string(source, splitlist):
#   Takes a string, and splits it according to the splitlist

    output = []
    atsplit = True
    
    for char in source:
        if char in splitlist:
            atsplit = True
            
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            
            else:
                output[-1] += char           
    return output

def get_hits(network, user, interest):
#   Takes a user and interest and returns a dictionary with suggestions.

    # ensure that the interest is a valid one and point to the right data location
    if interest == "Friend":
        array = 0
    elif interest == "Game":
        array = 1   
    else:
        return None  

    # create a dictionary to store possible matches and their number of occurances
    output= {}

    # store the user's interest
    user_interest = network[user][array]

    # loop through each person in the network
    for person in network:
        person_interest = network[person][array]

        # don't need to check the user itself
        if person == user:
            break

        for interest in user_interest:
            if interest in person_interest:
                for person_interest in person_interest:
                    # add a new entry if it doesn't already exist
                    if person_interest not in output:
                        output[person_interest] = 1
                    #otherwise increment the key value by 1 
                    else:
                        output[person_interest] += 1
    return output

def get_max_dictionary(dictionary):
#   Takes a dictioary and returns the key with the largest value

    # create separate lists for keys and values
    v = list(dictionary.values())
    k = list(dictionary.keys())

    return k[v.index(max(v))]


# TEST
net = create_data_structure(example_input)
print net
print path_to_friend(net, 'John', 'Ollie')
print get_connections(net, "Debra")
print add_new_user(net, "Debra", []) 
print add_new_user(net, "Nick", ["Seven Schemers", "The Movie: The Game"]) # True
print get_connections(net, "Mercedes")
print add_connection(net, "John", "Freda")
print get_secondary_connections(net, "Mercedes")
print connections_in_common(net, "Mercedes", "John")

print suggested_friend_and_game(net, "John")

