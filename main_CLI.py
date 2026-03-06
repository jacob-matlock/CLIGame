#==================================================
# IMPORTS
#==================================================
import os
import textwrap
import requests

#==================================================
# CLASS DEFINITION
#==================================================

class Room:
    """
    This class enables the creation of a Room object that is used throughout the game. 
    """
    def __init__(self, name, description):
        """
        Parameters:
        name - a string that holds the name of the object 
        description - a string that holds text that is displayed to the user when entering a room
        exits - a dictionary that holds the exits with keys north, east, south, and west
        items - a list of strings that represent items in the room the user can pick up
        secrets - a dictionary that holds strings as the values that display additional information when prompted
        monsters - a list of strings that represent monsters the user must fight in the room
        visited - a boolean that tracks if the user has been in the room or not
        
        coordinates - a tuple that contains the location of the room on the map
             - defined in the random room placement microservice
        alt_description - a string that is defined for some rooms that must have a change in description for any reason
             - example: when a monster is slain, the description of the room if the user re-enters that room afterwards
        """
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.secrets = {}
        self.monsters = []
        self.visited = False

#==================================================
# GET ROOMS FROM MICROSERVICE
#==================================================
rooms_dict = requests.get(f"http://localhost:1400/room-layout")

#==================================================
# USER ACTION FUNCTIONS
#==================================================

def create_map(current_room):
    clear_screen()

    def mark(room, accessible = True):
        if current_room == room:
            return f"[@] {room.name}"
        elif not accessible:
            return f"[X] {room.name}"
        else:
            return f"[ ] {room.name}"

    print("                " + mark(guard_chamber))
    print("                     |")
    print("   " + mark(rope_exit) + " ---- " + mark(cell_hall))
    print("                     |")

    print("     [X] Cell 1      |      [X] Cell 6")
    print("     [X] Cell 2      |      [X] Cell 7")
    print("     [X] Cell 3      |      [X] Cell 8")
    print("     [X] Cell 4      |      [X] Cell 9")
    print("     [X] Cell 5      |      " + mark(cell_10))
    print("                     |")
    print("                " + mark(cell_11))
    print()
    input("Press Enter to continue...")
    clear_screen()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pick_up_item(command, current_room, inventory):
    items = current_room.items
    if current_room == cell_11:
        if "bucket" in command or ("bucket" in command and "of" in command and "water" in command):
            inventory.append("bucket of water")
            current_room.items.remove("bucket of water")
            print("You picked up the bucket of water. You spill some onto your foot, so your shoe squelches when you take a step.")
            return True
        if "water" in command and "bucket" not in command:
            print("You scoop some water into your hands and raise it to your lips to drink. Before you take a sip, you notice a foul ")
            print("stench coming from the water, so you let it dribble through your fingers and dry your hands on the"
                  "thin cot blanket.")
            return True
        if ("keys" in command or ("jail" in command and "keys" in command)) and "guard" in current_room.monsters:
            return False
        elif ("keys" in command or ("jail" in command and "keys" in command)) and "guard" not in current_room.monsters:
            print("You picked up the jail keys")
            inventory.append("jail keys")
            current_room.items.remove("jail keys")
            print("You picked up the jail keys. There are 11 keys but 9 are rusted through, leaving only two in working condition")
            return True
    elif current_room == cell_10:
        if "signet" in command or "ring" in command or ("signet" in command and "ring" in command):
            inventory.append("signet ring")
            current_room.items.remove("signet ring")
            print("You picked up the signet ring.")
            return
    elif current_room == sword_room:
        if ("sword" in command or "blade" in command) and "signet ring" in inventory:
            inventory.append("sword")
            current_room.items.remove("sword")
            current_room.description = current_room.alt_description
            print("You slide the signet ring off your finger and see the same crest on it as on the sword. You push the"
                  " ring into the hole in the pedestal and the ring sinks further into it as if by magic. As you take "
                  "the shining sword, you find that you can suddenly read the words on the pedestal. The sentence reads:"
                  " 'It's dangerous to go alone, take this!'")
            return
    elif current_room == wand_room:
        if "wand" in command:
            inventory.append("wand")
            current_room.items.remove("wand")
            current_room.description = current_room.alt_description
            print("You picked up the wand.")
    for item in items:
        if item in command:
            inventory.append(item)
            current_room.items.remove(item)
            print(f"You picked up the {item}.")
            return True
    return False

