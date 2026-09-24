import random

class Wave:
    enemy_type = 0
    number_of_enemies = 0
    time_between_enemies = 0
    start_x = 0
    start_y = 0
    speed_x = 0
    speed_y = 0
    health = 0
    number_of_bullets = 0
    movement_type = ""
    burst_enemy_number = 0

waves = []

wave_1 = Wave() #normal weak one
wave_1.enemy_type = 0
wave_1.number_of_enemies = 6
wave_1.time_between_enemies = 4
wave_1.start_x = 0
wave_1.start_y = 0
wave_1.speed_x = 2
wave_1.speed_y = 2
wave_1.health = 1
wave_1.number_of_bullets = 3
wave_1.movement_type = "Bounce"
wave_1.burst_enemy_number = 1


waves.append(wave_1)

wave_2 = Wave() #fast but normal health
wave_2.enemy_type = 1
wave_2.number_of_enemies = 6
wave_2.time_between_enemies = 4
wave_2.start_x = 450
wave_2.start_y = 0
wave_2.speed_x = 4
wave_2.speed_y = 3
wave_2.health = 1
wave_2.number_of_bullets = 2
wave_2.movement_type = "Bounce"
wave_2.burst_enemy_number = 1

waves.append(wave_2)

wave_3 = Wave() #high health but slow
wave_3.enemy_type = 2
wave_3.number_of_enemies = 6
wave_3.time_between_enemies = 6
wave_3.start_x = 225
wave_3.start_y = 0
wave_3.speed_x = 3
wave_3.speed_y = 1.75
wave_3.health = 2
wave_3.number_of_bullets = 2
wave_3.movement_type = "Random"
wave_3.burst_enemy_number = 1

waves.append(wave_3)

wave_4 = Wave() #divebomb
wave_4.enemy_type = 3
wave_4.number_of_enemies = 6
wave_4.time_between_enemies = 4
wave_4.start_x = 225
wave_4.start_y = 100
wave_4.speed_x = 4
wave_4.speed_y = 2
wave_4.health = 1
wave_4.number_of_bullets = 2
wave_4.movement_type = "Divebomb"
wave_4.burst_enemy_number = 1

waves.append(wave_4)

wave_5 = Wave() #miniboss
wave_5.enemy_type = 4
wave_5.number_of_enemies = 1
wave_5.time_between_enemies = 2
wave_5.start_x = 0
wave_5.start_y = 100
wave_5.speed_x = 1
wave_5.speed_y = 1
wave_5.health = 10
wave_5.number_of_bullets = 2
wave_5.movement_type = "Random"
wave_5.burst_enemy_number = 1

waves.append(wave_5)

wave_6 = Wave() #small and spawn in groups of 3 (5 times)
wave_6.enemy_type = 6
wave_6.number_of_enemies = 9
wave_6.time_between_enemies = 1
wave_6.start_x = 225
wave_6.start_y = 100
wave_6.speed_x = 1
wave_6.speed_y = 1
wave_6.health = 1
wave_6.number_of_bullets = 4
wave_6.movement_type = "Random"
wave_6.burst_enemy_number = 3


waves.append(wave_6)

wave_7 = Wave() #high health and lots of bullets
wave_7.enemy_type = 6
wave_7.number_of_enemies = 10
wave_7.time_between_enemies = 4
wave_7.start_x = 0
wave_7.start_y = 100
wave_7.speed_x = 1.5
wave_7.speed_y = 1
wave_7.health = 2
wave_7.number_of_bullets = 4
wave_7.movement_type = "Random"
wave_7.burst_enemy_number = 1

waves.append(wave_7)

wave_8 = Wave() #go side to side very fast so hard to shoot
wave_8.enemy_type = 7
wave_8.number_of_enemies = 10
wave_8.time_between_enemies = 5
wave_8.start_x = 0
wave_8.start_y = 100
wave_8.speed_x = 4
wave_8.speed_y = 1
wave_8.health = 1
wave_8.number_of_bullets = 4
wave_8.movement_type = "ZigZag"
wave_8.burst_enemy_number = 1

waves.append(wave_8)

wave_9 = Wave() #a lot of small ones, lot of bullets
wave_9.enemy_type = 8
wave_9.number_of_enemies = 25
wave_9.time_between_enemies = 2
wave_9.start_x = 0
wave_9.start_y = 100
wave_9.speed_x = 1.5
wave_9.speed_y = 1
wave_9.health = 1
wave_9.number_of_bullets = 6
wave_9.movement_type = "Orbit" 
wave_9.burst_enemy_number = 1

waves.append(wave_9)

wave_10 = Wave() #boss
wave_10.enemy_type = 9
wave_10.number_of_enemies = 1
wave_10.time_between_enemies = 2
wave_10.start_x = 0
wave_10.start_y = 100
wave_10.speed_x = 1.5
wave_10.speed_y = 1
wave_10.health = 25
wave_10.number_of_bullets = 10
wave_10.movement_type = "Bounce"
wave_10.burst_enemy_number = 1

waves.append(wave_10)
