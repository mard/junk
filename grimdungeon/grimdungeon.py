from lib import libtcodpy as libtcod
import sys, math, textwrap, tarfile, ctypes

try:
    import audiere
except ImportError:
    if sys.platform.find('linux') == -1:
        from lib import audiere

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
#size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 43
 
#sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50
 
#parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2
 
#spell values
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12
 
FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True  #light walls or not
TORCH_RADIUS = 10
 
LIMIT_FPS = 20  #20 frames-per-second maximum

#sound settings
MIN_AMBIENCE_RANGE = 10
MAX_AMBIENCE_RANGE = 15
MIN_SECONDS_RANDOM_SOUND = 5
MAN_SECONDS_RANDOM_SOUND = 30
MIN_VOLUME_RANDOM_SOUND = 0.3
MAX_VOLUME_RANDOM_SOUND = 0.8
 
# sounds and ambience
DIR_WAV = 'wav/'
tar = tarfile.open(DIR_WAV + 'sound.tar')
tar.extractall(DIR_WAV)
d = audiere.open_device()

# general sounds
sound_general_start = d.open_file(DIR_WAV + '8-UNITOK.wav', 1)

# interface sounds
sound_button_hi = d.open_file(DIR_WAV + '8-BUTONC.wav', 1)
sound_button_lo = d.open_file(DIR_WAV + '8-BUTOND.wav', 1)

# orc sounds
sound_orc_pain = d.open_file(DIR_WAV + '8-STONB.wav', 1)
sound_orc_die = d.open_file(DIR_WAV + '8-STON0.wav', 1)
sound_orc = [sound_orc_pain, sound_orc_die]

# troll sounds
sound_troll_pain = d.open_file(DIR_WAV + '1-MGTR3.wav', 1)
sound_troll_die = d.open_file(DIR_WAV + '8-MGTR4.wav', 1)
sound_troll = [sound_troll_pain, sound_troll_die]

# player sounds
sound_player_pain = d.open_file(DIR_WAV + '8-STONC.wav', 1)
sound_player_die = d.open_file(DIR_WAV + '8-STOND.wav', 1)
sound_player_hit = d.open_file(DIR_WAV + '8-SVIH2.wav', 1)
sound_player = [sound_player_pain, sound_player_die]

# ambience sounds
sound_ambience_wind = d.open_file(DIR_WAV + '8-ATMOS1.wav', 1)
sound_ambience_forest = d.open_file(DIR_WAV + '8-VIETOR.wav', 1)
sound_ambience_swamp = d.open_file(DIR_WAV + '8-BAZIN0.wav', 1)
sound_ambience_fire = d.open_file(DIR_WAV + '8-OHEN1.wav', 1)
sound_ambience = [sound_ambience_wind, sound_ambience_forest, sound_ambience_swamp]
sound_ambience_dynamic = [sound_ambience_fire]

# spell sounds
sound_spell_fireball = d.open_file(DIR_WAV + '8-EXPLO3.wav', 1)
sound_spell_lightning = d.open_file(DIR_WAV + '8-STORM4.wav', 1)
sound_spell_confusion = d.open_file(DIR_WAV + '8-ZRIED0.wav', 1)

# random ambience soundbytes
sound_random_ambience_birds_1 = d.open_file(DIR_WAV + '8-VTAK10.wav', 1)
sound_random_ambience_birds_2 = d.open_file(DIR_WAV + '8-VTAK11.wav', 1)
sound_random_ambience_birds_3 = d.open_file(DIR_WAV + '8-VTAK02.wav', 1)
sound_random_ambience_frogs_1 = d.open_file(DIR_WAV + '8-ZABY0.wav', 1)
sound_random_ambience_frogs_2 = d.open_file(DIR_WAV + '8-ZABY2.wav', 1)
sound_random_ambience_noise_1 = d.open_file(DIR_WAV + '8-HLAS1.wav', 1)
sound_random_ambience_noise_2 = d.open_file(DIR_WAV + '8-HLAS2.wav', 1)
sound_random_ambience_dog = d.open_file(DIR_WAV + '1-PES01.wav', 1)
sound_random_ambience_hole = d.open_file(DIR_WAV + '8-HOLE00.wav', 1)
sound_random_ambience_fx = d.open_file(DIR_WAV + '8-FX03.wav', 1)
sound_random_ambience = [sound_random_ambience_birds_1, sound_random_ambience_birds_2, sound_random_ambience_birds_3, sound_random_ambience_frogs_1, sound_random_ambience_noise_1, sound_random_ambience_noise_2, sound_random_ambience_dog, sound_random_ambience_frogs_2, sound_random_ambience_hole, sound_random_ambience_fx]
 
