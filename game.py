from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# --- ŚWIAT ---
Ground(scale=(200, 1, 200), color=color.green, collider='box')
Sky()
EditorCamera() # Opcjonalne: pozwala na podgląd sceny
AmbientLight(color=color.rgba(100, 100, 100, 255)) # Dodajemy trochę światła

# --- DESZCZ ---
class Deszcz(Entity):
    def __init__(self, intensity=0.5):
        super().__init__()
        self.intensity = intensity
        self.drops = []
        
        for i in range(150):  # Liczba kropel deszczu
            drop = Entity(
                model='sphere',
                scale=(0.05, 0.3, 0.05),
                color=color.light_gray,
                position=(
                    random.uniform(-100, 100),
                    random.uniform(5, 15),
                    random.uniform(-100, 100)
                )
            )
            self.drops.append(drop)
    
    def update(self):
        for drop in self.drops:
            # Deszcz pada w dół
            drop.y -= 0.3
            # Jak spadnie za nisko, teleportuj go do góry
            if drop.y < 0:
                drop.y = random.uniform(10, 15)
                drop.x = camera.x + random.uniform(-50, 50)
                drop.z = camera.z + random.uniform(-50, 50)

deszcz = Deszcz()

# --- KLASA LATARNI ---
class Latarnia(Entity):
    def __init__(self, pos, id_num):
        # Słup latarni
        super().__init__(model='cylinder', scale=(0.2, 4, 0.2), position=pos, color=color.black, collider='box')
        self.id = id_num
        self.czy_rozbita = False
        # Klosz - cel rzutu
        self.klosz = Entity(parent=self, model='sphere', y=1.1, scale=(2, 0.5, 2), color=color.white, collider='sphere')

    def trafienie(self):
        if not self.czy_rozbita:
            self.czy_rozbita = True
            # Tworzymy dziurę w latarni (zmniejszamy klosz i zmieniamy kolor)
            self.klosz.color = color.dark_gray
            self.klosz.scale = (1.8, 0.4, 1.8)  # Zmniejszenie rozmiaru
            print(f"BUM! Latarnia nr {self.id} oberwała! Jest dziura!")

# --- GENEROWANIE 36 LATARNI ---
latarnie = []
for i in range(36):
    x_pos = random.choice([-5, 5]) 
    latarnia = Latarnia(pos=(x_pos, 2, i * 10), id_num=i)
    latarnie.append(latarnia)

# --- MECHANIKA RZUTU ---
def input(key):
    if key == 'left mouse button':
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'parent'):
            if isinstance(mouse.hovered_entity.parent, Latarnia):
                mouse.hovered_entity.parent.trafienie()

player = FirstPersonController() 
app.run()
