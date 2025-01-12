from logic import PropKB
from search import a_star
import random


class TreasureAgent:
    """
    Generic treasure agent for the Treasure Finding World. It contains the basic methods for
    initialization and position updating of the agent. There are 5 possible actions for
    the agent:
       -> Up: agent moves to the upper room
       -> Down: agent moves to the lower room
       -> Left: agent moves to the left room
       -> Right: agent moves to the right room
       -> Grab: agent tries to grab the treasure in the room
    """
    
    def __init__(self, rows=4, cols=6):
        self.x, self.y = 0, 0
        self.rows = rows
        self.cols = cols
        self.movements = ['Up', 'Down', 'Left', 'Right']
    
    def update_position(self, action):
        if action == 'Up':
            self.x -= 1
        elif action == 'Down':
            self.x += 1
        elif action == 'Left':
            self.y -= 1
        elif action == 'Right':
            self.y += 1
        elif action != 'Grab':
            raise Exception("Incorrect action: %s" % action)
        
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x >= self.rows:
            self.x = self.rows - 1
        if self.y >= self.cols:
            self.y = self.cols - 1



class RandomTreasureAgent(TreasureAgent):
    """
    Random agent that performs one of the possible actions without obtaining information about
    the environment, that is, the percept is ignored and the action is random
    The <percept> supplied to the <program> method is in the form (breeze, glitter),
    which both can be True or False
    """
    
    def __init__(self, rows=4, cols=6):
        TreasureAgent.__init__(self, rows, cols)
        
    def program(self, percept):
        glitter = percept[1]
        if glitter:
            return 'Grab'
        else:
            action = random.choice(self.movements)
            self.update_position(action)
            return action



class PLTreasureAgent(TreasureAgent):
    """
    Logical agent that performs one of the possible actions depending on the values of the
    Knowledge Base using Propositional Logic.
    The <percept> supplied to the <program> method is in the form (breeze, glitter),
    which both can be True or False
    """
    
    def __init__(self, rows=4, cols=6):
        TreasureAgent.__init__(self, rows, cols)
        self.kb = PropKB()  # Knowledge Base (KB) using Propositional Logic
        self.init_kb()      # Initial knowledge for the KB
        self.plan = []      # Current plan of actions
        self.visited = []   # Already visited rooms

    # Inserts the initial knowledge to the KB of the agent. The syntax to introduce
    # rules is:
    #   self.kb.tell(<rule>)
    def init_kb(self):
        """
        Rellenar con el codigo necesario para inicializar la KB con las reglas de
        logica proposicional que relacionen la presencia de brisa en una habitacion
        x,y (es decir, Bxy), y la presencia de pozos en las proximidades (Pxy).
        """
        pass

    # Returns the existing rooms next to the room with coordinates (x, y)
    def get_adjacent_rooms(self, x, y):
        """
        Rellenar con el codigo necesario para calcular las habitaciones adyacentes
        a una dada con coordenadas (x, y). Se debe devolver una lista con las
        coordenadas de las habitaciones en formato (x, y).
        """
        return []

    # Returns a list with all the rooms that are in the fringe, that is,
    # that are directly visitable from the already visited rooms
    def fringe_rooms(self):
        rooms = []
        for x in range(self.rows):
            for y in range(self.cols):
                room = (x, y)
                if room not in rooms and self.is_fringe(room):
                    rooms.append(room)
        return rooms

    # Determines if a room (x, y) is in the fringe
    def is_fringe(self, room):
        if room in self.visited:
            return False
        x, y = room
        for (i, j) in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if (i, j) in self.visited:
                return True
        return False

    # Returns the better action for the agent given a percept of the
    # environment (Percept-Action Cycle)
    def program(self, percept):
        breeze, glitter = percept
        """
        Rellenar con el codigo necesario para implementar la funcion PL-Treasure-Agent proporcionada 
        con la practica. La funcion debe devolver una accion posible a partir de las percepciones
        actuales, que se proporcionan como parametro 
        """        
        return None
            
    