# colors
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)
 

class Emitter:
    def __init__(self, sound, range = MAP_HEIGHT/3):
        self.sound = sound
        self.range = range
        self.volume_buffer = 0

    def setvolume(self):
        self.sound.volume = self.volume_buffer

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
 
        self.emitter = None

        #all tiles start unexplored
        self.explored = False
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
 
class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
 
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
 
class Object(object):
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    #x, y: coordinates
    #char: character used to represent object on the screen
    #name: name of the object
    #blocks: can be object stepped on?
    def __init__(self, x, y, char, name, color, blocks=False, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.ai = ai
        self.seen = False
        if(ai!=None):
            ai.owner = self

    def move(self, dx, dy):
        #move by the given amount, if the destination is not blocked
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        elif is_blocked(self.x + dx, self.y + dy):
            if not dy == 0 and not is_blocked(self.x, self.y + dy):
                self.y += dy
            elif not dx == 0 and not is_blocked(self.x + dx, self.y):
                self.x += dx
 
    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
 
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)
 
    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
 
    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
 
    def send_to_back(self):
        #make this object be drawn first, so all others appear above it if they're in the same tile.
        global objects
        objects.remove(self)
        objects.insert(0, self)
 
    def draw(self):
        #only show if it's visible to the player
        in_fov = libtcod.map_is_in_fov(fov_map, self.x, self.y)
        if (self.ai == None and self.seen) or in_fov:
            #set the color and then draw the character that represents this object at its position
            self.seen = True
            if in_fov:
                libtcod.console_set_foreground_color(con, self.color)
            else:
                libtcod.console_set_foreground_color(con, libtcod.grey)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Fighter(Object):
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, x, y, char, name, color, blocks, ai, hp, defense, power, soundset, death_function=None):
        super(Fighter, self).__init__(x=x, y=y, char=char, name=name, color=color, blocks=blocks, ai=ai)
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function
        self.soundset = soundset
        self.xp = 0
 
    def attack(self, target):
        #a simple formula for attack damage
        damage = self.power - target.defense
        sound_player_hit.stop()
        sound_player_hit.play()

        if damage > 0:
            #make the target take some damage
            message(self.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.take_damage(damage)
        else:
            message(self.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
 
    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            # self.soundset[0].stop()
            # self.soundset[0].pan = super(Fighter, self) / MAP_WIDTH
            self.soundset[0].play()
            #check for death. if there's a death function, call it
            if self.hp <= 0:
                function = self.death_function
                self.soundset[1].stop()
                self.soundset[1].play()
                if function is not None:
                    function(self)
 
    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class Corpse(Object):
    def __init__(self, x, y, char, name, color, blocks=False, ai=None):
        super(Corpse, self).__init__(x=x, y=y, char=char, name=name, color=color, blocks=blocks, ai=ai)
 
class BasicMonster:
    #AI for a basic monster.
    def take_turn(self):
        #a basic monster takes its turn. if you can see it, it can see you
        if libtcod.map_is_in_fov(fov_map, self.owner.x, self.owner.y):
 
            #move towards player if far away
            if self.owner.distance_to(player) >= 2:
                self.owner.move_towards(player.x, player.y)
 
            #close enough, attack! (if the player is still alive.)
            elif player.hp > 0:
                self.owner.attack(player)
 
class ConfusedMonster:
    #AI for a temporarily confused monster (reverts to previous AI after a while).
    def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
 
    def take_turn(self):
        if self.num_turns > 0:  #still confused...
            #move in a random direction, and decrease the number of turns confused
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
 
        else:  #restore the previous AI (this one will be deleted because it's not referenced anymore)
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)
 
 
class Item(Object):
    #an item that can be picked up and used.
    def __init__(self, x, y, char, name, color, blocks, ai, use_function=None):
        super(Item, self).__init__(x=x, y=y, char=char, name=name, color=color, blocks=blocks, ai=ai)
        self.use_function = use_function
 
    def pick_up(self):
        #add to the player's inventory and remove from the map
        if len(inventory) >= 26:
            message('Your inventory is full, cannot pick up ' + self.name + '.', libtcod.red)
        else:
            inventory.append(self)
            objects.remove(self)
            message('You picked up a ' + self.name + '!', libtcod.green)
            sound_button_lo.play()
 
    def drop(self):
        #add to the map and remove from the player's inventory. also, place it at the player's coordinates
        objects.append(self)
        inventory.remove(self)
        self.x = player.x
        self.y = player.y
        message('You dropped a ' + self.name + '.', libtcod.yellow)
 
    def use(self):
        #just call the "use_function" if it is defined
        if self.use_function is None:
            message('The ' + self.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self)  #destroy after use, unless it was cancelled for some reason
            else:
                message('Command cancelled.')
                sound_button_lo.play()
 
def is_blocked(x, y):
    #first test the map tile
    if map[x][y].blocked:
        return True
 
    #now check for any blocking objects
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True
 
    return False
 
def create_room(room):
    global map
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False
 
def create_h_tunnel(x1, x2, y):
    global map
    #horizontal tunnel. min() and max() are used in case x1>x2
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
 
def create_ambient_point(x, y, r, sound):
    global map
    map[x][y].emitter = Emitter(sound, r)

def create_v_tunnel(y1, y2, x):
    global map
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
 
def make_map():
    global map, player

    map = [[]]

    #fill map with "blocked" tiles
    map = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
 
    rooms = []
    num_rooms = 0
 
    for r in range(MAX_ROOMS):
        #random width and height
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        #random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
 
        #"Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)
 
        #run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
 
        if not failed:
            #this means there are no intersections, so this room is valid
 
            #"paint" it to the map's tiles
            create_room(new_room)
 
            #add some contents to this room, such as monsters
            place_objects(new_room)
 
            #center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()
 
            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                #all rooms after the first:
                #connect it to the previous room with a tunnel
 
                #center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms-1].center()
 
                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
 
            #finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

            #and create random ambience for this room
            create_ambient_point(new_x, new_y, libtcod.random_get_int(0, MIN_AMBIENCE_RANGE, MAX_AMBIENCE_RANGE), sound_ambience[libtcod.random_get_int(0, 0, (len(sound_ambience))-1)])

    #and finally, place hole for the next level.
    random_room = rooms[libtcod.random_get_int(0, 0, num_rooms-1)]
    place_hole(random_room)
 
def place_hole(room):
    x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
    y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
    hole = Object(x, y, chr(libtcod.CHAR_ARROW_S), 'hole', libtcod.black)
    objects.append(hole)

def place_objects(room):
    #choose random number of monsters
    num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
 
    for i in range(num_monsters):
        #choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            if libtcod.random_get_int(0, 0, 100) < 80:  #80% chance of getting an orc
                #create an orc
                monster = Fighter(x, y, 'o', 'orc', libtcod.desaturated_green, blocks=True, ai=BasicMonster(), hp=10, defense=0, power=3, soundset=sound_orc, death_function=monster_death)
            else:
                #create a troll
                monster = Fighter(x, y, 'T', 'troll', libtcod.darker_green, blocks=True, ai=BasicMonster(), hp=16, defense=1, power=4, soundset=sound_troll, death_function=monster_death)

            objects.append(monster)
 
    #choose random number of items
    num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)
 
    for i in range(num_items):
        #choose random spot for this item
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            dice = libtcod.random_get_int(0, 0, 100)
            if dice < 70:
                #create a healing potion (70% chance)
                item = Item(x, y, '!', 'healing potion', libtcod.violet, blocks=False, ai=None, use_function=cast_heal)
            elif dice < 70+10:
                #create a lightning bolt scroll (10% chance)
                item = Item(x, y, '#', 'scroll of lightning bolt', libtcod.light_yellow, blocks=False, ai=None, use_function=cast_lightning)
            elif dice < 70+10+10:
                #create a fireball scroll (10% chance)
                item = Item(x, y, '#', 'scroll of fireball', libtcod.light_yellow, blocks=False, ai=None, use_function=cast_fireball)
            else:
                #create a confuse scroll (10% chance)
                item = Item(x, y, '#', 'scroll of confusion', libtcod.light_yellow, blocks=False, ai=None, use_function=cast_confuse)
 
            objects.append(item)
            item.send_to_back()  #items appear below other objects
 
 
