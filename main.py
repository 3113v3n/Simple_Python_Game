import random
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item


#Create Black Magic
fire = Spell("Fire",25,600,"black")
thunder = Spell("Thunder",25,600,"black")
blizzard = Spell("Blizzard",25,600,"black")
lightning = Spell("Lightning",40,1200,"black")
quake = Spell("Quake",14,140,"black")

#Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 40, 1500, "white")


#Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hiportion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("ELixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

greenade = Item("Greenade", "atack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, lightning, cure, cura]
player_items = [{"item":potion, "quantity":15},
                {"item":hiportion, "quantity":5},
                {"item":superpotion, "quantity":5},
                {"item":elixer, "quantity":5},
                {"item":hielixer, "quantity":2},
                {"item":greenade, "quantity":5}]

#Instantiate Characters
player1 = Person("Valos:", 3060, 132,300,34,player_magic,player_items)
player2 = Person("Nicky:", 2070, 188,350,34,player_magic,player_items)
player3 = Person("Robot:", 4060, 200,260,34,player_magic,player_items)

enemy1 = Person("Krono:",10200,705,525,25,[],[])
enemy2 = Person("Cersei", 1250,130,560,325,[],[])
enemy3 = Person("Ramsey",1250,130,560,325,[],[])

enemies = [enemy1, enemy2, enemy3]
players = [player1, player2, player3]
running = True
i =0

print(bcolors.FAIL + bcolors.BOLD + "ENEMY ATTACK !!!" + bcolors.ENDC)

while running:
    print("==================================================")

    print("\n\n")
    #print player statistics
    print("NAME                      HP                                   MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) -1 #this is because counting starts at 0

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print ("You attacked for"+ enemies[enemy].name.replace(" ","") +" for", dmg, "points of damage." )
            #delete enemy from list
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ",""), "Has been died")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL  + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)
            #healing spell
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name +" heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name +" deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ","") + bcolors.ENDC)

                #delete enemy from list
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ",""), "Has been died")
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose Item: ")) - 1
            #Allow us to go back
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n " + "None left ..." + bcolors.ENDC)
                continue
            #reduce quantity after use
            player.items[item_choice]["quantity"]  -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:#each player gets max points
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                print(bcolors.OKGREEN + "\n" + item.name + "Fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop), "points of damage to " +enemies[enemy].name + bcolors.ENDC)
                #delete enemy from list
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ",""), "Has been killed")
                    del enemies[enemy]

    enemy_choice = 1
    #create enemy Target
    target = random.randrange(0,3)

    enemy_dmg = enemies[0].generate_damage()
    players[target].take_damage(enemy_dmg) #player to be attacked
    print("Enemy attacks for", enemy_dmg)


    #Determining the winner
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + bcolors.BOLD + "YOU WIN !!!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + bcolors.BOLD + "ENEMY HAS DEFEATED YOU !!!" + bcolors.ENDC)
        running = False
    #running = False
