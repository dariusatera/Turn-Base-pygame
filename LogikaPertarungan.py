from abc import ABC, abstractmethod
import random
import time

#SUPERCLASS#
class karakter (ABC):
    def __init__(self, nama, MXhp, atk,spd): # properties
        self.nama = nama
        self.hp = MXhp
        self.MXhp = MXhp 
        self.atk = atk
        self.spd = spd
        
    @abstractmethod    
    def BasicAttack(self, target):
        pass
        
    def Skill(self, target):
        pass
    
    def Ultimate(self, target=None, party=None):
        pass
    
    def is_alive(self):
        return self.hp > 0
    
#SUBCLASS# 

#Party
class Slayer(karakter):
    def BasicAttack(self, target):
        damage = int(self.atk * 0.9)  # Basic Attack memberikan 90% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Basic Attack pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")

    def Skill(self, target):
        damage = int(self.atk * 2)  # Skill memberikan 200% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Skill pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")

    def Ultimate(self, target):
        damage = int(self.atk * 3.5)  # Ultimate memberikan 350% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Ultimate pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")
        
class Mage(karakter):
    def BasicAttack(self, target):
        damage = int(self.atk * 0.9)  # Basic Attack memberikan 90% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Basic Attack pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")

    def Skill(self,target_index, targets):
         # Target utama menerima 150% damage
        target = targets[target_index]
        damage_main = int(self.atk * 1.5)
        target.hp -= damage_main
        print(f"{self.nama} menyerang {target.nama} dan memberikan {damage_main} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")

        # Target di kiri dan kanan menerima 50% damage
        damage_aoe = int(self.atk * 0.5)
        if target_index - 1 >= 0 and targets[target_index - 1].is_alive():  # Target di kiri
            left_target = targets[target_index - 1]
            left_target.hp -= damage_aoe
            print(f"{left_target.nama} terkena serangan area dan menerima {damage_aoe} damage!")
            print(f"{left_target.nama} tersisa {left_target.hp} HP.")
        if target_index + 1 < len(targets) and targets[target_index + 1].is_alive():  # Target di kanan
            right_target = targets[target_index + 1]
            right_target.hp -= damage_aoe
            print(f"{right_target.nama} terkena serangan area dan menerima {damage_aoe} damage!")
            print(f"{right_target.nama} tersisa {right_target.hp} HP.")

    def Ultimate(self, targets):
        damage = int(self.atk * 2)  # Ultimate memberikan 200% dari attack ke semua target
        print(f"{self.nama} menggunakan Area Attack!")
        for target in targets:  # Mengiterasi daftar target
            if target.is_alive():
                target.hp -= damage
                print(f"{target.nama} terkena serangan area dan menerima {damage} damage!")
                print(f"{target.nama} tersisa {target.hp} HP.")
        
class Healer(karakter):
    def BasicAttack(self, target):
        damage = int(self.atk * 0.9) # Basic Attack memberikan 90% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Basic Attack pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")
        
    def Skill(self, target):
        heal_amount = int(self.hp * 0.7)  # Skill memberikan 70% dari hp sebagai heal
        if target.hp + heal_amount > target.MXhp:
            heal_amount = target.MXhp - target.hp  # Pastikan tidak melebihi MXhp
        target.hp += heal_amount
        print(f"{self.nama} menyembuhkan {target.nama} sebesar {heal_amount} HP!")
        print(f"{target.nama} sekarang memiliki {target.hp} HP.")
        
    def Ultimate(self, party):
        heal_amount = int(self.hp * 0.5)  # Ultimate memberikan 50% dari hp sebagai heal
        print(f"{self.nama} menggunakan Area Heal!")
        for member in party:
            if member.is_alive():
                if member.hp + heal_amount > member.MXhp:
                    heal_amount = member.MXhp - member.hp  # Pastikan tidak melebihi Maxhp
                member.hp += heal_amount
                print(f"{member.nama} disembuhkan sebesar {heal_amount} HP!")
                print(f"{member.nama} sekarang memiliki {member.hp} HP.")
    
#Monster
class Monster(karakter):
    def BasicAttack(self, target):
        damage = int(self.atk * 0.9)  # Basic Attack memberikan 90% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Basic Attack pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")
        
    def Skill(self, target):
        damage = int(self.atk * 1.2) # Skill memberikan 120% dari attack
        target.hp -= damage
        print(f"{self.nama} menggunakan Skill pada {target.nama} dan memberikan {damage} damage!")
        print(f"{target.nama} tersisa {target.hp} HP.")


def display_stats(party, monsters):
    print("\n=== Status Party ===")
    time.sleep(1)  # Jeda 1 detik
    for member in party:
        print(f"{member.nama} - HP: {member.hp}/{member.MXhp}, ATK: {member.atk}, SPD: {member.spd}")
        time.sleep(1)  # Jeda 1 detik
    
    print("\n=== Status Monster ===")
    for monster in monsters:
        print(f"{monster.nama} - HP: {monster.hp}/{monster.MXhp}, ATK: {monster.atk}, SPD: {monster.spd}")
        time.sleep(1)  # Jeda 1 detik


# Sistem Giliran Berdasarkan Speed
def turn_order(party, monsters):
    # Gabungkan party dan monster, lalu urutkan berdasarkan speed (spd) secara menurun
    return sorted(party + monsters, key=lambda x: x.spd, reverse=True)

# Membuat Party dan Monster

# Membuat Stage
stage_1 = [
    Monster("Monster1", 250, 20, 12),
    Monster("Monster2", 250, 20, 14)
]

stage_2 = [
    Monster("Monster3", 300, 15, 9),
    Monster("Monster4", 300, 18, 6)
]

stage_3 = [
    Monster("Monster5", 600, 20, 18),
    Monster("Monster6", 250, 25, 8)
]

# Daftar stage
stages = [stage_1, stage_2, stage_3]

# Membuat Party
party = [
    Slayer("Slayer", 100, 40, 10),  # Slayer dengan speed 10
    Mage("Mage", 90, 45, 9),       # Mage dengan speed 9
    Healer("Healer", 110, 21, 8)     # Healer dengan speed 14
]



# Urutkan giliran berdasarkan speed
turns = turn_order(party, stages[0])  # Menggunakan stage pertama untuk pertarungan

