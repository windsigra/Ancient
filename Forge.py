# import mysql.connector
import colorama
import math
from colorama import Fore
colorama.init(autoreset=False)
import random
from datetime import datetime
# from char_load import Load_Master
# from char_save import *
# shield for parry weapons and range weapons,  top end(mace, morning star, club, ect) weapons shields is way less
# effective
# reach gives +1 to hit per 3 ft of reach over defenders reach


class Forge(object):
    # db = mysql.connector.connect(host='localhost', user='root', passwd='t5T%r4R$e3E#w2W@q1Q!', database='realmserver')

    weapon_list = {'Name': ['Greatsword', 'Longsword', 'Broadsword',
                            'Shortsword', 'Claymore', 'Battle Axe', 'Axe',
                            'Scimitar', 'Halberd', 'Falchion', 'Dagger', 'Pike',
                            'Spear', 'Whip', 'Shortbow', 'Longbow',
                            'Morningstar', 'Mace', 'Flail', 'Warhammer',
                            'Hammer', 'Staff', 'Greatclub', 'Sling', 'Shield'],
                   'item_mass': [6, 5, 4, 3, 6, 4, 2, 4, 7, 4, 2, 7, 6, 2, 4, 5, 3, 2, 2, 3, 2, 6, 2, 1, 4],
                   'size': ['N', 'N', 'B', 'B', 'N', 'B', 'S', 'B', 'N', 'B', 'S', 'N', 'N', 'M', 'B', 'N', 'B', 'M',
                            'M', 'N', 'S', 'N', 'N', 'S', 'N'], # B = Backpack, N = No storage, S = small bag, M = medium bag
                   'Dice_Type': [12, 8, 7, 6, 8, 8, 6, 6, 10, 8, 4, 6, 4, 4, 6, 8, 8, 8, 6, 8, 6, 6, 8, 6, 0],
                   'Damage_Modifier': [2, 0, 1, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 1, 0, 0],
                   'RDamage_Modifier': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'Damage_Type': ['Slash', 'Slash', 'Slash', 'Slash', 'Slash', 'Slash', 'Slash', 'Slash', 'Slash', 'Slash',
                                   'Pierce', 'Pierce', 'Pierce', 'Pierce', 'Pierce', 'Pierce', 'Crush',
                                   'Bash', 'Bash', 'Bash', 'Bash', 'Bash', 'Bash', 'Bash', 'Bash'],
                   'To_Hit_Modifier': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'RTo_Hit_Modifier': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'Range_Distance': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 180, 0, 0, 0, 0, 0, 0, 0, 60, 0],
                   'Thrown_Distance': [0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 40, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'parry': [3, 5, 3, 4, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'block': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                   'block_resist': [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1], # 0 False,  # 1 True
                   'weapon_reach': [6, 4, 3, 3, 5, 5, 2, 4, 7, 4, 2, 7, 5, 5, 0, 0, 4, 3, 4, 5, 2, 6, 4, 0, 1],
                   'weapon_speed': [5, 3, 4, 2, 4, 6, 3, 3, 5, 3, 1, 4, 3, 4, 4, 5, 5, 3, 4, 6, 4, 4, 5, 7, 1],
                   'Hands_Needed': [2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1],
                   'Weapon_Type': ['M', 'M', 'M', 'M', 'M', 'M', 'B', 'M', 'M', 'M',
                                   'B', 'M', 'B', 'M', 'R', 'R', 'M', 'M', 'M', 'M',
                                   'B', 'M', 'M', 'R', 'S'],   # M = Melee, R = Range, B = Thrown or Melee, S = Shield
                   'Base_Cost': [350,200, 130, 90, 200, 200, 50, 75, 175, 75, 30, 80, 35, 35, 175, 225, 110, 50, 65, 100,
                                 50, 25, 25, 25, 50],
                   'Base_Durability': [1000, 700, 800, 600, 850, 1250, 300, 500, 400, 500, 550, 400, 200, 350, 600, 600, 900, 1000,
                                      600, 700, 400, 500, 300, 350, 500],
                   'Material_base': ['ore','ore', 'ore', 'ore', 'ore', 'ore','ore', 'ore', 'ore', 'ore', 'ore', 'ore', 'wood', 'leather', 'wood',
                                     'wood', 'ore', 'ore', 'ore', 'wood', 'ore','wood', 'wood', 'leather', 'wood'],
                   'Material_Quantity': [5, 3, 3, 2, 4, 4, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 4, 2, 2, 3, 1, 2, 2, 1, 2],
                   'Create_base_chance': [30, 45, 50, 55, 35, 40, 60, 50, 60, 50, 50, 65, 55, 60, 65, 80, 70, 80, 80, 70, 45, 45, 35, 45, 55],
                   'Made_Of': '',
                   'craftsmanship': '',
                   'Crafted by': '',
                   'Condition': '',
                   'Rank': '',
                   'Enscription': '',
                   'Forged_Date': '',
                   'weapon_origin': 0
                   }

    armor_list = {'Name':
                      ['Full Platemail', 'Platemail', 'Banded mail', 'Chainmail', 'Scalemail', 'Ringmail',
                       'Studded Armor',
                       'Armor', 'Padded Armor', 'Attire', 'Scale Armor'],
                  'item_mass': [25, 20, 15, 8, 15, 12, 12, 10, 8, 4, 20],
                  'size': ['N', 'N', 'M', 'B', 'N', 'B', 'B', 'B', 'M', 'M', 'S', 'N'],  # B = Backpack, N = No storage, S = small bag, M = medium bag
                  'Armor_Class': [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 10],
                  'Base_Durability': [2500, 2000, 1500, 1250, 1000, 850, 650, 500, 300, 100, 2500],
                  'Base_Cost': [1000, 600, 350, 250, 175, 125, 100, 75, 50, 5, 5000],
                  'Material_base': ['ore', 'ore', 'ore', 'ore', 'ore', 'ore', 'leather', 'leather', 'linen', 'linen',
                                    'scales'],
                  'Material_Quantity': [20, 15, 10, 8, 6, 3, 5, 5, 3, 2, 20],
                  'Create_base_chance': [30, 45, 50, 55, 60, 65, 50, 55, 70, 75, 1],
                  'Made_Of': '',
                  'craftsmanship': '',
                  'Crafted by': '',
                  'Condition': '',
                  'Rank': '',
                  'Enscription': '',
                  'Forged_Date': '',
                  'armor_origin': 0
                  }

    material_list = {'Name': ['Bronze', 'Iron', 'Lean', 'Mithril',
                              'Adamanite', 'Crystal Lean', 'Leather',
                              'Wilkwork', 'Drow~Kyn', 'Dragon Hide', 'Cloth',
                              'Leather Laced', 'Elven Weave', 'Everflow', 'Oaken',
                              'Dry-knot', 'Silkwood', 'El-spring', 'Reen', 'Dragon'],

                     'Stat_Mod': [-2, 0, 1, 2, 3, 5, 0,
                                  1, 2, 3, 0,
                                  1, 2, 3, 0,
                                  1, 2, 3, 4, 5],
                     'Durability': [0, 500, 2000, 5000, 10000, 20000, 0,
                                        200, 500, 1200, 0,
                                        100, 300, 600, 0,
                                        200, 400, 750, 3000, 15000],
                     'Cost_per_unit': [5, 15, 500, 1000, 2500, 10000, 3,
                                       250, 1000, 3000, 1,
                                       200, 700, 2500, 1,
                                       200, 1000, 3000, 8000, 17500],
                     'Material_base': ['ore', 'ore', 'ore', 'ore', 'ore', 'ore',
                                       'leather', 'leather', 'leather', 'leather',
                                       'linen', 'linen', 'linen', 'linen', 'wood',
                                       'wood', 'wood', 'wood', 'wood', 'scales'],
                     'Create_mod': [0, -10, -25, -50, -80, -200,
                                    0, -20, -50, -100,
                                    0, -10, -50, -100,
                                    0, -15, -50, -90, -150, -125],
                     'Rank': [-1, 0, 1, 2, 3, 5,
                              0, 1, 2, 3,
                              0, 1, 2, 3,
                              0, 1, 2, 3, 4, 4],
                     'Enchant_base': [0, 0, 2, 3, 5, 8, 0, 2, 3, 5,
                                     0, 0, 2, 4, 0, 2, 3, 4, 5, 6],
                     'material_origin': 0
                     }

    craftmanship_list = {'Name': ['Horrible', 'Flawed', 'Standard', 'Fine',
                                  'Exceptional', 'Exquisite', 'Flawless'],
                         'stat_mod': [-2, -1, 0, 0, 1, 2, 3],
                         'Durability': [.4, .6, 0, 1.5, 2, 2.5, 3],
                         'Cost_mod': [.4, .6, 1, 1.2, 2, 7, 15],
                         'Rank': [-2, -1, 0, 1, 2, 3, 4],
                         'Enchant_mod': [0, 0, 0, 0, 0, 1, 2],
                         'craftmanship_origin': 0
                         }

    condition_list = {'Name': ['Battered', 'Poor', 'Worn', 'Good', 'Pristine'],
                      'stat_mod': [.2, .6, .9, 1, 1],
                      'Durability': [.15, .3, .6, .95, 1],
                      'Cost_mod': [.6, .7, .8, .95, 1],
                      'condition_origin': 0
                      }

    enchant_list = {'Name': ['0', '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10'],
                  'Stats': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  'durability': [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                  'Cost_mod': [0, 10000, 25000, 50000, 100000, 200000, 400000, 800000, 1500000, 2500000, 5000000]
                  }

    enchant_element_list = {'Name': ['Fire', 'Frost', 'Lightning', 'Poison', 'Acid'],
                          'stat_mod': [8, 8, 8, 8, 8],
                          'Cost_mod': [1000, 2500, 5000, 10000, 20000]
    }

    wpack = {'name': [],
             'name_type': [],  # longsword, dagger, longbow ect...
             'made_of': [],
             'cost': [],
             'weapon_type': [],   # if melee, range or thrown
             'damage_type': [],
             'dice_type': [],
             'damage_modifier': [],
             'to_hit_modifier': [],
             'range_distance': [],
             'parry': [],
             'block': [],
             'block_resist': [],
             'weapon_reach': [],
             'weapon_speed': [],
             'hands_needed': [],
             'magic_modifier': [],
             'magic_limit': [],
             'craftsmanship': [],
             'condition_': [],
             'durability': [],
             'crafted_by': [],
             'enchanted_by': [],
             'creation_date': [],
             'origin': []
             }
    apack = {'name': [],
             'name_type': [],  # armor set, platemail, full platemail, leather studded, leather, chain ect.
             'cost': [],
             'armor_class': [],
             'magic_modifier': [],
             'magic_limit': [],
             'craftsmanship': [],
             'condition_': [],
             'durability': [],
             'crafted_by': [],
             'enchanter_by': [],
             'creation_date': [],
             'origin': []
             }

    # cur = db.cursor(dictionary=True)
    # armor_sql = ("SELECT * from Lore_Armors WHERE armor_origin = %s")
    # armor_name = (armor_list['armor_origin'],)
    # cur.execute(armor_sql, armor_name)
    # armor_origin = cur.fetchone()
    #
    # cur = db.cursor(dictionary=True)
    # weapon_sql = ("SELECT * from Lore_Weapons WHERE weapon_origin = %s")
    # weapon_name = (weapon_list['weapon_origin'],)
    # cur.execute(weapon_sql, weapon_name)
    # weapon_origin = cur.fetchone()

    today = datetime.today()
    creation = today.strftime("%b %d %Y - %I:%M %p")
    armor_origin = 0
    weapon_origin = 0

    def __init__(self, order_name):
        self.number_of_weapons = None
        self.material_type = ''
        self.order_name = order_name
        # self.num = num

        print(Fore.LIGHTMAGENTA_EX + 'FORGE:',Fore.LIGHTGREEN_EX + '',self.order_name,Fore.LIGHTCYAN_EX + 'Online')
        print(self.creation)



    def data(self):
        for loop in range(0, 7):
            print()
            print(Fore.LIGHTMAGENTA_EX + '_' * 150)
            print()
            match loop:
                case 0:
                    print(Fore.LIGHTYELLOW_EX + '____{ Weapons Data }____')
                    self.main_list = self.weapon_list
                case 1:
                    print(Fore.LIGHTYELLOW_EX + '____{ Armors Data }____')
                    self.main_list = self.armor_list
                case 2:
                    print(Fore.LIGHTYELLOW_EX + '____{ Material Data }____')
                    self.main_list = self.material_list
                case 3:
                    print(Fore.LIGHTYELLOW_EX + '____{ Craftsmanship Data }____')
                    self.main_list = self.craftmanship_list
                case 4:
                    print(Fore.LIGHTYELLOW_EX + '____{ Condition Data }____')
                    self.main_list = self.condition_list
                case 5:
                    print(Fore.LIGHTYELLOW_EX + '____{ Enchant Data }____')
                    self.main_list = self.enchant_list
                case 6:
                    print(Fore.LIGHTYELLOW_EX + '____{ Enchant Element Data }____')
                    self.main_list = self.enchant_element_list


            count = 0
            #item_list = []
            outer = 0
            self.list_length = 0
            for key, value in self.main_list.items():
                print(Fore.LIGHTYELLOW_EX + f'{key}:', end='')

                if key != 'Made_Of':
                    for item in value:
                        val = str(item)
                        print(Fore.LIGHTWHITE_EX + f'[{count}]',Fore.LIGHTCYAN_EX + f'{val}  ', end='')
                        if count <= 25:
                            count += 1
                else:
                    break

                    count = 0
                print()
        print()
        print(Fore.LIGHTMAGENTA_EX + '_' * 150)
        print()

    # _-Armor Functions_----------------------------------------------------------

    def pick_armor_set(self):
        self.id_number = 0
        self.armor_type = random.choices(self.armor_list['Name'], weights=[270, 270, 260,260, 200, 200, 200, 250, 240, 230, 5], k=1)

        for item in self.armor_type:
            self.armor_set = item     #convert from example: ['Chainmail'] to Chainmail

        for item in self.armor_list['Name']:
            if item == self.armor_set:
                break
            self.id_number += 1

    def pick_material(self):
        self.material_id = 0
        if self.armor_list['Material_base'][self.id_number] == 'ore':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[10, 150, 50, 45, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], k=1)
        elif self.armor_list['Material_base'][self.id_number] == 'leather':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 50, 40, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], k=1)
        elif self.armor_list['Material_base'][self.id_number] == 'linen':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 20, 3, 1, 0, 0, 0, 0, 0, 0], k=1)
        elif self.armor_list['Material_base'][self.id_number] == 'wood':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 10, 5, 2, 1, 0], k=1)
        elif self.armor_list['Material_base'][self.id_number] == 'scales':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], k=1)
        for item in self.material_type:
            self.material_type = item
        for item in self.material_list['Name']:
            if item == str(self.material_type):
                self.material_type = item
                break
            self.material_id += 1

    def create_armor(self):
        self.crafted_id = 0
        self.armor_smith = 90
        self.armor_worked = 0
        self.crafting_modifier = 0
        self.armor_worked = self.armor_list['Create_base_chance'][self.id_number]
        self.armor_worked += self.material_list['Create_mod'][self.material_id]
        self.armor_worked += self.armor_smith
        for creating in range (1, 7):
            self.processing = random.randint(1, 100 - self.armor_smith)
            if self.processing <= self.armor_worked:
                    self.outcome = 'Success!'
                    self.crafting_modifier += 1
            else:
                self.outcome ='Failure~'

        match self.crafting_modifier:
            case 0:
                a = 25; b = 50; c = 100; d = 5; e = 1; f = 1; g = 1
            case 1:
                a = 5; b = 55; c = 100; d = 10; e = 5; f = 1; g = 1
            case 2:
                a = 5; b = 5; c = 200; d = 10; e = 10; f = 5; g = 1
            case 3:
                a = 1; b = 3; c = 100; d = 25; e = 10; f = 5; g = 1
            case 4:
                a = 1; b = 5; c = 100; d = 5; e = 1; f = 1; g = 1
            case 5:
                a = 1; b = 5; c = 150; d = 50; e = 10; f = 1; g = 1
            case 6:
                a = 1; b = 2; c = 100; d = 75; e = 50; f = 15; g = 5

        self.armor_craftmanship = random.choices(self.craftmanship_list['Name'], weights=[a, b, c, d, e, f, g], k=1)
        item = ''.join(self.armor_craftmanship)
        for name in self.craftmanship_list['Name']:
            if item == name:
                break
            self.crafted_id += 1
        for item in self.armor_craftmanship:
            self.armor_crafted = item



    def Armor_Condition(self):
        self.condition_id = 0
        self.armor_condition = random.choices(self.condition_list['Name'], weights=[1, 3, 10, 50, 5], k=1)
        self.item = ''.join(self.armor_condition)
        for name in self.condition_list['Name']:
            if self.item == name:
                break
            self.condition_id += 1
        for item in self.armor_condition:
            self.armor_condition = item

    def Armor_Cost(self):
        self.armor_cost = 0
        self.material_cost = 0
        self.crafted_cost = 0
        self.armor_cost = self.armor_list['Base_Cost'][self.id_number]
        self.material_cost = self.material_list['Cost_per_unit'][self.material_id] * self.armor_list['Material_Quantity'][self.id_number]
        self.armor_cost += self.material_cost
        self.crafted_cost = self.armor_cost * self.craftmanship_list['Cost_mod'][self.crafted_id]
        self.armor_cost = self.crafted_cost
        int(self.armor_cost)
        #print('Crafted Cost: ', self.armor_cost)
        self.condition = self.armor_cost * self.condition_list['Cost_mod'][self.condition_id]
        self.armor_cost = int(self.condition)
        #print('Final Cost: ', self.armor_cost)

    def Armor_Stats(self):
        self.armor_class = 0
        self.durability = 0
        self.armor_class = self.armor_list['Armor_Class'][self.id_number] + self.material_list['Stat_Mod'][self.material_id]
        if self.material_list['Name'][self.material_id] != 'Cloth':
            self.armor_class += int(self.craftmanship_list['stat_mod'][self.crafted_id])
        self.armor_class *= round(self.condition_list['stat_mod'][self.condition_id])
        if self.armor_class < 0:
            self.armor_class = 0
        self.durability = int(self.armor_list['Base_Durability'][self.id_number] + self.material_list['Durability'][
            self.material_id])
        if self.craftmanship_list['Durability'][self.crafted_id] != 0:
            self.durability *= self.craftmanship_list['Durability'][self.crafted_id]
        if self.condition_list['Durability'][self.condition_id] != 0:
            self.durability *= self.condition_list['Durability'][self.condition_id]
        self.durability = int(self.durability)

    #_-Armor Functions End_________________________________________

    def Armor_Magic(self):
        self.enchant_id = 0
        self.magic = ''
        self.magic_limit = 0
        self.magic_bonus = random.choices(self.enchant_list['Name'], weights=[12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
        self.magic = ''.join(self.magic_bonus)
        for item in self.enchant_list['Name']:
            if self.magic == item:
                break
            self.enchant_id += 1
        if self.magic == '0':
            self.magic = ''
        self.magic_limit = self.material_list['Enchant_base'][self.material_id] + self.craftmanship_list['Enchant_mod'][self.crafted_id]
        if self.enchant_list['Stats'][self.enchant_id] > self.magic_limit:
            self.enchant_bonus = self.enchant_list['Stats'][self.magic_limit]
            self.armor_class += self.enchant_bonus

            self.armor_cost += self.enchant_list['Cost_mod'][self.magic_limit]

            self.durability += self.enchant_list['durability'][self.magic_limit]
            self.magic = self.enchant_list['Name'][self.magic_limit]
            if self.magic == '0':
                self.magic = ''
        else:
            self.enchant_bonus = self.enchant_list['Stats'][self.enchant_id]
            self.armor_class += self.enchant_bonus
            self.armor_cost += self.enchant_list['Cost_mod'][self.enchant_id]
            self.durability += self.enchant_list['durability'][self.enchant_id]

    ###############################################
    ### -____ARMOR ORDER______-###
    ###############################################

    def armor_order(self, num, filter, condition_name, craftsmanship_name, material_name, armor_name, enchant):
        armor_set = ''
        self.material_name = material_name  # set Original Material
        clear_apack = {'name': [],
                         'name_type': [],
                         'cost': [],
                         'armor_class': [],
                         'magic_modifier': [],
                         'magic_limit': [],
                         'craftsmanship': [],
                         'condition_': [],
                         'durability': [],
                         'crafted_by': [],
                         'enchanted_by': [],
                         'creation_date': [],
                         'origin': []
                         }
        self.apack.clear()
        self.apack = dict(clear_apack)
        self.number_of_armors = num

        for count in range(1, self.number_of_armors + 1):
            self.material_name = material_name # if Steel or Damascus return to original material of iron.
            self.pick_armor_set()
            self.pick_material()
            self.create_armor()
            self.Armor_Condition()
            self.Armor_Cost()
            self.Armor_Stats()
            self.Armor_Magic()
            COLORNAME = 'LIGHTCYAN_EX'
            color = getattr(Fore, COLORNAME)
            if self.craftmanship_list['Name'][self.crafted_id] == 'Horrible' or self.craftmanship_list['Name'][self.crafted_id] == 'Flawed':
                COLORNAME = 'LIGHTRED_EX'
                color = getattr(Fore, COLORNAME)
            else:
                COLORNAME = 'LIGHTCYAN_EX'
                color = getattr(Fore, COLORNAME)
            if self.material_type == 'Adamanite':
                COLORNAME2 = 'LIGHTBLUE_EX'
                color2 = getattr(Fore, COLORNAME2)
            else:
                COLORNAME2 = 'LIGHTWHITE_EX'
                color2 = getattr(Fore, COLORNAME2)

            if self.material_list['Name'][self.material_id] == 'Dragon':
                COLORNAME2 = 'LIGHTRED_EX'
                color2 = getattr(Fore, COLORNAME2)

            if self.material_list['Name'][self.material_id] == 'Crystal Lean':
                COLORNAME2 = 'LIGHTYELLOW_EX'
                color2 = getattr(Fore, COLORNAME2)

            if self.material_list['Name'][self.material_id] == 'Lean':
                COLORNAME2 = 'LIGHTCYAN_EX'
                color2 = getattr(Fore, COLORNAME2)

            if self.material_list['Name'][self.material_id] == 'Mithril':
                COLORNAME2 = 'LIGHTGREEN_EX'
                color2 = getattr(Fore, COLORNAME2)

            if self.armor_class <= 0:
                COLORNAME1 = 'LIGHTRED_EX'
                color1 = getattr(Fore, COLORNAME1)
            else:
                COLORNAME1 = 'LIGHTWHITE_EX'
                color1 = getattr(Fore, COLORNAME1)

            self.original_armor_set = self.armor_set

            if self.material_type == 'Mithril' and self.armor_set == 'Chainmail' and self.armor_crafted == 'Exquisite':
                self.armor_set = 'Elven Chain'
                COLORNAME2 = 'LIGHTYELLOW_EX'
                color2 = getattr(Fore, COLORNAME2)
            if self.material_type == 'Mithril' and self.armor_set == 'Chainmail' and self.armor_crafted == 'Flawless':
                self.armor_set = 'Royal Elven Chain'
                COLORNAME2 = 'LIGHTMAGENTA_EX'
                color2 = getattr(Fore, COLORNAME2)

            self.original_material_type = self.material_type

            if (self.material_type == 'Iron') and (self.armor_crafted == 'Fine' or self.armor_crafted == 'Exceptional'):
                self.material_type = 'Steel'
                COLORNAME2 = 'LIGHTYELLOW_EX'
                color2 = getattr(Fore, COLORNAME2)
            if (self.material_type == 'Iron') and (self.armor_crafted == 'Flawless' or self.armor_crafted == 'Exquisite'):
                self.material_type = 'Damascus'
                COLORNAME2 = 'LIGHTMAGENTA_EX'
                color2 = getattr(Fore, COLORNAME2)
            if self.material_type == 'Adamanite' and self.armor_crafted == 'Flawless' and (self.armor_set == 'Full Platmail' or
                    self.armor_set == 'Platemail'):
                self.material_type = 'Dwarven'
                COLORNAME2 = 'LIGHTBLUE_EX'
                color2 = getattr(Fore, COLORNAME2)

            if filter == 0:
                print(color1 + f'{count}', Fore.LIGHTMAGENTA_EX + f'{self.order_name} Armor Set[{self.id_number}]',
                      Fore.LIGHTYELLOW_EX + f'Cost: {self.armor_cost} ',
                      color + f': {self.armor_condition}, {self.armor_crafted},',
                      color2 + f' {self.magic} {self.material_type} {self.armor_set}',
                      color1 + f'Ac:{self.armor_class}',
                      Fore.BLUE + f' Durability: {self.durability}')

            elif ((self.armor_crafted == craftsmanship_name or craftsmanship_name == 'All') and (self.armor_condition == condition_name
                    or condition_name == 'All') and (self.original_material_type == material_name or material_name == 'All')
                    and (self.original_armor_set == armor_name or armor_name == 'All' )):
                if self.enchant_bonus >= enchant:
                    print(color1 + f'{count}',Fore.LIGHTMAGENTA_EX + f'{self.order_name} Armor Set[{self.id_number}]',
                        Fore.LIGHTYELLOW_EX + f'Cost: {self.armor_cost} ',
                        color + f': {self.armor_condition}, {self.armor_crafted},',
                        color2 + f' {self.magic} {self.material_type} {self.armor_set}',
                        color1 + f'Ac:{self.armor_class}',
                        Fore.BLUE + f' Durability: {self.durability}')

            # print("------------")
            # print(self.enchant_bonus)
            # print(enchant)
            # print(type(self.enchant_bonus))
            # print(condition_name)
            # print(self.armor_condition)
            # print(craftsmanship_name)
            # print(self.armor_crafted)
            # print(self.material_name)
            # print(self.material_type)
            # print(armor_name)
            # print(self.armor_set)
            # print("------------")


            self.Armor_packing()
        self.Armor_shipment()

    def Armor_packing(self):
        self.armor_origin += 1
        #self.apack = []
        self.name = self.material_type + ' ' + self.armor_set
        if self.magic_bonus != '':
            self.name = self.magic + ' ' + self.material_type + ' ' + self.armor_set
### SPECIAL NAMING OF ARMORS
        if self.material_type == 'Mithril' and self.armor_set == 'Chainmail' and  self.armor_crafted == 'Exquisite':
            self.armor_set = 'Elven Chain'

        if self.material_type == 'Mithril' and self.armor_set == 'Chainmail' and  self.armor_crafted == 'Flawless':
            self.armor_set = 'High Elven Chain'

        if self.material_type == 'Iron' and  self.armor_crafted == 'Fine':
            self.material_type = 'Steel'

        if self.material_type == 'Iron' and  self.armor_crafted == 'Exceptional':
            self.material_type = 'Steel'

        if self.material_type == 'Iron' and  self.armor_crafted == 'Exquisite':
            self.Material_type = 'Damascus'

        if self.material_type == 'Iron' and  self.armor_crafted == 'Flawless':
            self.material_type = 'Damascus'

        if self.material_type == 'Adamanite' and  self.armor_crafted == 'Flawless':
            self.material_type = 'Dwarven'

        self.crafted_by = self.order_name + ' Forge'
        self.apack['name'].append(self.name)
        self.apack['name_type'].append(self.armor_set)
        self.apack['cost'].append(self.armor_cost)
        self.apack['armor_class'].append(self.armor_class)
        self.apack['magic_modifier'].append(int(self.enchant_id))
        self.apack['magic_limit'].append(self.magic_limit)
        self.apack['craftsmanship'].append(self.armor_crafted)
        self.apack['condition_'].append(self.armor_condition)
        self.apack['durability'].append(self.durability)
        self.apack['crafted_by'].append(self.crafted_by)
        self.apack['enchanted_by'].append(self.crafted_by)
        self.apack['creation_date'].append(self.creation)
        self.apack['origin'].append(self.armor_origin)
        # print(self.apack)



    def Armor_shipment(self):
        self.count = 0
        # print()
        # print(Fore.LIGHTWHITE_EX + f'{self.order_name} Armor shipping Label')
        # for key, value in self.apack.items():
        #     print()
        #     print(Fore.LIGHTYELLOW_EX + f'{key}:', Fore.LIGHTCYAN_EX + f'{value[1]} ', end='')

        # print(Fore.LIGHTMAGENTA_EX + '_' * 150)
        # print()
        for key, value in self.apack.items():
            key = key
            # print()
            # print(Fore.LIGHTYELLOW_EX + f'{key}: ', end='')
            for item in value:
                val = str(item)
                # print(Fore.LIGHTWHITE_EX + f'[{self.count}]', Fore.LIGHTCYAN_EX + f'{val}, ', end='')
                self.count += 1
            self.count = 0
            # print()
        # print()
        # print(Fore.LIGHTMAGENTA_EX + '_' * 150)
        # print()
        # print()
        # print(Fore.LIGHTWHITE_EX + 'Number Armors Forged: ', self.number_of_armors)
        # print(Fore.LIGHTWHITE_EX + f'{self.order_name} Armor Shipping LABEL: ', self.apack['armor_name'][1])
        # print(Fore.LIGHTRED_EX + 150 * '-')
        # print(Fore.LIGHTYELLOW_EX + 'ARMOR SETS PACKED:> ', self.order_name, self.apack)
        # print(Fore.LIGHTRED_EX + 150 * '-')

    def pick_weapon_type(self):
        self.weapon_id = 0
        self.weapon_type = random.choices(self.weapon_list['Name'], weights=[5, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], k=1)
        for item in self.weapon_type:
            self.weapon_name = item
        for item in self.weapon_list['Name']:
            if item == self.weapon_name:
                break
            self.weapon_id += 1

    def wpick_material(self):
        self.material_id = 0
        if self.weapon_list['Material_base'][self.weapon_id] == 'ore':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[30, 150, 50, 25, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                k=1)
        elif self.weapon_list['Material_base'][self.weapon_id] == 'leather':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 50, 40, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                k=1)
        elif self.weapon_list['Material_base'][self.weapon_id] == 'linen':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 20, 3, 1, 0, 0, 0, 0, 0, 0],
                                                k=1)
        elif self.weapon_list['Material_base'][self.weapon_id] == 'wood':
            self.material_type = random.choices(self.material_list['Name'],
                                                weights=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 10, 5, 2, 1, 0],
                                                k=1)

        for item in self.material_type:
            self.material_type = item
        for item in self.material_list['Name']:
            if item == str(self.material_type):
                self.material_type = item
                break
            self.material_id += 1

    def create_weapon(self):
        self.crafted_id = 0
        self.weapon_smith = 90
        self.armor_worked = 0
        self.crafting_modifier = 0
        self.weapon_worked = self.weapon_list['Create_base_chance'][self.weapon_id]
        self.weapon_worked += self.material_list['Create_mod'][self.material_id]
        self.weapon_worked += self.weapon_smith
        for creating in range(1, 7):
            self.processing = random.randint(1, 100 - self.weapon_smith)
            if self.processing <= self.weapon_worked:
                self.outcome = 'Success!'
                self.crafting_modifier += 1
            else:
                self.outcome = 'Failure~'
        match self.crafting_modifier:
            case 0:
                a = 25; b = 50; c = 100; d = 5; e = 1; f = 1; g = 1
            case 1:
                a = 5; b = 55; c = 100; d = 10; e = 5; f = 1; g = 1
            case 2:
                a = 5; b = 5; c = 200; d = 10; e = 10; f = 5; g = 1
            case 3:
                a = 1; b = 3; c = 100; d = 25; e = 10; f = 5; g = 1
            case 4:
                a = 1; b = 5; c = 100; d = 5; e = 1; f = 1; g = 1
            case 5:
                a = 1; b = 5; c = 150; d = 50; e = 10; f = 1; g = 1
            case 6:
                a = 1; b = 2; c = 100; d = 75; e = 50; f = 15; g = 5
        self.weapon_craftmanship = random.choices(self.craftmanship_list['Name'], weights=[a, b, c, d, e, f, g], k=1)
        item = ''.join(self.weapon_craftmanship)
        for name in self.craftmanship_list['Name']:
            if item == name:
                break
            self.crafted_id += 1
        for item in self.weapon_craftmanship:
            self.weapon_crafted = item

    def Weapon_condition(self):
        self.condition_id = 0
        self.weapon_condition = random.choices(self.condition_list['Name'], weights=[1, 3, 10, 50, 5], k=1)
        self.item = ''.join(self.weapon_condition)
        for name in self.condition_list['Name']:
            if self.item == name:
                break
            self.condition_id += 1
        for item in self.weapon_condition:
            self.weapon_condition = item

    def Weapon_cost(self):
        self.weapon_cost = 0
        self.material_cost = 0
        self.crafted_cost = 0
        self.weapon_cost = self.weapon_list['Base_Cost'][self.weapon_id]
        self.material_cost = self.material_list['Cost_per_unit'][self.material_id] * self.weapon_list['Material_Quantity'][self.weapon_id]
        self.weapon_cost += self.material_cost
        self.crafted_cost = self.weapon_cost * self.craftmanship_list['Cost_mod'][self.crafted_id]
        self.weapon_cost = self.crafted_cost
        int(self.weapon_cost)
        self.condition = self.weapon_cost * self.condition_list['Cost_mod'][self.condition_id]
        self.weapon_cost = int(self.condition)

    def Weapon_stats(self):
        self.type_of_weapon = self.weapon_list['Name']
        self.dice_type = self.weapon_list['Dice_Type'][self.weapon_id]
        self.damage_modifier = self.weapon_list['Damage_Modifier'][self.weapon_id]
        self.rdamage_modifier = self.weapon_list['RDamage_Modifier'][self.weapon_id]
        self.to_hit_modifier = self.weapon_list['To_Hit_Modifier'][self.weapon_id]
        self.rto_hit_modifier = self.weapon_list['RTo_Hit_Modifier'][self.weapon_id]
        self.range_distance = self.weapon_list['Range_Distance'][self.weapon_id]
        self.thrown_distance = self.weapon_list['Thrown_Distance'][self.weapon_id]
        self.parry = self.weapon_list['parry'][self.weapon_id]
        self.block = self.weapon_list['block'][self.weapon_id]
        self.block_resist = self.weapon_list['block_resist'][self.weapon_id]
        self.reach = self.weapon_list['weapon_reach'][self.weapon_id]
        self.weapon_speed = self.weapon_list['weapon_speed'][self.weapon_id]
        self.hands_needed = self.weapon_list['Hands_Needed'][self.weapon_id]
        self.damage_type = self.weapon_list['Damage_Type'][self.weapon_id]
        self.weapon_type = self.weapon_list['Weapon_Type'][self.weapon_id]
        self.durability = 0
        self.durability = int(self.weapon_list['Base_Durability'][self.weapon_id] + self.material_list['Durability'][
            self.material_id])
        # print(Fore.LIGHTYELLOW_EX + 'DICE USED: ', self.dice_type)
        # print(Fore.LIGHTCYAN_EX + 'Condition modifier: ', self.condition_list['stat_mod'][self.condition_id])
        # print(Fore.LIGHTBLUE_EX + 'Craftmanship modifier: ', self.craftmanship_list['stat_mod'][self.crafted_id])
        if self.craftmanship_list['Durability'][self.crafted_id] != 0:
            self.durability *= self.craftmanship_list['Durability'][self.crafted_id]
        if self.condition_list['Durability'][self.condition_id] != 0:
            self.durability *= self.condition_list['Durability'][self.condition_id]
        self.durability = int(self.durability)
        if self.weapon_list['Weapon_Type'][self.weapon_id] =='melee' or self.weapon_list['Weapon_Type'][self.weapon_id] =='both':
            self.to_hit_modifier = int(self.to_hit_modifier + self.material_list['Stat_Mod'][self.material_id])
            self.dice_type = int(self.dice_type + self.material_list['Stat_Mod'][self.material_id])
            self.damage_modifier = int(self.damage_modifier + self.craftmanship_list['stat_mod'][self.crafted_id])
            self.to_hit_modifier = int(self.to_hit_modifier + self.craftmanship_list['stat_mod'][self.crafted_id])
            self.dice_type = int(self.dice_type + self.craftmanship_list['stat_mod'][self.crafted_id])
            self.damage_modifier = int(self.damage_modifier + self.condition_list['stat_mod'][self.condition_id])
            if self.condition_list['stat_mod'][self.condition_id] != 0:
                self.dice_type = int(self.dice_type * self.condition_list['stat_mod'][self.condition_id])
            self.to_hit_modifier = int(self.to_hit_modifier + self.condition_list['stat_mod'][self.condition_id])
            if self.damage_modifier < 0:
                self.damage_modifier = 0
            if self.to_hit_modifier < 0:
                self.to_hit_modifier = 0
        else:
            self.rdamage_modifier = self.rdamage_modifier + self.material_list['Stat_Mod'][self.material_id]
            self.rto_hit_modifier = self.material_list['Stat_Mod'][self.material_id]
            self.dice_type += self.material_list['Stat_Mod'][self.material_id]
            self.rdamage_modifier += self.craftmanship_list['stat_mod'][self.crafted_id]
            self.rto_hit_modifier += self.craftmanship_list['stat_mod'][self.crafted_id]
            self.rdamage_modifier += self.condition_list['stat_mod'][self.condition_id]
            self.rto_hit_modifier += self.condition_list['stat_mod'][self.condition_id]
            self.dice_type = int(self.dice_type + self.craftmanship_list['stat_mod'][self.crafted_id])
            self.dice_type = int(self.dice_type + self.condition_list['stat_mod'][self.condition_id])
            if self.rdamage_modifier < 0:
                self.rdamage_modifier = 0
            if self.rto_hit_modifier < 0:
                self.rto_hit_modifier = 0

    def Weapon_magic(self):
        self.enchant_id = 0
        self.magic = ''
        self.magic_limit = 0
        self.magic_limit = self.material_list['Enchant_base'][self.material_id] + self.craftmanship_list['Enchant_mod'][
            self.crafted_id]


        self.magic_bonus = random.choices(self.enchant_list['Name'], weights=[100, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
        self.magic = ''.join(self.magic_bonus)
        self.enchant_id = self.magic.replace('+', '')
        self.enchant_id = int(self.enchant_id)



        if self.enchant_id > self.magic_limit:
            if self.magic_limit >= 2:
                x = random.randint(1, self.magic_limit)
                self.enchant_id = x
            else:
                self.enchant_id = self.magic_limit

        if self.magic == '0':
            self.magic = ''
        else:
            self.magic = '+' + str(self.enchant_id)


        if self.weapon_list['Weapon_Type'][self.weapon_id] == 'M' or self.weapon_list['Weapon_Type'][self.weapon_id] == 'B':
            self.to_hit_modifier += self.enchant_id
            self.dice_type += self.enchant_id
            self.damage_modifier += self.enchant_id
            self.weapon_cost += self.enchant_list['Cost_mod'][self.enchant_id]
            self.durability += self.enchant_list['durability'][self.enchant_id]
            self.magic = self.enchant_list['Name'][self.enchant_id]
        else:
            self.rto_hit_modifier += self.enchant_id
            self.dice_type += self.enchant_id
            self.rdamage_modifier += self.enchant_id
            self.weapon_cost += self.enchant_list['Cost_mod'][self.enchant_id]
            self.durability += self.enchant_list['durability'][self.enchant_id]
            self.magic = self.enchant_list['Name'][self.enchant_id]

        if self.magic == '0':
            self.magic = ''

   ############################################
                     ### -____WEAPON ORDER______-###
   ############################################

    def weapon_order(self, num):
        weapon_forged = ''
        clear_wpack = {'name': [],
                         'name_type': [],  # longsword, dagger, longbow ect...
                         'made_of': [],
                         'cost': [],
                         'weapon_type': [],  # if melee, range or thrown
                         'damage_type': [],
                         'dice_type': [],
                         'damage_modifier': [],
                         'to_hit_modifier': [],
                         'range_distance': [],
                         'parry': [],
                         'block': [],
                         'block_resist': [],
                         'weapon_reach': [],
                         'weapon_speed': [],
                         'hands_needed': [],
                         'magic_modifier': [],
                         'magic_limit': [],
                         'craftsmanship': [],
                         'condition_': [],
                         'durability': [],
                         'crafted_by': [],
                         'enchanted_by': [],
                         'creation_date': [],
                         'origin': []
                       }
        self.wpack.clear()
        self.wpack = dict(clear_wpack)

        self.number_of_weapons = num
        for count in range(1, self.number_of_weapons +1):
            self.pick_weapon_type()
            self.wpick_material()
            self.create_weapon()
            self.Weapon_condition()
            self.Weapon_cost()
            self.Weapon_stats()
            self.Weapon_magic()
            COLORNAME = 'LIGHTCYAN_EX'
            color = getattr(Fore, COLORNAME)
            if self.condition_list['Name'][self.condition_id] == 'Pristine':
                COLORNAME3 = 'LIGHTWHITE_EX'
                color3 = getattr(Fore, COLORNAME3)
            elif self.condition_list['Name'][self.condition_id] == 'Battered' or self.condition_list['Name'][
                self.condition_id] == 'Poor':
                COLORNAME3 = 'LIGHTRED_EX'
                color3 = getattr(Fore, COLORNAME3)
            else:
                COLORNAME3 = 'LIGHTCYAN_EX'
                color3 = getattr(Fore, COLORNAME3)
            if self.craftmanship_list['Name'][self.crafted_id] == 'Horrible' or self.craftmanship_list['Name'][
                self.crafted_id] == 'Flawed':
                COLORNAME = 'LIGHTRED_EX'
                color = getattr(Fore, COLORNAME)
            else:
                COLORNAME = 'LIGHTCYAN_EX'
                color = getattr(Fore, COLORNAME)
            if self.craftmanship_list['Name'][self.crafted_id] == 'Exceptional' or self.craftmanship_list['Name'][
                self.crafted_id] == 'Fine':
                COLORNAME = 'LIGHTBLUE_EX'
                color = getattr(Fore, COLORNAME)
            if self.craftmanship_list['Name'][self.crafted_id] == 'Exquisite':
                COLORNAME = 'LIGHTMAGENTA_EX'
                color = getattr(Fore, COLORNAME)
            if self.craftmanship_list['Name'][self.crafted_id] == 'Flawless':
                COLORNAME = 'LIGHTYELLOW_EX'
                color = getattr(Fore, COLORNAME)

            if self.material_list['Name'][self.material_id] == 'Lean':
                COLORNAME2 = 'LIGHTMAGENTA_EX'
                color2 = getattr(Fore, COLORNAME2)
            elif self.material_list['Name'][self.material_id] == 'Mithril':
                COLORNAME2 = 'LIGHTGREEN_EX'
                color2 = getattr(Fore, COLORNAME2)
            elif  self.material_list['Name'][self.material_id] == 'Adamantium':
                COLORNAME2 = 'LIGHTBLUE_EX'
                color2 = getattr(Fore, COLORNAME2)
            elif self.material_list['Name'][self.material_id] == 'Crystal Lean' or self.material_list['Name'][
                self.material_id] == 'Dragon':
                COLORNAME2 = 'LIGHTYELLOW_EX'
                color2 = getattr(Fore, COLORNAME2)
            else:
                COLORNAME2 = 'LIGHTWHITE_EX'
                color2 = getattr(Fore, COLORNAME2)
            if self.damage_modifier < 0 or self.rdamage_modifier < 0:
                COLORNAME1 = 'LIGHTRED_EX'
                color1 = getattr(Fore, COLORNAME1)
            else:
                COLORNAME1 = 'LIGHTWHITE_EX'
                color1 = getattr(Fore, COLORNAME1)
            if self.to_hit_modifier == 0:
                self.displaytohit = self.dice_type
            else:
                self.displaytohit = f"{self.dice_type}+{self.damage_modifier}"
            self.x = ''.join(self.weapon_craftmanship)
            # print(self.x)
            self.h = self.material_id
            self.y = self.material_type
            # print(self.weapon_name)
            if self.material_type == 'Adamantium' and self.weapon_name and self.x == 'Exquisite':
                self.material_type = 'King Slayer'
            if self.material_type == 'Adamantium' and self.weapon_name and self.x == 'Flawless':
                self.material_type = 'Dragon Slayer'
            # if self.x == ('Flawless' or self.x == 'Exquisite') and (self.y == 'Adamantium' or self.y == 'Crystal Lean' or self.h == 19) and (self.weapon_condition != 'Battered' or self.weapon_condition != 'Poor'):
            # if self.magic == '+10':
            print(color1 + f'{count}', Fore.LIGHTMAGENTA_EX + f'{self.order_name} Weapon Forged[{self.weapon_id}]',
                  Fore.LIGHTYELLOW_EX + f'Cost: {self.weapon_cost} ',color1 + f"{self.magic_limit}",
                  color3 + f': {self.weapon_condition}',color + f', {self.weapon_crafted},',
                    color2 + f' {self.magic} {self.material_type} {self.weapon_name}',
                    color1 + f'1d{self.displaytohit}',
                    Fore.BLUE + f' Durability: {self.durability}')
            self.damage_modifier = self.to_hit_modifier
            self.Weapon_packing()
        self.Weapon_shipment()


    def Weapon_packing(self):
        # self.wpack = []

        self.weapon_origin += 1
        self.title1 = self.material_type
        self.title2 = self.weapon_name
        self.name = self.magic + ' ' + self.material_type + ' ' + self.weapon_name
        if self.magic >= '1':
            self.name += '+' + self.magic + ' '
        if self.material_type == 'Adamantium' and self.weapon_name == 'Great Sword' and  self.weapon_crafted == 'Exquisite':
            self.name = 'King Slayer'
        if self.material_type == 'Adamantium' and self.weapon_name == 'Great Sword' and  self.weapon_crafted == 'Flawless':
            self.name = 'Dragon Slayer'

        self.crafted_by = self.order_name + ' Forge'
        # self.weapon_origin = str(self.weapon_origin)
        self.wpack['name'].append(self.name)
        self.wpack['name_type'].append(self.weapon_name)
        self.wpack['made_of'].append(self.material_type)
        self.wpack['cost'].append(self.weapon_cost)
        self.wpack['weapon_type'].append(self.weapon_type)
        self.wpack['damage_type'].append(self.damage_type)
        self.wpack['dice_type'].append(self.dice_type)
        if self.weapon_type == 'R':
            self.wpack['damage_modifier'].append(int(self.rdamage_modifier))
            self.wpack['to_hit_modifier'].append(int(self.to_hit_modifier))
            self.wpack['range_distance'].append(self.range_distance)
        else:
            self.wpack['damage_modifier'].append(int(self.damage_modifier))
            self.wpack['to_hit_modifier'].append(int(self.rto_hit_modifier))
            self.wpack['range_distance'].append(self.thrown_distance)
        self.wpack['parry'].append(self.parry)
        self.wpack['block'].append(self.block)
        self.wpack['block_resist'].append(self.block_resist)
        self.wpack['weapon_reach'].append(self.reach)
        self.wpack['weapon_speed'].append(self.weapon_speed)
        self.wpack['hands_needed'].append(self.hands_needed)
        self.wpack['magic_modifier'].append(self.enchant_id)
        self.wpack['magic_limit'].append(self.magic_limit)
        self.wpack['craftsmanship'].append(self.weapon_crafted)
        self.wpack['condition_'].append(self.weapon_condition)
        self.wpack['durability'].append(self.durability)
        self.wpack['crafted_by'].append(self.crafted_by)
        self.wpack['enchanted_by'].append(self.crafted_by)
        self.wpack['creation_date'].append(self.creation)
        self.wpack['origin'].append(self.weapon_origin)
    def Weapon_shipment(self):
        self.count = 0
        print()
        print(Fore.LIGHTWHITE_EX + f'{self.order_name} weapon shipping Label')
        for key, value in self.wpack.items():
            pass
        #     print()
        #     print(Fore.LIGHTYELLOW_EX + f'{key}:',Fore.LIGHTCYAN_EX + f'{value[0]} ', end='')
        #
        #
        # print(Fore.LIGHTMAGENTA_EX + '_' * 150)
        # print()
        # for key, value in self.wpack.items():
        #     # pass
        #     print()
        #     print(Fore.LIGHTYELLOW_EX + f'{key}: ', end='')
        #     for item in value:
        #         val = str(item)
        #         print(Fore.LIGHTWHITE_EX + f'[{self.count}]', Fore.LIGHTCYAN_EX + f'{val}, ', end='')
        #         self.count += 1
        #     self.count = 0
        #     print()
        # print()
        # print(Fore.LIGHTMAGENTA_EX + '_' * 150)
        # print()
        # print()
        # print(Fore.LIGHTWHITE_EX + 'Number Weapons Forged: ', self.number_of_weapons)
        # print(Fore.LIGHTWHITE_EX + f'{self.order_name} Weapon Shipping LABEL: ', self.wpack['name'][0])
        # print(Fore.LIGHTRED_EX + 150 * '-')
        # print(Fore.LIGHTYELLOW_EX + 'WEAPONS PACKED:> ', self.order_name, self.wpack)
        # print(Fore.LIGHTRED_EX + 150 * '-')

    def forged_weapon(self):
        self.weapon_order(num)
        # self.count = 0
        # print(Fore.LIGHTYELLOW_EX + '{______Choose a Weapon Number______}')
        # print()
        # self.item = self.wpack['weapon_name']
        #
        # for self.plist in self.item:
        #     print(Fore.LIGHTWHITE_EX + f'{self.count}..........',Fore.LIGHTCYAN_EX + f'{self.plist}')
        #     self.count += 1
        # print()
        # self.count -= 1
        # self.response = int(input(Fore.LIGHTCYAN_EX + f'Pick a Number from (0-{self.count}):>? '))
        # print()
        # print(Fore.LIGHTBLUE_EX + 'WEAPON STATS:')
        # for key, value in self.wpack.items():
        #     print()
        #     print(Fore.LIGHTYELLOW_EX + f'{key}:', Fore.LIGHTCYAN_EX + f'{value[self.response]} ', end='')

        # self.data()
        # self.armor_order(self)
        # self.weapon_order(self)

    # def data(self):
    #     for loop in range(0, 7):
    #         print()
    #         print(Fore.LIGHTMAGENTA_EX + '_' * 150)
    #         print()
    #         match loop:
    #             case 0:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Weapons Data \____')
    #                 self.main_list = self.weapon_list
    #             case 1:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Armors Data \____')
    #                 self.main_list = self.armor_list
    #             case 2:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Material Data \____')
    #                 self.main_list = self.material_list
    #             case 3:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Craftmanship Data \____')
    #                 self.main_list = self.craftmanship_list
    #             case 4:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Condition Data \____')
    #                 self.main_list = self.condition_list
    #             case 5:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Enchant Data \____')
    #                 self.main_list = self.enchant_list
    #             case 6:
    #                 print(Fore.LIGHTYELLOW_EX + '____/ Enchant Element Data \____')
    #                 self.main_list = self.enchant_element_list
    #
    #         count = 0
    #         # item_list = []
    #         for key, value in self.main_list.items():
    #             print()
    #             print(Fore.LIGHTYELLOW_EX + f'{key}: ', end='')
    #             for item in value:
    #                 val = str(item)
    #                 print(Fore.LIGHTWHITE_EX + f'[{count}]', Fore.LIGHTCYAN_EX + f'{val}, ', end='')
    #                 count += 1
    #             count = 0
    #             print()
    #     print()
    #     print(Fore.LIGHTMAGENTA_EX + '_' * 150)
    #     print()
    # # data(self)

    def armor_appraisal(self, char, armor, craftmanship, condition):
        # This function retrieves list number of said item from master lists
        # Cross-references them to find exacting data not assigned to the character dbase.
        # To use to analyse value, use of material, stats, costs and values and so on.
        # Main functino ability is:, list number for order where information stored in other keys
        # and ability to access other keys to evaluate  for an appraisal.
        # print(Fore.LIGHTGREEN_EX + f"{char}")
        # print()
        # print("ARMOR: ", armor)
        # print('CRAFTMANSHIP:',craftmanship)
        # print('CONDITION:', condition)
        self.char = char
        mgcount = 0
        #  Magical Value evaluation
        for self.magic in self.enchant_list['Name']:
            if armor.find('+') == 0:
                self.magic = self.magic + ' '
                if armor.find(self.magic) == 0:
                    break
                mgcount += 1

        marmor = armor.replace(self.magic, '')
        # print('ARMOR WITHOUT + : ', marmor)
        # print(mgcount)
        # print(marmor)
        plusarmor = mgcount
        if mgcount == 0:
            plusarmor = 'None'
        else:
            plusarmor = '+' + str(mgcount)

        cha_bonus_penalty = self.char['cha_cost_modifier']
        cha_bonus_penalty = 1 - float(cha_bonus_penalty)
        cha_bonus_penalty = 1 + float(cha_bonus_penalty)
        mvalue = self.enchant_list['Cost_mod'][mgcount]
        msvalue = int(self.enchant_list['Cost_mod'][mgcount])

        mtcount = 0
        for material in self.material_list['Name']:


            if marmor.find('Crystal Lean') >= 0:
                self.material = 'Crystal Lean'
                self.Oarmor = marmor.replace('Crystal Lean', '')
                self.Oarmor = self.Oarmor.lstrip()
                Aarmor = marmor.replace(' ', '')
                mtcount = 5
                break

            if marmor.find('Dragon Hide') >= 0:
                self.material = 'Dragon Hide'
                self.Oarmor = marmor.replace('Dragon Hide', '')
                self.Oarmor = self.Oarmor.lstrip()
                Aarmor = marmor.replace(' ', '')
                mtcount = 9
                break

            if marmor.find('Leather Laced') >= 0:
                self.material = 'Leather Laced'
                self.Oarmor = marmor.replace('Leather Laced', '')
                self.Oarmor = self.Oarmor.lstrip()
                Aarmor = marmor.replace(' ', '')
                mtcount = 11  # use on cost modifier in material
                break


            if marmor.find(material) >= 0:
                self.material = material
                self.Oarmor = marmor.replace(material, '')
                self.Oarmor = self.Oarmor.lstrip()
                Aarmor = marmor.replace(' ', '')
                break
            # print(marmor.find(material))
            mtcount += 1
        # print("material count:", mtcount)
        # print(self.Oarmor)
        arcount = 0
        for armor_set in self.armor_list['Name']:
            # print(Fore.LIGHTRED_EX + f"{armor_set}.  {self.Oarmor}")
            if armor_set == self.Oarmor:
                # print(Fore.LIGHTRED_EX + f"{arcount}.  {self.Oarmor}")
                armor_units = self.armor_list['Material_Quantity'][arcount]
                base_armor_set_cost = str(self.armor_list['Base_Cost'][arcount])
                material_unit_cost = str(self.material_list['Cost_per_unit'][mtcount])
                break
            arcount += 1
        # print('armor count', arcount)
        # print(armor_units)
        crafted_item = vars
        self.crafted_item = crafted_item
        crafted_listnumber = 0
        for self.crafted_item in self.craftmanship_list['Name']:  # retrieve the list number of the key
            if craftmanship == self.crafted_item:
                break
            crafted_listnumber += 1
        craft_cost_mod = self.craftmanship_list['Cost_mod'][crafted_listnumber]  # using the list number on key found
        print(Fore.LIGHTWHITE_EX + f"\n~Craftmanship Detail~")
        print(Fore.LIGHTWHITE_EX+ f"Crafted Details: {crafted_listnumber}, {self.crafted_item}, {craft_cost_mod}")
        print(Fore.LIGHTMAGENTA_EX + f"List N#: {crafted_listnumber}\nCrafted state: {self.crafted_item}\nCost Modifier: {craft_cost_mod}")

        item_condition = vars
        self.item_condition = item_condition
        con_listnumber = 0
        for self.item_condition in self.condition_list['Name']:  # retrieve the list number of the key
            if condition == self.item_condition:
                break
            con_listnumber += 1
        con_cost_mod = self.condition_list['Cost_mod'][con_listnumber]
        print(Fore.LIGHTWHITE_EX + f"\n~Condition Detail~")
        print(Fore.LIGHTMAGENTA_EX + f"List N#: {con_listnumber}\nCondition state: {self.item_condition}\nCost Modifier: {con_cost_mod}")


        print()
        print(Fore.LIGHTWHITE_EX + f"Armor components for:",Fore.LIGHTGREEN_EX + char['armor_worn'])
        print(Fore.LIGHTWHITE_EX + f"    Armor Set:",Fore.LIGHTRED_EX + self.Oarmor)
        print(Fore.LIGHTWHITE_EX + f"    {self.Oarmor} (Base) Cost:", Fore.LIGHTRED_EX + f"{base_armor_set_cost}gp")
        print(Fore.LIGHTWHITE_EX + f"    Magic found:", Fore.LIGHTBLUE_EX + plusarmor)
        print(Fore.LIGHTWHITE_EX + f"    (Base) worth:", Fore.LIGHTBLUE_EX + f"{msvalue:<,}")
        print(Fore.LIGHTWHITE_EX + f"    Made of:", Fore.LIGHTYELLOW_EX + self.material)
        print(Fore.LIGHTWHITE_EX + f"    One unit {self.material} cost:", Fore.LIGHTYELLOW_EX + f"{material_unit_cost}gp")
        print(Fore.LIGHTWHITE_EX + f"    {self.Oarmor}s Made of: ", Fore.LIGHTYELLOW_EX + str(armor_units),
              f" units of {str(self.material)}")
        unit_sum = int(armor_units) * int(material_unit_cost)
        print(Fore.LIGHTWHITE_EX + f"    (Base) cost of {self.material}: ", Fore.LIGHTYELLOW_EX + f"{unit_sum}gp")
        total_value = int(msvalue) + int(base_armor_set_cost) + int(unit_sum)
        print(Fore.LIGHTWHITE_EX + f"Total material/magic Value: ",Fore.LIGHTGREEN_EX + f"{total_value:<,}gp")
        print()

        cvalue = int(total_value * craft_cost_mod)
        worth_of_skill = int(cvalue - total_value)
        print(Fore.LIGHTWHITE_EX + f"Quality of Armor:",Fore.LIGHTBLUE_EX + f" {craftmanship}")
        print(Fore.LIGHTWHITE_EX + f"Added Value craftmanship:",Fore.LIGHTBLUE_EX + f"  {worth_of_skill:<,}gp")
        print(Fore.LIGHTWHITE_EX + f"After Craftmanship Value/Devalue:",Fore.LIGHTBLUE_EX + f" {cvalue:<,}gp")

        convalue = int(cvalue * con_cost_mod)
        condition_affect = int(convalue - cvalue)
        print(Fore.LIGHTWHITE_EX + f"\nCondition of Armor:", Fore.LIGHTBLUE_EX + f" {condition}")
        print(Fore.LIGHTWHITE_EX + f"Condition Devalued/None:", Fore.LIGHTBLUE_EX + f"  {condition_affect:<,}gp")
        print('-' * 50)
        print(Fore.LIGHTWHITE_EX + f"Armor Appraisal Value: ", Fore.LIGHTBLUE_EX + f" {convalue:<,}gp")
        print('-' * 50)
        print()
        appraisal_value = int(convalue / 1.5)
        cha_mod = float(self.char['cha_cost_modifier'])
        print(Fore.LIGHTWHITE_EX + f"Appraisal Offer Base:",Fore.LIGHTCYAN_EX + f"{appraisal_value:<,}gp")
        print(Fore.LIGHTCYAN_EX + f"Charisma Modifier: {cha_mod}")
        print(Fore.LIGHTCYAN_EX + f"Charisma Mod Converted: {cha_bonus_penalty}")
        cappraisal = appraisal_value * cha_mod
        cappraisal = int(appraisal_value - cappraisal)
        self.final_appraisal = int(appraisal_value + cappraisal)
        print(Fore.LIGHTWHITE_EX + f"Charisma Affect Value:",Fore.LIGHTCYAN_EX + f"{cappraisal:<,}gp")
        print()
        print('-' * 50)
        print(Fore.LIGHTWHITE_EX + f"Sell Offer Value:",Fore.LIGHTCYAN_EX + f"{self.final_appraisal:<,}gp")
        print('-' * 50)
        print('\n\n\n')
        print(Fore.LIGHTWHITE_EX + "Craftmanship States")
        for c in self.craftmanship_list['Name']:
            print(Fore.LIGHTBLUE_EX + c)

        print(Fore.LIGHTWHITE_EX + "\n\nCondition States")
        for c in self.condition_list['Name']:
            print(Fore.LIGHTRED_EX + c)
        print('HERE:', self.final_appraisal)





    def weapon_appraisal(self, char, weapon,  craftmanship, condition):
        print("weapon: ", weapon)
        self.char = char
        mgcount = 0
        #  Magical Value evaluation
        self.title_name = weapon
        title_name = weapon
        for self.magic in self.enchant_list['Name']:
            if weapon.find('+') == 0:
                self.magic = self.magic + ' '
                if weapon.find(self.magic) == 0:
                    break
                mgcount += 1

        mweapon = weapon.replace(self.magic, '')
        print('weapon WITHOUT + : ', mweapon)
        print(mgcount)
        print(mweapon)
        plusarmor = mgcount
        if mgcount == 0:
            plusarmor = 'None'
        else:
            plusarmor = '+' + str(mgcount)

        cha_bonus_penalty = self.char['cha_cost_modifier']
        cha_bonus_penalty = 1 - float(cha_bonus_penalty)
        cha_bonus_penalty = 1 + float(cha_bonus_penalty)
        mvalue = self.enchant_list['Cost_mod'][mgcount]
        msvalue = int(self.enchant_list['Cost_mod'][mgcount])

        mtcount = 0
        for material in self.material_list['Name']:

            if mweapon.find('Crystal Lean') >= 0:
                self.material = 'Crystal Lean'
                self.Oweapon = mweapon.replace('Crystal Lean', '')
                self.Oweapon = self.Oweapon.lstrip()
                Aarmor = mweapon.replace(' ', '')
                mtcount = 5
                break

            if mweapon.find('Dragon Hide') >= 0:
                self.material = 'Dragon Hide'
                self.Oweapon = mweapon.replace('Dragon Hide', '')
                self.Oweapon = self.Oweapon.lstrip()
                Aarmor = mweapon.replace(' ', '')
                mtcount = 9
                break

            if mweapon.find('Leather Laced') >= 0:
                self.material = 'Leather Laced'
                self.Oweapon = mweapon.replace('Leather Laced', '')
                self.Oweapon = self.Oweapon.lstrip()
                Aarmor = mweapon.replace(' ', '')
                mtcount = 11  # use on cost modifier in material
                break

            if mweapon.find(material) >= 0:
                self.material = material
                self.Oweapon = mweapon.replace(material, '')
                self.Oweapon = self.Oweapon.lstrip()
                Aarmor = mweapon.replace(' ', '')
                break
            print(mweapon.find(material))
            mtcount += 1
        print("material count:", mtcount)
        print(self.Oweapon)
        arcount = 0
        for Weapon in self.weapon_list['Name']:
            print(Fore.LIGHTRED_EX + f"{Weapon}.  {self.Oweapon}")
            if Weapon == self.Oweapon:
                print(Fore.LIGHTRED_EX + f"{arcount}.  {self.Oweapon}")
                weapon_units = self.weapon_list['Material_Quantity'][arcount]
                base_weapon_cost = str(self.weapon_list['Base_Cost'][arcount])
                material_unit_cost = str(self.material_list['Cost_per_unit'][mtcount])
                break
            arcount += 1
        print('weapon count', arcount)
        print(weapon_units)
        crafted_item = vars
        self.crafted_item = crafted_item
        crafted_listnumber = 0
        for self.crafted_item in self.craftmanship_list['Name']:  # retrieve the list number of the key
            if craftmanship == self.crafted_item:
                break
            crafted_listnumber += 1
        craft_cost_mod = self.craftmanship_list['Cost_mod'][crafted_listnumber]  # using the list number on key found
        print(Fore.LIGHTWHITE_EX + f"\n~Craftmanship Detail~")
        print(Fore.LIGHTWHITE_EX + f"Crafted Details: {crafted_listnumber}, {self.crafted_item}, {craft_cost_mod}")
        print(
            Fore.LIGHTMAGENTA_EX + f"List N#: {crafted_listnumber}\nCrafted state: {self.crafted_item}\nCost Modifier: {craft_cost_mod}")

        item_condition = vars
        self.item_condition = item_condition
        con_listnumber = 0
        for self.item_condition in self.condition_list['Name']:  # retrieve the list number of the key
            if condition == self.item_condition:
                break
            con_listnumber += 1
        con_cost_mod = self.condition_list['Cost_mod'][con_listnumber]
        print(Fore.LIGHTWHITE_EX + f"\n~Condition Detail~")
        print(
            Fore.LIGHTMAGENTA_EX + f"List N#: {con_listnumber}\nCondition state: {self.item_condition}\nCost Modifier: {con_cost_mod}")

        print()
        print(Fore.LIGHTWHITE_EX + f"Weapon components for:", Fore.LIGHTGREEN_EX + title_name)
        print(Fore.LIGHTWHITE_EX + f"    Weapon Type:", Fore.LIGHTRED_EX + self.Oweapon)
        print(Fore.LIGHTWHITE_EX + f"    {self.Oweapon} (Base) Cost:", Fore.LIGHTRED_EX + f"{base_weapon_cost}gp")
        print(Fore.LIGHTWHITE_EX + f"    Magic found:", Fore.LIGHTBLUE_EX + plusarmor)
        print(Fore.LIGHTWHITE_EX + f"    (Base) worth:", Fore.LIGHTBLUE_EX + f"{msvalue:<,}")
        print(Fore.LIGHTWHITE_EX + f"    Made of:", Fore.LIGHTYELLOW_EX + self.material)
        print(Fore.LIGHTWHITE_EX + f"    One unit {self.material} cost:",
              Fore.LIGHTYELLOW_EX + f"{material_unit_cost}gp")
        print(Fore.LIGHTWHITE_EX + f"    {self.Oweapon}s Made of: ", Fore.LIGHTYELLOW_EX + str(weapon_units),
              f" units of {str(self.material)}")
        unit_sum = int(weapon_units) * int(material_unit_cost)
        print(Fore.LIGHTWHITE_EX + f"    (Base) cost of {self.material}: ", Fore.LIGHTYELLOW_EX + f"{unit_sum}gp")
        total_value = int(msvalue) + int(base_weapon_cost) + int(unit_sum)
        print(Fore.LIGHTWHITE_EX + f"Total material/magic Value: ", Fore.LIGHTGREEN_EX + f"{total_value:<,}gp")
        print()

        cvalue = int(total_value * craft_cost_mod)
        worth_of_skill = int(cvalue - total_value)
        print(Fore.LIGHTWHITE_EX + f"Quality of Armor:", Fore.LIGHTBLUE_EX + f" {craftmanship}")
        print(Fore.LIGHTWHITE_EX + f"Added Value craftmanship:", Fore.LIGHTBLUE_EX + f"  {worth_of_skill:<,}gp")
        print(Fore.LIGHTWHITE_EX + f"After Craftmanship Value/Devalue:", Fore.LIGHTBLUE_EX + f" {cvalue:<,}gp")

        convalue = int(cvalue * con_cost_mod)
        condition_affect = int(convalue - cvalue)
        print(Fore.LIGHTWHITE_EX + f"\nCondition of Armor:", Fore.LIGHTBLUE_EX + f" {condition}")
        print(Fore.LIGHTWHITE_EX + f"Condition Devalued/None:", Fore.LIGHTBLUE_EX + f"  {condition_affect:<,}gp")
        print('-' * 50)
        print(Fore.LIGHTWHITE_EX + f"Armor Appraisal Value: ", Fore.LIGHTBLUE_EX + f" {convalue:<,}gp")
        print('-' * 50)
        print()
        appraisal_value = int(convalue / 1.5)
        cha_mod = float(self.char['cha_cost_modifier'])
        print(Fore.LIGHTWHITE_EX + f"Appraisal Offer Base:", Fore.LIGHTCYAN_EX + f"{appraisal_value:<,}gp")
        print(Fore.LIGHTCYAN_EX + f"Charisma Modifier: {cha_mod}")
        print(Fore.LIGHTCYAN_EX + f"Charisma Mod Converted: {cha_bonus_penalty}")
        cappraisal = appraisal_value * cha_mod
        cappraisal = int(appraisal_value - cappraisal)
        self.final_appraisal = int(appraisal_value + cappraisal)
        print(Fore.LIGHTWHITE_EX + f"Charisma Affect Value:", Fore.LIGHTCYAN_EX + f"{cappraisal:<,}gp")
        print()
        print('-' * 50)
        print(Fore.LIGHTWHITE_EX + f"Sell Offer Value:", Fore.LIGHTCYAN_EX + f"{self.final_appraisal:<,}gp")
        print('-' * 50)
        print('\n\n\n')
        print(Fore.LIGHTWHITE_EX + "Craftmanship States")
        for c in self.craftmanship_list['Name']:
            print(Fore.LIGHTBLUE_EX + c)

        print(Fore.LIGHTWHITE_EX + "\n\nCondition States")
        for c in self.condition_list['Name']:
            print(Fore.LIGHTRED_EX + c)
        print('HERE:', self.final_appraisal)

# Call FUNCTIONS OF THE CLASS

if __name__ in '__main__':
    num = 10000
    filter = 1

    opal = Forge('Opal')
    freeport = Forge('Freeport')
    print("\n"*3)
    question = input("Do you want to filter search?(Yes or No)? ")
    if question == "n" or question == 'N' or question == 'No' or question == "no":
        freeport.armor_order(num, 0, 'All', 'All', 'All', 'All', 0)
    elif question == "y" or question == 'Y' or question == 'Yes' or question == "yes":
        count = int(input("\nEnter amount of armors to generation? "))
        num = count
        print("\n" * 30)
        print("   {-Armor Condition-}")
        print("1....Battered")
        print("2....Worn")
        print("3....Good")
        print("4....Pristine")
        con = int(input("\nEnter Armor Condition to search for or hit <0> for ALL: "))

        cond = ["All","Battered","Worn","Good","Pristine"]
        condition_name = cond[con]
        print("\n" * 30)
        print("   {-Armor Craftsmanship-}")
        print("1....Horrible")
        print("2....Flawed")
        print("3....Standard")
        print("4....Fine")
        print("5....Exceptional")
        print("6....Exquisite")
        print("7.... Flawless")
        cra = int(input("\nEnter Armor Craftsmanship to search for or hit <0> for ALL: "))

        crafts = ['All', 'Horrible', 'Flawed', 'Standard', 'Fine',
                    'Exceptional', 'Exquisite', 'Flawless']
        craftsmanship_name = crafts[cra]
        print("\n" * 30)
        print("   {-Armor Made of-}")
        print("1....Bronze")
        print("2....Iron")
        print("3....Lean")
        print("4....Mithril")
        print("5....Adamanite")
        print("6....Crystal Lean")
        print("7....Leather")
        print("8.... Wilkwork")
        print("9.... Drow~Kyn")
        print("10.... Dragon Hide")
        print("11.... Cloth")
        print("12.... Leather Laced")
        print("13.... Elven Weave")
        print("14.... Everflow")
        print("15.... Oaken")
        print("16.... Dry-knot")
        print("17.... Silkwood")
        print("18.... El-spring")
        print("19.... Reen")
        print("20.... Dragon")

        mat = int(input("\nEnter what the Armor is Made of to search for or hit <0> for ALL: "))

        material = ['All', 'Bronze', 'Iron', 'Lean', 'Mithril',
                    'Adamanite', 'Crystal Lean', 'Leather', 'Leather Laced'
                    'Wilkwork', 'Drow~Kyn', 'Dragon Hide', 'Cloth',
                    'Leather Laced', 'Elven Weave', 'Everflow', 'Oaken',
                    'Dry-knot', 'Silkwood', 'El-spring', 'Reen', 'Dragon']
        material_name = material[mat]
        print("\n" * 30)
        print("   {-Armor Set-}")
        print("1....Full Platemail")
        print("2....Platemail")
        print("3....Banded mail")
        print("4....Chainmail")
        print("5....Scalemail")
        print("6....Ringmail")
        print("7....Studded Armor")
        print("8....Armor")
        print("9....Padded Armor")
        print("10....Attire")
        print("11....Scale Armor")
        armor = int(input("\nEnter Armor Condition to search for or hit <0> for ALL: "))


        armors = ['All', 'Full Platemail', 'Platemail', 'Banded mail', 'Chainmail', 'Scalemail', 'Ringmail',
                'Studded Armor', 'Armor', 'Padded Armor', 'Attire', 'Scale Armor']
        armor_name = armors[armor]
        print()
        enchant = int(input(Fore.LIGHTBLUE_EX + "Enter from 1-10 the + enchantment or <0> for NONE: "))
        print()
        print(Fore.LIGHTYELLOW_EX + f"Armor Set:",Fore.LIGHTCYAN_EX + f"{armor_name}")
        print(Fore.LIGHTYELLOW_EX + "Made of:",Fore.LIGHTMAGENTA_EX + f"{material_name}")
        print(Fore.LIGHTYELLOW_EX + "Craftsmanship:",Fore.LIGHTBLUE_EX + f"{craftsmanship_name}")
        print(Fore.LIGHTYELLOW_EX + "Condition:",Fore.LIGHTWHITE_EX + f"{condition_name}")
        if enchant == 0:
            print(Fore.LIGHTYELLOW_EX + "Enchant +:", Fore.LIGHTWHITE_EX + "None")
        elif enchant > 0:
            print(Fore.LIGHTYELLOW_EX + "Enchant +:",Fore.LIGHTGREEN_EX + f"+{enchant}")
        print()
        print(Fore.LIGHTGREEN_EX + "Seeking...")
        print()
        freeport.armor_order(num, 1, condition_name, craftsmanship_name, material_name, armor_name, enchant)
    # freeport.data()
    # print(dir({}))
    # print()

    print()
    # print(freeport.weapon_list.items())
    # freeport.weapon_order(num)
    # print('BASE ', num)
    # opal.armor_order(num)
    # opal.forged_weapon()
    # accessL = Load_Master('charload', 'Sigra')
    # char = accessL.name
    # charsave(char)

    # name = '+10 Adamantium Full Platemail'
    # craftmanship = 'Fine'
    # condition = 'Pristine'
    # for key, value in char.items():
    #     print(key, value)
    # char['armor_worn']
    # opal.armor_appraisal(char, char['armor_worn'], char['armor_craftmanship'], char['armor_condition'])