def render_info(x, y, total_width, text):
    libtcod.console_print_center(panel, x + total_width / 2, y, libtcod.BKGND_NONE, str(text))

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)
 
    #render the background first
    libtcod.console_set_background_color(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False)
 
    #now render the bar on top
    libtcod.console_set_background_color(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False)
 
    #finally, some centered text with the values
    libtcod.console_set_foreground_color(panel, libtcod.white)
    libtcod.console_print_center(panel, x + total_width / 2, y, libtcod.BKGND_NONE,
        name + ': ' + str(value) + '/' + str(maximum))
 
def get_names_under_mouse():
    #return a string with the names of all objects under the mouse
    mouse = libtcod.mouse_get_status()
    (x, y) = (mouse.cx, mouse.cy)
 
    #create a list with the names of all objects at the mouse's coordinates and in FOV
    names = [obj.name for obj in objects
        if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]
 
    names = ', '.join(names)  #join the names, separated by commas
    return names.capitalize()
 
def render_graphics():
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute
    global emitters
    emitters = []
    global glosnosc
    glosnosc = {}

    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
 
        #go through all tiles, and set their background color according to the FOV
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight

                if not visible:
                    #if it's not visible right now, the player can only see it if it's explored
                    if map[x][y].explored:
                        if wall:
                            libtcod.console_set_back(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_back(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                else:
                    #it's visible
                    if wall:
                        libtcod.console_set_back(con, x, y, color_light_wall, libtcod.BKGND_SET )
                    else:
                        libtcod.console_set_back(con, x, y, color_light_ground, libtcod.BKGND_SET )
                    #since it's visible, explore it
                    map[x][y].explored = True

    #draw all objects in the list, except the player. we want it to
    #always appear over all other objects! so it's drawn later.
    for object in objects:
        if object != player:
            object.draw()
    player.draw()
 
    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
 
    #prepare to render the GUI panel
    libtcod.console_set_background_color(panel, libtcod.black)
    libtcod.console_clear(panel)
 
    #print the game messages, one line at a time
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_foreground_color(panel, color)
        libtcod.console_print_left(panel, MSG_X, y, libtcod.BKGND_NONE, line)
        y += 1

    #show the player's stats
    render_bar(1, 1, BAR_WIDTH, 'HP', player.hp, player.max_hp,
        libtcod.light_red, libtcod.darker_red)

    render_bar(1, 2, BAR_WIDTH, 'XP', player.xp, 100,
        libtcod.light_blue, libtcod.darker_blue)

    render_info(1, 4, BAR_WIDTH, 'Floor: ' + str(floor))
 
    #display names of objects under the mouse
    libtcod.console_set_foreground_color(panel, libtcod.light_gray)
    libtcod.console_print_left(panel, 1, 0, libtcod.BKGND_NONE, get_names_under_mouse())

    mouse = libtcod.mouse_get_status()
    (x1, y1) = (mouse.cx, mouse.cy)

    #print str(math.atan2(player.y-y1, player.x-x1)/math.pi*180)
 
    #blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

def render_ambience():
    global ambient_recompute
    global emitters
    emitters = []
    global glosnosc
    glosnosc = {}

    if ambient_recompute:
        ambient_recompute = False
 
        #go through all tiles, and set their background color according to the FOV
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # set sound volume for ambient emitters
                if map[x][y].emitter:
                    for ambience in sound_ambience + sound_ambience_dynamic:
                        if not glosnosc.has_key(ambience):
                            glosnosc[ambience] = 0.0
                        if ambience == map[x][y].emitter.sound:
                            volume = math.hypot(x-player.x, y-player.y)/map[x][y].emitter.range
                            if volume < 1 or volume > map[x][y].emitter.volume_buffer:
                                map[x][y].emitter.volume_buffer = math.fabs(volume - 1)
                            if volume > 1:
                                map[x][y].emitter.volume_buffer = 0.0
                            if map[x][y].emitter.volume_buffer > glosnosc[ambience]:
                                glosnosc[ambience] = map[x][y].emitter.volume_buffer
        for ambience in sound_ambience + sound_ambience_dynamic:
            ambience.volume = glosnosc[ambience]
            print ambience, ambience.volume
        print "-"
 
def message(new_msg, color = libtcod.white):
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)
 
    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]
 
        #add the new line as a tuple, with the text and the color
        game_msgs.append( (line, color) )
 
 
