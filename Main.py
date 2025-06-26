from ursina import *
from random import randint, choice

app = Ursina()

window.title = 'Mini Sandbox 3D'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Terreno
ground = Entity(model='plane', scale=(50,1,50), texture='shore', texture_scale=(25,25), collider='box')

# Edificios simples
for i in range(20):
    x = randint(-20,20)
    z = randint(-20,20)
    h = randint(2,8)
    b = Entity(model='cube', color=color.gray, position=(x,h/2,z), scale=(3,h,3), collider='box')

# Vehículos (cubos móviles)
cars = []
for i in range(5):
    x = randint(-15,15)
    z = randint(-15,15)
    car = Entity(model='cube', color=color.azure, position=(x,0.5,z), scale=(2,0.5,1), collider='box')
    car.speed = randint(1,3) * choice([1,-1])
    cars.append(car)

# Personaje principal
player = FirstPersonController(model='cube', color=color.orange, speed=8, jump_height=2, position=(0,2,0))

# NPCs
npcs = []
for i in range(8):
    x = randint(-22,22)
    z = randint(-22,22)
    npc = Entity(model='cube', color=color.random_color(), position=(x,1,z), scale=(1,2,1), collider='box')
    npc.direction = choice([Vec3(1,0,0), Vec3(-1,0,0), Vec3(0,0,1), Vec3(0,0,-1)])
    npcs.append(npc)

# HUD
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2, background=True)

def update():
    global score
    # Mueve autos
    for car in cars:
        car.x += time.dt * car.speed
        if abs(car.x) > 23:
            car.speed *= -1
        # Colisión con player
        if car.intersects(player).hit:
            player.position = (0,2,0)
            score = max(0, score-10)
            score_text.text = f'Score: {score}'
    # NPC movimiento básico
    for npc in npcs:
        npc.position += npc.direction * time.dt
        if abs(npc.x) > 23 or abs(npc.z) > 23:
            npc.direction *= -1
        # Colisión con player (saluda para sumar puntos)
        if distance(npc.position, player.position) < 2:
            score += 1
            score_text.text = f'Score: {score}'
            npc.position = (randint(-22,22),1,randint(-22,22))

    # Cambiar color ambiente según score
    if score > 20:
        scene.ambient_color = color.rgb(255, 200, 200)
    else:
        scene.ambient_color = color.rgb(200, 255, 255)

    # Si el jugador cae del mapa, reaparece
    if player.y < -10:
        player.position = (0,2,0)
        score = max(0, score-5)
        score_text.text = f'Score: {score}'

def input(key):
    # Simula "robar un auto": súbete encima y muévelo con el jugador
    if key == 'e':
        for car in cars:
            if distance(player.position, car.position) < 2:
                player.position = car.position + Vec3(0,2,0)
                car.color = color.red

app.run()
