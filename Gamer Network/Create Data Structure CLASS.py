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

class Network:
    def __init__(self):
        self.network = {}

    def __call__(self):
    #   Print out the network dictionary.

        for each in self.network:
            print "%s:\t%s, %s" %(each, self.network[each][0], self.network[each][1])

    def create_data_structure(self, string_input):
    #   Takes a standardized string and creates a network dictionary containing a 
    #   user key, and two separate arrays for values. {user: [friends], [games]}

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
            friends, point = self.segment_parser(string_input[search_point:], "to", ".")
            for each in friends:
                user_friends.append(each)
            search_point += point

            # find the user's games, add to the array, update the search point
            games, point = self.segment_parser(string_input[search_point:], "play", ".")
            for each in games:
                user_games.append(each)
            search_point += point

            # add the user entry to the network
            self.network[user] = [user_friends, user_games]

        return self.network

    def get_connections(self, user):
    #   A list of all connections the user has. If the user has no connections, 
    #   an empty list is returned. If the user is not in network, None is returned.  

        # if user not in self.network:
        #     print "WRONG"
        #     return None

        connections = self.network[user][0]
        if len(connections) == 0:
            return []
        else:
            return connections

    def add_connection(self, user_A, user_B):
    #   Adds a connection from user_A to user_B. If one or both users does not
    #   exist in the network then False is returned. If user_B is already in 
    #   user_A's connections then the network is returned untouched.

        if (user_A not in self.network) and (user_B not in self.network):
            return False

        connections = self.network[user_A][0]
        if user_B not in connections:
            connections.append(user_B)
        return 


    def add_new_user(self, user, games):
    #   Creates a new user profile and adds that user to the network, along with
    #   any game preferences specified in games. The user has no connections to
    #   begin with.    

        if user in self.network:
            for each in games:
                previous_games = self.network[user][1]
                if each not in previous_games:
                    previous_games.append(each)
        else:
            self.network[user] = [[], games]
            return 

    def get_secondary_connections(self, user):
    #   Finds all the secondary connections, i.e. connections of connections, of a 
    #   given user. 

        if user not in self.network:
            return None

        connections = self.network[user][0]

        secondary_connections = []

        for friend in connections:
            connections_friends = self.get_connections(friend)
            for friends_friend in connections_friends:
                if friends_friend not in secondary_connections:
                    secondary_connections.append(friends_friend)
        return secondary_connections

    def connections_in_common(self, user_A, user_B):
#   Finds the number of people that user_A and user_B have in common.

        if (user_A not in self.network) or (user_B not in self.network):
            return False

        common = []
        a_friends = self.get_connections(user_A)
        b_friends = self.get_connections(user_B)
        for friend in a_friends:
            if friend in b_friends:
                common.append(friend)
        return len(common)


    def path_to_friend(network, user, connection):
    # your RECURSIVE solution here!
        return None

    # HELPER FUNCTIONS
    def segment_parser(self, source, start_word, end_word):

        # takes a string input, and two key words
        # returns the desired segment and the end point of search

        start = source.find(start_word) + len(start_word) + 1
        end = source.find(end_word)
        segment = (self.split_string(source[start:end], [",", " "]))

        return segment, end+1

    def split_string(self, source, splitlist):

        # takes a string, and splits it according to the splitlist

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


net = Network()
net.create_data_structure(example_input)