def player_move_or_attack(dx, dy):
    global fov_recompute
    global ambient_recompute
 
    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy
 
    #try to find an attackable object there
    target = None
    for object in objects:
        if object.x == x and object.y == y:
            if isinstance(object, Fighter):
                target = object
                break
            elif isinstance(object, Object) and object.name == 'hole':
                message('You found a hole. Press [n] to proceed to next floor.')
 
    #attack if target found, move otherwise
    if target is not None:
        player.attack(target)
    else:
        player.move(dx, dy)
        fov_recompute = True
        ambient_recompute = True
 
 
def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
 
    #calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_height_left_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    height = len(options) + header_height
 
    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
 
    #print the header, with auto-wrap
    libtcod.console_set_foreground_color(window, libtcod.white)
    libtcod.console_print_left_rect(window, 0, 0, width, height, libtcod.BKGND_NONE, header)
 
    #print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_left(window, 0, y, libtcod.BKGND_NONE, text)
        y += 1
        letter_index += 1
 
    #blit the contents of "window" to the root console
    x = SCREEN_WIDTH/2 - width/2
    y = SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
 
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
 
    #convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None
 
def inventory_menu(header):
    #show a menu with each item of the inventory as an option
    sound_button_hi.play()
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]
 
    index = menu(header, options, INVENTORY_WIDTH)
 
    #if an item was chosen, return it
    sound_button_lo.play()
    if index is None or len(inventory) == 0: return None
    return inventory[index]