def change_rooms(command, current_room):
    if type(command) == str:
        if "north" == command:
            direction = "north"
        elif "east" in command:
            direction = "east"
        elif "south" in command:
            direction = "south"
        elif "west" in command:
            direction = "west"
        else:
            print("Invalid direction. Please try again.")
            return current_room
    elif type(command) == list:
        if "north" in command:
            direction = "north"
        elif "east" in command:
            direction = "east"
        elif "south" in command:
            direction = "south"
        elif "west" in command:
            direction = "west"
        else:
            print("Invalid direction. Please try again.")
            return current_room

    if current_room.exits[direction] is not None:
        new_room = current_room.exits[direction]
        print(textwrap.fill(new_room.description, width=120))
        new_room.visited = True
        return new_room
    else:
        print("You can't go that way.")

def room_secret(current_room):
    if current_room.secrets is not None:
        for item in current_room.secrets:
            wrapped_secret = textwrap.fill(current_room.secrets[item], width=120)
            print(wrapped_secret)
        current_room.secrets = None

def view_map(current_room, inventory):
    if "parchment" in inventory and "ink" in inventory:
        create_map(current_room)
    else:
        if "parchment" in inventory and "ink" not in inventory:
            print("You need ink to draw a map.")
        elif "parchment" not in inventory and "ink" in inventory:
            print("You need parchment to draw a map.")
        else:
            print("You need both parchment and ink to draw a map.")
    pass

def view_inventory(current_room, inventory, stats):
    clear_screen()
    for item in inventory:
        print(item)

    print("Press enter to continue playing...")
    input()

    clear_screen()
    print(current_room.description)
    get_command(current_room, inventory, stats)

def view_stats(current_room, inventory,stats):
    clear_screen()

    for item in stats:
        print(item)

    print("Press enter to continue playing...")
    input()

    clear_screen()
    get_command(current_room, inventory, stats)

def attack(current_room, inventory, stats, command):
    if current_room.monsters is None:
        print("There are no enemies in this room.")
    elif "sword" not in inventory and "wand" not in inventory:
        print("You have no weapons. You cannot attack.")
        get_command(current_room, inventory, stats)
    elif "sword" in inventory and "wand" not in inventory:
        print(f"You slay the {current_room.monsters} with your sword.")
        current_room.monsters = None
        stats["stamina"] -= 10
        get_command(current_room, inventory, stats)
    elif "wand" in inventory and "sword" not in inventory:
        print(f"You slay the {current_room.monsters} with magic.")
        current_room.monsters = None
        stats["magic"] -= 10
        get_command(current_room, inventory, stats)
    else:
        print("Invalid command. Please try again.")
        get_command(current_room, inventory, stats)

def unlock(current_room, inventory, command, stats):
    if current_room == cell_11:
        if "jail keys" in inventory:
            print("You unlock the door and shove it open, despite its rusty, squealing hinges.")
            new_room = change_rooms("north", current_room)
            new_room.visited = True
            return new_room
    elif "10" in command:
        print("The cell door reluctantly unlocks and opens for you.")
        if current_room == cell_hall:
            new_room = change_rooms("east", current_room)
            new_room.visited = True
            return new_room
    else:
        print("The key fits in the lock but the lock refuses to turn.")
        get_command(current_room, inventory, stats)

def use_item(command, inventory):
    pass


#==================================================
# HELPER FUNCTIONS
#==================================================

