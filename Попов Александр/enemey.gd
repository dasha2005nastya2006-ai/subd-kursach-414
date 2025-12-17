extends Node2D

@onready var silent = $roar1
@onready var norm = $roar3
@onready var loud = $roar5
@onready var close = $roar7


var movement_oprtunity = {
	"start": ["room1", "room5", "room8", "room11"], #место за городом 
	"room1": ["room2.1", "room2.2", "roomA",  "roomD", "room5", "room11", "room8"],#стартовые камеры
	"room5": ["room6.1", "room6.2", "roomA", "roomB", "room11", "room1", "room8"],#стартовые камеры
	"room8": ["room9.1", "room9.2", "roomC", "roomB", "room11", "room1", "room5"],#стартовые камеры
	"room11": ["room12.1", "room12.2", "roomC", "roomB", "room5", "room1", "room8"],#стартовые камеры
	
	"room4.1": ["office", "room4.2", "room4.4", "room3", "room13", "roomD"],#камеры около оффиса
	"room4.2": ["office", "room4.1", "room4.3", "room3", "room7", "roomA"],#камеры около оффиса
	"room4.3": ["office", "room4.2", "room4.4", "room7", "room10", "roomB"],#камеры около оффиса
	"room4.4": ["office", "room4.1", "room4.3", "room13", "room10", "roomC"],#камеры около оффиса
	
	"roomA": ["room1",  "room5"],#камеры в дерёвнях (В НИХ НЕТ ВСПЫШКИ)
	"roomB": ["room5",  "room8"],#камеры в дерёвнях (В НИХ НЕТ ВСПЫШКИ)
	"roomC": ["room8",  "room11"],#камеры в дерёвнях (В НИХ НЕТ ВСПЫШКИ)
	"roomD": ["room1",  "room11"],#камеры в дерёвнях (В НИХ НЕТ ВСПЫШКИ)
	
	"room2.1": ["room3", "room2.2", "room1", "roomD"],#места по краям города
	"room2.2": ["room3", "room2.1", "room1", "roomA"],#места по краям города
	
	"room6.1": ["room7", "room6.2", "room5", "roomA"],#места по краям города
	"room6.2": ["room7", "room6.1", "room5", "roomB"],#места по краям города
	
	"room9.1": ["room10", "room9.2", "room8", "roomB"],#места по краям города
	"room9.2": ["room10", "room9.1", "room8", "roomC"],#места по краям города
	
	"room12.1": ["room13", "room12.2", "room11", "roomD"],#места по краям города
	"room12.2": ["room13", "room12.1", "room11", "roomC"],#места по краям города
	
	"room3": ["room4.1", "room4.2", "room2.1", "room2.2"],
	"room7": ["room4.2", "room4.3", "room6.1", "room6.2"],
	"room10": ["room4.3", "room4.4", "room9.1", "room9.2"],
	"room13": ["room4.1", "room4.4", "room12.1", "room12.2"],
	
	"office": []
}
var positions = {
	"start": Vector2(9999, 9999),
	"office": Vector2(555, 383),
	"room1": Vector2(464, -547),
	"room3": Vector2(4246, -536),
	"room5": Vector2(4643, 202),
	"room7": Vector2(6509, -1685),
	"room8": Vector2(7165, -518),
	"room10": Vector2(5210, 2320),
	"room11": Vector2(-5926, 6065),
	"room13": Vector2(204, 4369),
	"room14": Vector2(5562, 285),
	"room2.1": Vector2(17109, -542),
	"room2.2": Vector2(2954, -538),
	"room6.1": Vector2(5558, 200),
	"room6.2": Vector2(4519, -1698),
	"room9.1": Vector2(7241, 603),
	"room9.2": Vector2(7248, 1735),
	"room12.1": Vector2(-3636, 4369),
	"room12.2": Vector2(-1716, 4369),
	"roomA": Vector2(2124, 4369),
	"roomB": Vector2(4044, 4369),
	"roomC": Vector2(5964, 4369),
	"roomD": Vector2(7885, 4369),
	"room4.1": Vector2(5542, -529),
	"room4.2": Vector2(3509, 821),
	"room4.3": Vector2(2904, 116),
	"room4.4": Vector2(3715, 175),
}

var current_room = "start"
var current_camera = "office"