def handle_input():
    key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
    mouse = libtcod.mouse_get_status()
    (x, y) = (mouse.cx, mouse.cy)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  #exit game

    elif chr(key.c) == 'r':
        reset()

    if game_state == 'playing':
        #movement keys
        if key.vk == libtcod.KEY_KP8 or key.vk == libtcod.KEY_UP:
            player_move_or_attack(0, -1)
 
        elif key.vk == libtcod.KEY_KP2 or key.vk == libtcod.KEY_DOWN:
            player_move_or_attack(0, 1)
 
        elif key.vk == libtcod.KEY_KP4 or key.vk == libtcod.KEY_LEFT:
            player_move_or_attack(-1, 0)
 
        elif key.vk == libtcod.KEY_KP6 or key.vk == libtcod.KEY_RIGHT:
            player_move_or_attack(1, 0)

        elif key.vk == libtcod.KEY_KP7:
            player_move_or_attack(-1, -1)

        elif key.vk == libtcod.KEY_KP9:
            player_move_or_attack(1, -1)

        elif key.vk == libtcod.KEY_KP1:
            player_move_or_attack(-1, 1)

        elif key.vk == libtcod.KEY_KP3:
            player_move_or_attack(1, 1)

        #if nearest player neighbor is clicked
        elif mouse.lbutton:
            angle = math.atan2(player.y-y, player.x-x)/math.pi*180
            if angle > 157.5:
                player_move_or_attack(1, 0)
            elif 157.5 > angle > 112.5:
                player_move_or_attack(1, -1)
            elif 112.5 > angle > 67.5:
                player_move_or_attack(0, -1)
            elif 67.5 > angle > 22.5:
                player_move_or_attack(-1, -1)
            elif 22.5 > angle > -22.5:
                player_move_or_attack(-1, 0)
            elif -22.5 > angle > -67.5:
                player_move_or_attack(-1, 1)
            elif -67.5 > angle > -112.5:
                player_move_or_attack(0, 1)
            elif -112.5 > angle > -157.5:
                player_move_or_attack(1, 1)
            elif -157.5 > angle:
                player_move_or_attack(1, 0)
        else:
            #test for other keys
            key_char = chr(key.c)

            if key_char == 'n':
                for object in objects:  #look for an item in the player's tile
                    if object.x == player.x and object.y == player.y and isinstance(object, Object):
                        if object.name == 'hole':
                            next_level()
                            break
                        else:
                            no_hole = True
                if no_hole == True:
                    message('There is no hole down there.')

            if key_char == 'g':
                #pick up an item
                for object in objects:  #look for an item in the player's tile
                    if object.x == player.x and object.y == player.y and isinstance(object, Item):
                        object.pick_up()
                        break
 
            if key_char == 'i':
                #show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()
 
            if key_char == 'd':
                #show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()
 
            return 'didnt-take-turn'
 
