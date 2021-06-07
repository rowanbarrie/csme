from transitions import Machine


class Conversation(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    # states = ['asleep', 'hanging out', 'hungry', 'sweaty', 'saving the world']
    states = ['start', 'end']

    transitions = [
        {'trigger': 'talk', 'source': 'start', 'dest': 'end'},
        # {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
        # {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
        # {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}
    ]

    def __init__(self, name):

        # No anonymous superheroes on my watch! Every narcoleptic superhero gets
        # a name. Any name at all. SleepyMan. SlumberGirl. You get the idea.
        self.name = name

        # What have we accomplished today?
        self.kittens_rescued = 0

        # Initialize the state machine
        self.machine = Machine(model=self,
                               states=Conversation.states,
                               transitions=Conversation.transitions,
                               initial='start')