def parse_input(command):
    if "quit" in command or command == ["q"]:
        exit()

    action = None

    if (("pick" in command and "up" in command)
            or "get" in command or "take" in command
            or "grab" in command):
        return "pick up"
    elif "go" in command or "walk" in command or "run" in command:
        return "change rooms"
    elif "search" in command or command == "search" or command == "s":
        return "secret"
    elif "map" in command or command == "map" or command == "m":
        return "map"
    elif "inventory" in command or command == "inventory" or command == "i":
        return "inventory"
    elif "stats" in command or command == "stats":
        return "stats"
    elif ("slay" in command or "kill" in command or "hit" in command or "stab" in command or "slash" in command or
          "attack" in command or "hit" in command):
        return "attack"
    elif "use" in command:
        return "use item"
    elif "dump" in command:
        return "dump"
    elif "yell" in command:
        return "yell"
    elif "unlock" in command:
        return "unlock"
    else:
        return "invalid command"

def get_command(current_room, inventory, stats):
    command = input().lower().split()
    action = parse_input(command)

    if action == "pick up":
         success = pick_up_item(command, current_room, inventory)
         if not success:
             print(f"You do not see that item in the {current_room.name}.")

    elif action == "change rooms":
        new_room = change_rooms(command, current_room)
        return new_room
    elif action == "secret":
        room_secret(current_room)
    elif action == "map":
        view_map(current_room, inventory)
    elif action == "inventory":
        view_inventory(current_room, inventory, stats)
    elif action == "stats":
        view_stats(current_room, inventory, stats)
    elif action == "attack":
        attack(current_room, inventory, stats, command)
    elif action == "use item":
        use_item(command, inventory)
    elif action == "unlock":
        new_room = unlock(current_room, inventory, command, stats)
        return new_room
    elif action == "dump":
        if current_room == cell_11 and "bucket of water" in inventory:
            print(textwrap.fill("You dump the bucket of water on the floor and it trickles down the hallway towards the guard. It "
                  "pools at his feet and he starts running down the hallway towards your cell. Just before he reaches "
                  "your cell, the guard slips and falls unconscious on the floor. His keys fall out of his hand and "
                  "land just outside the door to your cell.", width=120))
            current_room.monsters.remove("guard")
            current_room.description = current_room.alt_description
            print()
            return current_room

    elif action == "yell":
        if current_room == cell_11 and "guard" in current_room.monsters:
            print("You yell at the guard and he gives you a rude gesture.")
            return current_room
    elif action == "invalid command":
        print("Invalid command. Please try again.")
    else:
        print("Invalid command. Please try again.")


#==================================================
# DISPLAY FUNCTIONS
#==================================================

def welcome_message():
    """
    This function displays the title and the first prompt for the user. It requires no parameters and returns nothing.
    """
    clear_screen()
    print("Thank you for playing Dungeon Escape!")
    print()
    print()
    print("Enter 'Play' to start the game or 'Instructions' for game instructions")

def instructions_screen():
    """
    This function displays the instructions for the user. This screen is only accessible from the title screen. It
    requires no parameters and returns nothing.
    """

    clear_screen()
    print("Instructions: Read Them Carefully")
    print()
    print("Your goal is to find the key and escape the dungeon... or escape another way.")
    print("To navigate, enter the direction you want to go (ex: go north, walk south, etc).")
    print("To use the map, collect the ink and parchment. Then enter 'Map' at any time.")
    print("To check your inventory, enter 'Inventory' at any time.")
    print("To view your stats, enter 'Stats' at any time.")
    print("To exit the map, inventory, or stats screens, enter 'Exit'.")
    print("To pick up items, enter 'Pick up x' where x is the item in question. Change 'pick up' to 'use' if you want "
          "to use the item.")
    print("This dungeon is deadly. Slay your foes as fast as possible by entering 'Slay monster' or some acceptable "
          "variation.")
    print("To quit the game, enter 'Quit' at any time.")
    print()
    print()
    print("P.S. Please be creative. I am integrating lots of little commands and there are too many to list."
          "Play around with it and see what you can find!")

    input("Press Enter to return to the Title Screen...")
    title_screen()