def reset():
    global con
    init_start()
    init_mechanics()    
    libtcod.console_clear(con)
    message('Map reset\'d.')

def next_level():
    global con, floor
    floor += 1
    init_mechanics()
    libtcod.console_clear(con)
    message('You have entered the next level.')

def player_death(player):
    #the game ended!
    global game_state
    message('You died! Press [r] to reset.', libtcod.red)
    game_state = 'dead'
    sound_player_die.play()
 
    #for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = libtcod.dark_red
 
def monster_death(monster):
    #remove it and create a nasy corpse! it doesn't block, can't be
    #attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', libtcod.orange)
    objects.remove(monster)
    corpse=Corpse(x=monster.x, y=monster.y, name='remains of ' + monster.name, char='%', color=libtcod.dark_red, blocks=False, ai=None)
    objects.append(corpse)
    corpse.send_to_back()
 
def target_tile(max_range=None):
    #return the position of a tile left-clicked in player's FOV (optionally in a range), or (None,None) if right-clicked.
    while True:
        #render the screen. this erases the inventory and shows the names of objects under the mouse.
        render_graphics()
        libtcod.console_flush()
 
        key = libtcod.console_check_for_keypress()
        mouse = libtcod.mouse_get_status()  #get mouse position and click status
        (x, y) = (mouse.cx, mouse.cy)
 
        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return (None, None)  #cancel if the player right-clicked or pressed Escape
 
        #accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
        if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and
            (max_range is None or player.distance(x, y) <= max_range)):
            return (x, y)
 
def target_monster(max_range=None):
    #returns a clicked monster inside FOV up to a range, or None if right-clicked
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  #player cancelled
            return None
 
        #return the first clicked monster, otherwise continue looping
        for obj in objects:
            if obj.x == x and obj.y == y and isinstance(obj, Fighter) and obj != player:
                return obj
 
def closest_monster(max_range):
    #find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range
 
    for object in objects:
        if isinstance(object, Fighter) and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            #calculate distance between this object and the player
            dist = player.distance_to(object)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = object
                closest_dist = dist
    return closest_enemy
 
