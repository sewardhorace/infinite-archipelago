'''
steps:
1. Setup
	Define boundaries: (2d array, 256 X 256 - is this needed?)
	Create a room of random dimensions between 10 and 100
	Randomly place the room within the boundaries - discard if it overlaps an existing room
	Repeat until 10 rooms are placed in the boundaries
3. Create corridors to join the rooms/neighboring corridors
	Choose a random starting point - a sector join point or any point of the edge of a random room
	Choose a random ending point - a sector join point or any point on the edge of another random room
	Find the path between the two points
  (Limit 4 doors in a room)
	Repeat until all sector join points and rooms have been connected at least once (one room/sector join at a time)
  Repeat until all areas are reachable
	Unify overlapping corridors (including connecting corridors to neighboring sectors)
4. Translate locations based on coordinates of sector
5. Store data
	Every discrete corridor needs to know its draw description and neighboring rooms (edges)
	Every room needs to know its upper left origin and height/width and the coordinates of its neighboring corridors
'''
import random, math

BOUNDS = width, height = 50, 50 #grid of 50 5*5 squares
BUFFER = 1
#TODO: make sector a class that has the properties of bounds and buffer

def random_from_curve(mean:int, minimum:int, maximum:int):
  std_deviation = (maximum - mean) / 3
  num = random.gauss(mean, std_deviation)
  if num < minimum:
      num = minimum
  if num > maximum:
      num = maximum
  return int(num)

# def point_inside_rect(x, y, rect):
#   if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
#     return True
#   else:
#     return False

def distance(point_a, point_b):
  return math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])

class Room:
  def __init__(self, bounds):
    self._dimensions = self.__set_dimensions()
    self._origin = self.__set_origin(bounds)

  def __set_dimensions(self):
    width = random_from_curve(10, 2, 20)
    height = random_from_curve(10, 2, 20)
    return width, height

  def __set_origin(self, bounds, buffer=BUFFER):
    x = random.randint(buffer, bounds[0] - self._dimensions[0] - buffer)
    y = random.randint(buffer, bounds[1] - self._dimensions[1] - buffer)
    return x, y

  @property
  def x(self):
    return self._origin[0]

  @property
  def y(self):
    return self._origin[1]

  @property
  def width(self):
    return self._dimensions[0]

  @property
  def height(self):
    return self._dimensions[1]

  @property
  def top(self):
    return self._origin[1]

  @property
  def bottom(self):
    return self._origin[1] + self._dimensions[1]

  @property
  def left(self):
    return self._origin[0]

  @property
  def right(self):
    return self._origin[0] + self._dimensions[0]

  @property
  def topleft(self):
    return self._origin

  @property
  def topright(self):
    return self._origin[0] + self._dimensions[0], self._origin[1]

  @property
  def bottomleft(self):
    return self._origin[0], self._origin[1] + self._dimensions[1]

  @property
  def bottomright(self):
    return self._origin[0] + self._dimensions[0], self._origin[1] + self._dimensions[1]

  @property
  def center(self):
    return self._origin[0] + self._dimensions[0]/2, self._origin[1] + self._dimensions[1]/2

  def nearest_side(self, point):
    north = abs(point[1] - self.top)
    south = abs(point[1] - self.bottom)
    east = abs(point[0] - self.right)
    west = abs(point[0] - self.left)
    nearest = max([north, south, east, west])
    if nearest == north:
      return 'north'
    elif nearest == south:
      return 'south'
    elif nearest == east:
      return 'east'
    elif nearest == west:
      return 'west'

class Door:
  def __init__(self):
    pass

class Corridor:
  def __init__(self):
    pass


class Sector:
  def __init__(self, neighboring__points=None):
    self.rooms = self.__generate_rooms()

  def __generate_rooms(self):
    rooms = []
    while len(rooms) < 10:
      new_room = Room(BOUNDS)
      colliding = False
      for room in rooms:
        if self.__check_room_collision(new_room, room):
          colliding = True
          break
      if colliding == False:
        rooms.append(new_room)
    return rooms

  def __check_room_collision(self, room_a, room_b, buffer=BUFFER):
    #TODO: FATAL! two rooms can overlap in a cross shape
    if (room_a.right + buffer < room_b.left or 
        room_a.left - buffer > room_b.right or 
        room_a.top - buffer > room_b.bottom or 
        room_a.bottom + buffer < room_b.top):
      return False
    else:
      return True

  def __nearest_rooms(self, room_main, amt_rooms=3):
    rooms = self.rooms.copy()
    rooms.remove(room_main)

    rooms_nearest = []
    while len(rooms_nearest) < amt_rooms:
      room_nearest = rooms[0]
      for room in rooms:
        dist_new = distance(room_main.center, room.center)
        dist_old = distance(room_main.center, room_nearest.center)
        if dist_new < dist_old:
          room_nearest = room

      rooms_nearest.append(room_nearest)
      rooms.remove(room_nearest)
    return rooms_nearest
      
  def __generate_doors(self):
    #http://www.python-course.eu/graphs_python.php
    doors = []
    for node in graph:
      for neighbour in graph[node]:
        doors.append((node, neighbour))
    return doors

  def __merge_corridors(self, corridor_a, corridor_b):
    pass

  def __connect_rooms(self, room_a, room_b):
    '''
    main method

    get room and 3 nearest rooms
    for each pair, 
      create a corridor object and link the rooms and corridors in a graph structure
      create a door for edge in the graph, 
        located at a random point on the nearest side of each room
      determine the path of each corridor (from door to door) - A* algorithm
      merge any overlapping corridors
    
    choose another random room that is not yet part of the graph
    repeat until all rooms are part of the graph

    graph = {}
    while !all(room in graph for room in rooms):
      random.shuffle(rooms)
      room = rooms.pop()
      amt_connections = random.randint(1, 3)
      nearest_rooms = self.__nearest_rooms(room, amt_connections)
      corridors = [Corridor() for i in range(amt_connections)]
      if room in graph:

      else:
        graph[room] = corridors
      for i in range(amt_connections):
        graph[nearest_rooms[i]] = [corridors[i]]
        graph[corridors[i]] = []
      graph[corridor]
    
    '''
    pass