def title_screen():
    """
    This function displays the title screen and prompts the user for a command. It will continue to display until the
    user enters any of the following commands: 'Play', 'Instructions', or 'Quit'. The commands are not case-sensitive.

    If the user enters 'Instructions', the instructions screen will be displayed.
    If the user enters 'Play' or 'Quit', the respective value will be returned.

    Returns:
         "play" - if user enters "play" or "p"
         "quit" - if user enters "quit" or "q"
    """

    clear_screen()
    welcome_message()
    first_command = input().lower()
    acceptable_commands = ["play", "p", "instructions", "i", "quit", "q"]

    if first_command not in acceptable_commands:
        print("Invalid command. Please try again.")
        title_screen()

    if first_command == "instructions" or first_command == 'i':
        instructions_screen()
    elif first_command == "play" or first_command == "p":
        return "play"
    elif first_command == "quit" or first_command == 'q':
        return "quit"
    
#==================================================
# FIXED ROOM CLASS OBJECTS
#==================================================
cell_11 = Room("Cell 11", "You are in a cell with a cot against the south wall and a cell door in "
                          "the north wall. There is a bucket in the corner with water dripping into it. Outside of the "
                          "cell door, is a guard standing watch at the end of the hall.")
cell_11.items = ["bucket of water", "jail keys"]
cell_11.monsters = ["guard"]
cell_11.visited = True
cell_11.alt_description = ("You are in a cell with a cot against the south wall and a cell door in the north wall. "
                           "There is a small stream of water running out the cell door, past the guard's unconscious "
                           "body.")

cell_10 = Room("Cell 10", "There is a skeleton with withered remains of clothing draping over its "
                          "bones laying on the cot in this cell. The cell door is on the west wall.")
cell_10.items = ["signet ring"]
cell_10.secrets = {0:"You search through the debris in the cell and notice a glinting object on the skeleton's finger. "
                     "It appears to be a Signet Ring."}

cell_hall = Room("Cell Hall", "There are 5 cells lining the walls on both the east and west sides of "
                              "the hall. They are numbered 1 - 11. You can see through the bars that there is a "
                              "skeleton in cell 10. The door is to the north.")

guard_chamber = Room("Guard Chamber", "You are in what appears to be a guard chamber. There are wooden "
                                      "lockers lining the east wall and doors on the north, south, and west walls.")
guard_chamber.items = ["parchment"]
guard_chamber.secrets = {0:"You search through the lockers and find parchment in the bottom of one."}

rope_exit = Room("Rope Exit", "This room is empty of any items. There are many cobwebs draping from the"
                              " walls and ceiling.")
rope_exit.secrets = {0: "Upon further inspection, you see a webbing network of cracks covering the western wall. It "
                        "seems like a strong enough force should be able to knock the wall down"}
rope_exit.alt_description = ("Bright sunlight streams into this room from the hole you blasted in the wall. You can see "
                             "the ground below you but it is too far to jump safely. You do see a thick tree branch "
                             "extending away from the building above you.")

#==================================================
# FIXED ROOM EXITS
#==================================================

cell_11.exits = {"north": cell_hall, "east": None, "south": None, "west": None}
cell_hall.exits = {"north": guard_chamber, "east": cell_10, "south": cell_11, "west": None}
cell_10.exits = {"north": None, "east": None, "south": None, "west": cell_hall}
guard_chamber.exits = {"north": large_room, "east": None, "south": cell_hall, "west": None}
rope_exit.exits = {"north": None, "east": guard_chamber, "south": None, "west": None}

#==================================================
# GAME LOOP
#==================================================

first_command = title_screen()

if first_command == "quit":
    exit()

else: #the game begins
    clear_screen()

    game_over = False
    stats = {"health": 30,
             "max_health": 30,
             "stamina": 30,
             "max_stamina": 30,
             "magic": 30,
             "max_magic": 30}
    current_room = cell_11
    inventory = []

    wrapped_desc = textwrap.fill(current_room.description, width=120)
    print(wrapped_desc)
    print("What do you do?")


    while True:
        #print(current_room.name)

        result = get_command(current_room, inventory, stats)

        if type(result) == Room:
            if result == current_room:
                continue
            else:
                current_room = result