def cast_heal():
    #heal the player
    if player.hp == player.max_hp:
        message('You are already at full health.', libtcod.red)
        return 'cancelled'
    message('Your wounds start to feel better!', libtcod.light_violet)
    player.heal(HEAL_AMOUNT)
 
def cast_lightning():
    #find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(LIGHTNING_RANGE)
    if monster is None:  #no enemy found within maximum range
        message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'
 
    #zap it!
    message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
        + str(LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
    monster.take_damage(LIGHTNING_DAMAGE)
    sound_spell_lightning.play()
 
def cast_fireball():
    global sound_ambience_fire
    #ask the player for a target tile to throw a fireball at
    message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    message('The fireball explodes, burning everything within ' + str(FIREBALL_RADIUS) + ' tiles!', libtcod.orange)
    sound_spell_fireball.play()
    create_ambient_point(x, y, FIREBALL_RADIUS+2, sound_ambience_fire)
 
    for obj in objects:  #damage every fighter in range, including the player
        if obj.distance(x, y) <= FIREBALL_RADIUS and isinstance(obj, Fighter):
            message('The ' + obj.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hit points.', libtcod.orange)
            obj.take_damage(FIREBALL_DAMAGE)
 
def cast_confuse():
    #ask the player for a target to confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None: return 'cancelled'
 
    #replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster  #tell the new component who owns it
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', libtcod.light_green)
    sound_spell_confusion.play()

def random_frame():
    return libtcod.random_get_int(0, LIMIT_FPS*MIN_SECONDS_RANDOM_SOUND, LIMIT_FPS*MAN_SECONDS_RANDOM_SOUND)

def render_random_ambient_sounds():
    global frame_counter, next_random_frame
    frame_counter = frame_counter + 1
    if next_random_frame == frame_counter:
        index = libtcod.random_get_int(0, 0, (len(sound_random_ambience))-1)
        sound_random_ambience[index].volume = libtcod.random_get_float(0, MIN_VOLUME_RANDOM_SOUND, MAX_VOLUME_RANDOM_SOUND)
        sound_random_ambience[index].play()
        next_random_frame = random_frame()
        frame_counter = 0

def init_ambience():
    sounds = sound_ambience + sound_ambience_dynamic
    for sound in sounds:
        sound.repeating = 1
        sound.volume = 0.0
        sound.play()

#############################################
# Initialization & Main Loop
#############################################

def init_start():
    global floor
    global player
    global game_msgs
    global objects
    global inventory

    #create object representing the player
    player = Fighter(x=0, y=0, char='@', name='player', color=libtcod.white, blocks=True, ai=None, hp=50, defense=2, power=5, soundset=sound_player, death_function=player_death)

    #the list of objects with just the player
    objects = [player]

    #empty inventory list
    inventory = []

    #create the list of game messages and their colors, starts empty
    game_msgs = []

    floor = 1

def init_mechanics():
    global player
    global objects
    global fov_recompute
    global fov_map
    global ambient_recompute
    global game_state
    global frame_counter
    global next_random_frame

    objects = [player]

    #generate map (at this point it's not drawn to the screen)
    make_map()
 
    #create the FOV map, according to the generated map
    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].blocked, not map[x][y].block_sight)

    fov_recompute = True
    ambient_recompute = True
    game_state = 'playing'
    player_action = None

    frame_counter = 0
    next_random_frame = random_frame()

init_start()
init_mechanics()
init_ambience()

#libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

#a warm welcoming message!
message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)
sound_general_start.play()

while not libtcod.console_is_window_closed():

    #render the screen
    render_graphics()

    #recompute ambient sound voumes
    render_ambience()

    #random ambient sounds
    render_random_ambient_sounds()

    libtcod.console_flush()
 
    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()
 
    #handle keys and exit game if needed
    player_action = handle_input()
    if player_action == 'exit':
        break
 
    #let monsters take their turn
    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for object in objects:
            if object.ai:
                object.ai.take_turn()