# сопоставление камер и комнат
var camera_to_room = {
	"office": "office",
	"camera1": "room1",

	"camera2.1": "room2.1",
	"camera2.2": "room2.2",

	"camera3": "room3",

	"camera4.1": "room4.1",
	"camera4.2": "room4.2",
	"camera4.3": "room4.3",
	"camera4.4": "room4.4",

	"camera5": "room5",

	"camera6.1": "room6.1",
	"camera6.2": "room6.2",

	"camera7": "room7",
	"camera8": "room8",

	"camera9.1": "room9.1",
	"camera9.2": "room9.2",

	"camera10": "room10",
	"camera11": "room11",

	"camera12.1": "room12.1",
	"camera12.2": "room12.2",

	"camera13": "room13",

	"cameraA": "roomA",
	"cameraB": "roomB",
	"cameraC": "roomC",
	"cameraD": "roomD",
}

@onready var game = $Gameover
@onready var timer = $Timer

func _ready():
	position = positions[current_room]
	timer.start()

func _on_timer_timeout():
	# Получаем список возможных следующих комнат для текущей
	var possible_next = movement_oprtunity.get(current_room, [])
	#print(possible_next)
	if possible_next.size() > 0:
		var next_room
		if current_room == "start":
			var cam1 = possible_next[0]
			var cam5 = possible_next[1]
			var cam8 = possible_next[2]
			var cam11 = possible_next[3]
			var weighted_choices = [cam1, cam5, cam8, cam11]

			print(weighted_choices)
			next_room = weighted_choices[randi() % weighted_choices.size()]

		elif possible_next.size() == 2: # используется для деревень
			var cam1 = possible_next[0] #первая комната в масссиве 
			var cam2 = possible_next[1] #вторая комната

			var weighted_choices = [cam1, cam2] #50% на 50% 

			print(weighted_choices)
			next_room = weighted_choices[randi() % weighted_choices.size()]

		elif current_room == "room2.1" or current_room == "room2.1" or current_room == "room2.2" or current_room == "room6.1" or current_room == "room6.2" or current_room == "room9.1" or current_room == "room9.2" or current_room == "room12.1" or current_room == "room12.2":
			var forward_room = possible_next[0] #первая комната
			var middle_room = possible_next[1] #вторая комната
			var back_room = possible_next[2] #третья комната
			var village = possible_next[3] #жоский откат назад

			var weighted_choices = [forward_room, forward_room, middle_room, middle_room, back_room, village]

			print(weighted_choices)
			next_room = weighted_choices[randi() % weighted_choices.size()]

		elif current_room == "room4.1" or current_room == "room4.2" or current_room == "room4.3" or current_room == "room4.4":
			var office = possible_next[0] #оффис
			var one = possible_next[1] #соседняя 4.Х
			var two  = possible_next[2] #соседняя 4.Х
			var back1 = possible_next[3] # назад в микрорайон
			var back2 = possible_next[4] # назад в микрорайон
			var village = possible_next[5] # в деревню
			
			var weighted_choices = [village, back1, back1, back1, back2, back2, back2, two, two, two, two, two, one, one, one, one, one, office, office, office, office, office, office, office, office, office, office, office, office, office, office, office, office]
			
			print(weighted_choices)
			next_room = weighted_choices[randi() % weighted_choices.size()]
			
		elif possible_next.size() == 4: #используется для 3 7 10 13
			var four = possible_next[0] #первая комната
			var five = possible_next[1] #вторая комната
			var back = possible_next[2] #третья комната (центральная)
			var backswing = possible_next[3] #четвёртая комната

			var weighted_choices = [four, four, four, four, five, five, five, five, back, back, backswing, backswing]

			print(weighted_choices)
			next_room = weighted_choices[randi() % weighted_choices.size()]

		elif possible_next.size() == 7: #используется для центральной комнаты 1 5 8 11
			var forwrd = possible_next[0] #первая комната
			var move = possible_next[1] #вторая комната
			var village = possible_next[2] #третья комната
			var village1 = possible_next[3] #четвёртая комната
			var telefrag = possible_next[4] #пятая комната
			var teleporter = possible_next[5] #шестая комната
			var tlprt = possible_next[6]

			var weighted_choices = [forwrd, forwrd, forwrd, forwrd, move, move, move, move, village, village, village1, village1, telefrag,  teleporter, tlprt]#надо будет вычислить проценты передвижения
			print(weighted_choices)
			next_room = weighted_choices[randi() % weighted_choices.size()]
		else:
			# Если нет развилок
			next_room = possible_next[0]
		
		if current_room != current_camera:  # Это условие можно оставить или убрать, в зависимости от логики
			current_room = next_room
			position = positions[current_room]
		print("он в ", current_room)
		if current_room == "office":
			print("Аниматроник в офисе")
			game.visible = true
			get_tree().change_scene_to_file("res://gg.tscn")


