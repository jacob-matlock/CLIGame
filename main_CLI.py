import os
import textwrap

class Room:
    def __init__(self, name, description, exits, items, secrets, monsters, visited):
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items
        self.secrets = secrets
        self.monsters = monsters
        self.visited = visited

def create_map(rooms_list):
    print("The map")

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
            print("stench coming from the water, so you let it dribble through your fingers and dry your hands on the cot.")
            return True
        if ("keys" in command or ("jail" in command and "keys" in command)) and "guard" in current_room.monsters:
            return False
        elif ("keys" in command or ("jail" in command and "keys" in command)) and "guard" not in current_room.monsters:
            print("You picked up the jail keys")
            inventory.append("jail keys")
            current_room.items.remove("jail keys")
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
            print("You picked up the sword")
            return
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

def view_map(current_room, inventory, rooms_list):
    if "parchment" in inventory and "ink" in inventory:
        create_map(rooms_list)
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

def parse_input(command):
    if command == "quit" or command == "q":
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

def get_command(current_room, inventory, stats, rooms_list):
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
        view_map(current_room, inventory, rooms_list)
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

#######################################################################################################################
"""This section of the code is creating the rooms and items in the game."""

cell_11 = Room("Cell 11", "You are in a cell with a cot against the south wall and a cell door in "
                          "the north wall. There is a bucket in the corner with water dripping into it. Outside of the "
                          "cell door, is a guard standing watch at the end of the hall.", {"north": "Cell Hall",
                          "east": None, "south": None, "west": None},["bucket of water", "jail keys"],
                   None, ["guard"], True)
cell_10 = Room("Cell 10", "There is a skeleton with withered remains of clothing draping over its "
                          "bones laying on the cot in this cell. The cell door is on the west wall.",{"north": None,
                          "east": None, "south": None,"west": "Cell Hall"}, ["signet ring"],{0:"You search "
                          "through the debris in the cell and notice a glinting object on the skeleton's finger. It "
                          "appears to be a Signet Ring."}, [], False)

cell_hall = Room("Cell Hall", "There are 5 cells lining the walls on both the east and west sides of "
                              "the hall. They are numbered 1 - 11. You can see through the bars that there is a "
                              "skeleton in cell 10. The door is to the north.", {"north": "Guard Chamber",
                              "east": "Cell 10", "south": "Cell 11", "west": None},[], None, [], False)

guard_chamber = Room("Guard Chamber", "You are in what appears to be a guard chamber. There are wooden "
                                      "lockers lining the east wall and doors on the north, south, and west walls.",
                                 {"north": "Large Room", "east": None, "south": "Cell Hall", "west": "Sleeping "
                                      "Quarters"},["parchment"],{0:"You search through the lockers and find "
                                      "parchment in the bottom of one."}, [], False)

sleeping_quarters = Room("Sleeping Quarters", "This room has with ten beds lining both the north and "
                                              "south walls with a chest at the foot of each. There is a door to the"
                                              " east.",{"north": None, "east": "Guard Chamber", "south": None,
                                              "west": None},["ink"], {0: "You search through each chest and "
                                              "find a bottle of ink in one."}, [], False)

large_room = Room("Large Room", "You are in a large, empty room with a door on each wall. There are "
                                "beautiful paintings lining the walls between the doors.", {"north":"Sword Room",
                                "east":"Statue Room", "south": "Guard Chamber", "west":"Empty Room"},None,
                         None, [], False)

sword_room = Room("Sword Room", "You are in a small room with dim lighting. In the center of the room "
                                "is a pedestal with a shiny, glinting sword placed in it. Engraved on the hilt of the "
                                "sword is a gryphon with a snake in its talons. There is a singular door in the south "
                                "wall.", {"north": None, "east": None, "south": "Large Room", "west": None},
                          ["sword"], {0: "There is a small round hole in the pedestal just in front of the "
                                         "blade of the sword."}, [], False)

statue_room = Room("Statue Room", "You are in a medium sized room with several rows of monster statues "
                         "of all different kinds. While counting, you see a cyclops, man-bat, pigman, goblin, ogre, "
                         "mimic, and minotaur to name a few. Your final count makes 25 total statues in the room. There "
                         "are doors on the east and west walls.", {"north": None, "east": "Kitchen", "south": None,
                         "west": "Large Room"}, None, None, None, False)

empty_room = Room("Empty Room", "You are in a small room with torches lining the walls but is otherwise "
                                "empty. There are doors on the east and west walls.", {"north": None, "east":
                                "Large Room", "south": None, "west": "Wand Room"}, None, None,
                       None, False)

wand_room = Room("Wand Room", "You are in a small room with a pedestal in the center. Carved on the "
                              "pedestal are strange, curving runes. Placed on top of the pedestal is a thin wooden rod "
                              "with similar runes engraved in it. Upon further inspection, you see a small diamond "
                              "embedded in the tip of the wand. There are doors in the north and east walls.",
                        {"north":"Minotaur Room", "east":"Empty Room", "south": None, "west": None}, ["wand"],
                      None, None, False)

minotaur_room = Room("Minotaur Room", "Upon entering this room, you are blasted with a wall of stench. "
                                "It is so overpowering that you almost leave the room but you notice a menacing Minotaur"
                                " with matted, midnight black fur across the room. It glares at you, snorting and "
                                "stamping its feet, seemingly preparing to charge.", {"north": "Art Room",
                                "east": None, "south": "Wand Room", "west":"Strange Room"}, ["Minotaur Horn"],
                         None, ["Minotaur"], False)