func update_camera(new_camera: String):
	current_camera = new_camera

# сброс аниматроника при вспышке	## Проверяем, можно ли отпугнуть (например, если аниматроник в room1 или office)
func flash_reset():
	# комната, соответствующая текущей камере
	var camera_room = camera_to_room.get(current_camera, "")
	# Сброс, если аниматроник в той же комнате, что и камера
	if current_room == camera_room and current_room != "office":
		if current_room == "room1" or current_room == "room5" or current_room == "room8" or current_room == "room11":
			silent.play()
		elif current_room == "room2.1" or current_room == "room2.2" or current_room == "room6.1" or current_room == "room6.2" or current_room == "room9.1" or current_room == "room9.2" or current_room == "room12.1" or current_room == "room12.2":
			norm.play()
		elif current_room == "room3" or current_room == "room7" or current_room == "room10" or current_room == "room13":
			loud.play()
		elif current_room == "room4.1" or current_room == "room4.2" or current_room == "room4.3" or current_room == "room4.4":
			close.play()

		current_room = "start"
		position = positions[current_room]
		timer.stop()
		timer.start()
		print("успех вспышки")
	else:
		print("мимо!")





#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#РЕЗЕР (ОТКАТ НА ВЕРСИЮ ALPHA 1.5)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#extends Node2D
#
#var room_order = ["room7", "room6", "room5", "room4", "room3", "room2", "room1", "office"]
#var positions = {
	#"office": Vector2(555, 383),
	#"room1": Vector2(1929, -521),
	#"room2": Vector2(2695, -336),
	#"room3": Vector2(4266, -428),
	#"room4": Vector2(2088, 227),
	#"room5": Vector2(3096, 329),
	#"room6": Vector2(3998, 146),
	#"room7": Vector2(3379, 868)
#}
#
#var current_room = "room7"
#var current_camera = "office"
#
#@onready var game = $Gameover
#@onready var sprite = $Sprite2D
#@onready var timer = $Timer
#
#func _ready():
	#position = positions[current_room]
	#timer.wait_time = randf_range(8, 8)
	#timer.start()
	#timer.connect("timeout", Callable(self, "_on_timer_timeout"))
#
#func _on_timer_timeout():
	#var current_index = room_order.find(current_room)
	#if current_index < room_order.size() - 1:
		#var next_index = current_index + 1
		#var next_room = room_order[next_index]
		#if current_room != current_camera:
			#current_room = next_room
			#position = positions[current_room]
		#print("Аниматроник телепортировался в ", current_room)
		#if current_room == "office":
			#print("Аниматроник в офисе! Игра окончена.")
			#game.visible = true
	#timer.wait_time = randf_range(8, 8)
	#timer.start()
#
#func update_camera(new_camera: String):
	#current_camera = new_camera
	#if current_room == "office":
		#print("Аниматроник в офисе! Игра окончена.")
#
## функция для сброса аниматроника при вспышке
#func flash_reset():
	#current_room = "room7"
	#position = positions[current_room]
	#timer.stop()
	#timer.wait_time = randf_range(1, 1)  # Сброс таймера
	#timer.start()
	#print("Аниматроник отпугнут вспышкой и сброшен в room7!")
	#
#
#func flash_retreat():
	#var current_index = room_order.find(current_room)
	#var retreat_index = max(0, current_index - 2)  # Отойти на 2 комнаты назад, но не меньше 0
	#var retreat_room = room_order[retreat_index]
	#current_room = retreat_room
	#position = positions[current_room]
	#print("Аниматроник отступил в ", current_room)
	## Опционально: задержка перед следующим движением
	#timer.stop()
	#await get_tree().create_timer(5.0).timeout  # Задержка 5 секунд
	#timer.start()
	#