strange_room = Room("Strange Room", "You are in a cluttered room with lots of strange, unfamiliar "
                                "objects. Among them, a crystal orb, preserved monster parts, piles of bones and other "
                                "curiosities. There are a few cabinets dotting the walls with doors on the north and "
                                "east walls.", {"north": "Pit Room", "east": "Minotaur Room", "south": None,
                                "west": None}, ["potion"], {0:"You search through the cabinets in the room and find a small "
                                "glass bottle with a blue, shimmery liquid in it. The bottle is labeled “magic in a "
                                "bottle” with poor handwriting."}, None, False)

pit_room = Room("Pit Room", "You barely stop walking into this room in time to not fall into the gaping"
                            " pit that spans the majority of where the floor should be. There is a narrow ledge running "
                            "along the south and east walls, allowing passage between the two doors there.",
                      {"north": None, "east": "Art Room", "south": "Strange Room", "west": None}, None,
                    None, None, False)

art_room = Room("Art Room", "You are in awe of the beauty in this room. Scattered throughout the dimly "
                            "lit space are partially finished works of art. There is a painting of a beautiful sunset, "
                            "left without its landscape, a statue of a man fighting an invisible enemy, with his legs "
                            "forever entombed in stone, and many other pieces, abandoned by their creator. Aside from the "
                            "art, you see a door on each wall.", {"north": "Golden Key Room", "east": "Garden",
                            "south": "Minotaur Room", "west": "Pit Room"}, None, None, None, False)

gk_room = Room("Golden Key Room", "Suspended by a rope in the middle of this room is a golden key with "
                                  "wings on its bow. There are doors on the north and south walls.", {"north":
                                  "Torture Chamber", "east": None, "south": "Art Room", "west": None}, ["Golden Key"],
                           None, None, False)

torture_chamber = Room("Torture Chamber", "This room is full of medieval torture devices. Looking at "
                                          "them sends shivers down your spine. There are doors to the west, south, and "
                                          "east.", {"north": None, "east": "Workshop", "south": "Golden Key Room",
                                          "west": "Man-Bat Room"}, None, None, None, False)

manbat_room = Room("Man-Bat Room", "At first glance, this room seemed empty, but as you look around, you"
                                   " hear a slight squeaking coming from above you. You look up and see a man-bat hybrid"
                                   " hanging from the ceiling. It appears to be smelling the air between you.",
                             {"north": None, "east": "Torture Chamber", "south": None, "west": None},
                            ["man-bat wing"], None, ["Man-Bat"], False)

workshop = Room("Workshop", "This room is filled with machines belonging to masters of many different "
                            "trades. There is a smithy, a tanning rack, carpenters tools, and plenty more. There is no "
                            "work in progress at any of the workstations so it appears to serve more as a storage room "
                            "right now. There are doors on the west, north, and east walls.", {"north": "Rope Exit",
                            "east": "Dining Room", "south": None, "west": "Torture Chamber"}, None, None,
                   None, False)

rope_exit = Room("Rope Exit", "This room is empty of any items. There are many cobwebs draping from the "
                              "walls and ceiling. There is a door on the south wall.", {"north": None, "east": None,
                              "south": "Workshop", "west": None}, None, {0: "Upon further inspection, you see a webbing "
                              "network of cracks covering the northern wall. It seems like a strong enough force should "
                              "be able to knock the wall down"}, None, False)

dining_room = Room("Dining Room", "You are in a long dining room with a table spanning almost the length"
                                  " of the whole room. There are chairs at each head and at even intervals down each "
                                  "side. While the places at the table are set, ready for a meal, there is no food in "
                                  "the room, save for some fresh fruit in bowls lining the center of the table. There "
                                  "is a single door in the west wall.", {"north": None, "east": None, "south":
                                  None, "west": "Workshop"}, ["fruit"], {0: "You run your fingers along the"
                                  " trim that lines the walls and you feel something catch. When you go back to see what"
                                  " it was, you find that there is a small button embedded in the wood of the trim."},
                         None, False)

garden = Room("Garden", "Light streams into this room from skylights in the ceiling. The sunlight bathes"
                        " and feeds rows upon rows of plants. You see fruits and vegetables of all kinds, ripe for the "
                        "picking. There are doors in the east and west walls.", {"north": None, "east": "Ogre Room",
                        "south": None, "west": "Art Room"}, ["fruit", "vegetables"], None, None, False)

ogre_room = Room("Ogre Room", "You step into this room and are greeted by a thunderous roar. Across the "
                              "room you see a massive ogre heft a giant club onto his shoulder. Drool drips onto the "
                              "floor from his underbitten jaw as he takes a step towards you, menacingly.", {"north": })

rooms_list = [cell_11, cell_10, cell_hall, guard_chamber, sleeping_quarters, large_room, sword_room, statue_room,
             empty_room]
#######################################################################################################################
"""This section connects all of the rooms together."""
cell_11.exits["north"] = cell_hall

cell_hall.exits["north"] = guard_chamber
cell_hall.exits["east"] = cell_10
cell_hall.exits["south"] = cell_11

cell_10.exits["west"] = cell_hall

guard_chamber.exits["north"] = large_room
guard_chamber.exits["south"] = cell_hall
guard_chamber.exits["west"] = sleeping_quarters

sleeping_quarters.exits["east"] = guard_chamber

large_room.exits["south"] = guard_chamber
large_room.exits["north"] = sword_room

sword_room.exits["south"] = large_room
#######################################################################################################################

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

        result = get_command(current_room, inventory, stats, rooms_list)

        if type(result) == Room:
            if result == current_room:
                continue
            else:
                current_room = result
