курсовая игра на движке godot engine 4.5.1 
эта игра вдохновлена серией игр five night`s at freddy`s 
в ней так же будет механики камер, интелект аниматроника и свои механики, которые я собираюсь внедрить
насчёт названия надо будет по работать
ИИ противника будет состоять на проверке и генерации случайных чисел

код аниматроника
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

КОД ДЛЯ СИСТЕМЫ КАМЕР

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
extends CanvasLayer

#@onready var scheme = $Scheme
#@onready var camera_office = get_parent().get_node("camera_system/office1")
#@onready var map = get_parent().get_node("camera_system/office1")
#@onready var camera1 = get_parent().get_node("camera_system/Camera1")
#@onready var camera2 = get_parent().get_node("camera_system/Camera2_1")
#@onready var camera3 = get_parent().get_node("camera_system/Camera2_2")
#@onready var camera4 = get_parent().get_node("camera_system/Camera3")
#@onready var camera5 = get_parent().get_node("camera_system/Camera4_1")
#@onready var camera6 = get_parent().get_node("camera_system/Camera4_2")
#@onready var camera7 = get_parent().get_node("camera_system/Camera4_3")
#@onready var camera8 = get_parent().get_node("camera_system/Camera4_4")
#@onready var camera9 = get_parent().get_node("camera_system/Camera5")
#@onready var camera10 = get_parent().get_node("camera_system/Camera6_1")
#@onready var camera11 = get_parent().get_node("camera_system/Camera7")
#@onready var camera12 = get_parent().get_node("camera_system/Camera8")
#@onready var camera13 = get_parent().get_node("camera_system/Camera9_1")
#@onready var camera14 = get_parent().get_node("camera_system/Camera9_2")
#@onready var camera15 = get_parent().get_node("camera_system/Camera10")
#@onready var camera16 = get_parent().get_node("camera_system/Camera11")
#@onready var camera17 = get_parent().get_node("camera_system/Camera12_1")
#@onready var world = get_parent().get_node("camera_system/world")

#НОВЫЙ ОНРЕДИ КАМЕР
@onready var cam_off = get_parent().get_node("camera_system/office1")
@onready var map = get_parent().get_node("camera_system/world")
@onready var cam1 = get_parent().get_node("camera_system/Camera1")
@onready var cam5 = get_parent().get_node("camera_system/Camera5")
@onready var cam8 = get_parent().get_node("camera_system/Camera8")
@onready var cam11 = get_parent().get_node("camera_system/Camera11")
@onready var cam2_1 = get_parent().get_node("camera_system/Camera2_1")
@onready var cam2_2 = get_parent().get_node("camera_system/Camera2_2")
@onready var cam6_1 = get_parent().get_node("camera_system/Camera6_1")
@onready var cam6_2 = get_parent().get_node("camera_system/Camera6_2")
@onready var cam9_1 = get_parent().get_node("camera_system/Camera9_1")
@onready var cam9_2 = get_parent().get_node("camera_system/Camera9_2")
@onready var cam12_1 = get_parent().get_node("camera_system/Camera12_1")
@onready var cam12_2 = get_parent().get_node("camera_system/Camera12_2")
@onready var cam4_1 = get_parent().get_node("camera_system/Camera4_1")
@onready var cam4_2 = get_parent().get_node("camera_system/Camera4_2")
@onready var cam4_3 = get_parent().get_node("camera_system/Camera4_3")
@onready var cam4_4 = get_parent().get_node("camera_system/Camera4_4")
@onready var cam3 = get_parent().get_node("camera_system/Camera3")
@onready var cam7 = get_parent().get_node("camera_system/Camera7")
@onready var cam10 = get_parent().get_node("camera_system/Camera10")
@onready var cam13 = get_parent().get_node("camera_system/Camera13")
@onready var camA = get_parent().get_node("camera_system/CameraA")
@onready var camB = get_parent().get_node("camera_system/CameraB")
@onready var camC = get_parent().get_node("camera_system/CameraC")
@onready var camD = get_parent().get_node("camera_system/CameraD")

@onready var animatronic = get_parent().get_node("enemey")
@onready var battery_label = $charge 
@onready var txt_cam = $curcam
 
var cameras = []
var camera_names = ["camera1", "camera2.1", "camera2.2", "camera3", "cameraA", "camera5", "camera6.1", "camera6.2", "camera7", "cameraB", "camera8", "camera9.1", "camera9.2", "camera10", "cameraC", "camera11", "camera12.1", "camera12.2", "camera13", "cameraD", "camera4.1", "camera4.2", "camera4.3", "camera4.4"]

var flashlight_battery = 100.0  # Заряд батареи (0-100)
var flashlight_drain = 100.0     # Сколько тратится за использование
var flashlight_recharge = 5   # Восстановление за секунду
var flashlight_cooldown = 0   # Время до следующего использования
var max_cooldown = 10          # Максимальный cooldown в секундах

var tween: Tween #для анимации перехода в офисе
var map_status = 0 #для анимации перехода в офисе

var now_cam = "office" #для вспышки штучка

func _ready():
	cameras = [cam1, cam2_1, cam2_2, cam3, camA, cam5, cam6_1, cam6_2, cam7, camB, cam8, cam9_1, cam9_2, cam10, camC, cam11, cam12_1, cam12_2, cam13, camD, cam4_1, cam4_2, cam4_3, cam4_4]
	$next_cam.visible = false
	$back_cam.visible = false
	$flash.visible = false
	if cam_off == null:
		print("Ошибка: CameraOffice не найден!")
		return
	cam_off.make_current()

	if animatronic == null:
		print("Ошибка: Animatronic не найден!")
		return
	if battery_label:
		battery_label.text = "Battery: " + str(int(flashlight_battery)) + "%"


func _process(delta: float) -> void:
	if flashlight_battery < 100.0:
		flashlight_battery += flashlight_recharge * delta
		flashlight_battery = min(flashlight_battery, 100.0)
	if flashlight_cooldown > 0.0:
		flashlight_cooldown -= delta

	if battery_label:
		battery_label.text = "Battery: " + str(int(flashlight_battery)) + "%"


func _on_flash_pressed() -> void:
	if now_cam == "office" or now_cam == "cameraA" or now_cam == "cameraB" or now_cam == "cameraB" or now_cam == "cameraD":
		return
	elif flashlight_cooldown <= 0.0 and flashlight_battery >= flashlight_drain:
		flashlight_battery -= flashlight_drain
		flashlight_cooldown = max_cooldown
		animatronic.flash_reset()  # Вызываем сброс
		#print("Вспышка активирована! Заряд: ", flashlight_battery)
	else:
		print("Вспышка не готова! Заряд: ", flashlight_battery, ", Cooldown: ", flashlight_cooldown)

func _on_map_mouse_entered() -> void:
	cam_anim()
func _on_map_pressed() -> void:
	cam_anim()
	
func cam_anim() -> void:
	if map_status == 0:
		if tween and tween.is_running():
			#tween.kill()
			return #посмотрим, может не буду прерывать анимацию
		tween = create_tween()
		map_status = 1
		#параметры передвижения камеры
		tween.tween_property(cam_off, "position:x", cam_off.position.x + 1283, 1.0).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	elif map_status == 1:
		if tween and tween.is_running():
			#tween.kill()
			return #посмотрим, может не буду прерывать анимацию
		tween = create_tween()
		map_status = 0
		#параметры передвижения камеры
		tween.tween_property(cam_off, "position:x", cam_off.position.x - 1280, 1).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)

func _on_next_cam_pressed() -> void:

	var current_index = camera_names.find(now_cam)
	if current_index != -1:
		var next_index = (current_index + 1) % camera_names.size()
		# Если зациклились на "office", переходим к первой камере (cam1)
		if camera_names[next_index] == "office":
			next_index = 1  # Индекс cam1

		var next_cam = cameras[next_index]
		next_cam.make_current()
		animatronic.update_camera(camera_names[next_index])
		now_cam = camera_names[next_index]
		$map.visible = false
		txt_cam.text = camera_names[next_index] if camera_names[next_index] != "office" else ""

func _on_back_cam_pressed() -> void:

	var current_index = camera_names.find(now_cam)
	if current_index != -1:
		var next_index = (current_index - 1) % camera_names.size()
		# Если зациклились на "office", переходим к первой камере (cam1)
		if camera_names[next_index] == "office":
			next_index = 1  # Индекс cam1

		var next_cam = cameras[next_index]
		next_cam.make_current()
		animatronic.update_camera(camera_names[next_index])
		now_cam = camera_names[next_index]
		$map.visible = false
		txt_cam.text = camera_names[next_index] if camera_names[next_index] != "office" else ""
		
#////////////////////////////////////////////////////////////////////////////////////////////////////
#ВСЕ ЭТИ ФУНКЦИИ СКОРО ПОД СНОС!!!!!!!!
#////////////////////////////////////////////////////////////////////////////////////////////////////

#func _on_button_city_1_pressed() -> void:
	#cam1.make_current()
	#animatronic.update_camera("camera1")  # Передаём строку
	#now_cam = "camera1"
	#$map.visible = false
	#txt_cam.text = "cam1"
	#
#
#func _on_button_city_2_pressed() -> void:
	#cam2.make_current()
	#animatronic.update_camera("camera2")
	#now_cam = "camera2"
	#$map.visible = false
	#txt_cam.text = "cam2"
#
#func _on_button_city_3_pressed() -> void:
	#cam3.make_current()
	#animatronic.update_camera("camera3")
	#now_cam = "camera3"
	#$map.visible = false
	#txt_cam.text = "cam3"
#
#func _on_button_city_4_pressed() -> void:
	#cam4.make_current()
	#animatronic.update_camera("camera4")
	#now_cam = "camera4"
	#$map.visible = false
	#txt_cam.text = "cam4"
#
#func _on_button_city_5_pressed() -> void:
	#cam5.make_current()
	#animatronic.update_camera("camera5")
	#now_cam = "camera5"
	#$map.visible = false
	#txt_cam.text = "cam5"
#
#func _on_button_city_6_pressed() -> void:
	#camera6.make_current()
	#animatronic.update_camera("camera6")
	#now_cam = "camera6"
	#$map.visible = false
	#txt_cam.text = "cam6"
#
#func _on_button_city_7_pressed() -> void:
	#camera7.make_current()
	#animatronic.update_camera("camera7")
	#now_cam = "camera7"
	#$map.visible = false
	#txt_cam.text = "cam7"
	#
#func _on_button_city_8_pressed() -> void:
	#camera8.make_current()
	#animatronic.update_camera("camera8")
	#now_cam = "camera8"
	#$map.visible = false
	#txt_cam.text = "cam8"
#
#func _on_button_city_9_pressed() -> void:
	#camera9.make_current()
	#animatronic.update_camera("camera9")
	#now_cam = "camera9"
	#$map.visible = false
	#txt_cam.text = "cam9"
#
#func _on_button_city_10_pressed() -> void:
	#camera10.make_current()
	#animatronic.update_camera("camera10")
	#now_cam = "camera10"
	#$map.visible = false
	#txt_cam.text = "cam10"
#
#func _on_button_city_11_pressed() -> void:
	#camera11.make_current()
	#animatronic.update_camera("camera11")
	#now_cam = "camera11"
	#$map.visible = false
	#txt_cam.text = "cam11"
#
#func _on_button_city_12_pressed() -> void:
	#camera12.make_current()
	#animatronic.update_camera("camera12")
	#now_cam = "camera12"
	#$map.visible = false
	#txt_cam.text = "cam12"
#
#func _on_button_city_13_pressed() -> void:
	#camera13.make_current()
	#animatronic.update_camera("camera13")
	#now_cam = "camera13"
	#$map.visible = false
	#txt_cam.text = "cam13"
#
#func _on_button_city_14_pressed() -> void:
	#camera14.make_current()
	#animatronic.update_camera("camera14")
	#now_cam = "camera14"
	#$map.visible = false
	#txt_cam.text = "cam14"
#
#func _on_button_city_15_pressed() -> void:
	#camera15.make_current()
	#animatronic.update_camera("camera15")
	#now_cam = "camera15"
	#$map.visible = false
	#txt_cam.text = "cam15"
#
#func _on_button_city_16_pressed() -> void:
	#camera16.make_current()
	#animatronic.update_camera("camera16")
	#now_cam = "camera16"
	#$map.visible = false
	#txt_cam.text = "cam16"
#
#func _on_button_city_17_pressed() -> void:
	#camera17.make_current()
	#animatronic.update_camera("camera17")
	#now_cam = "camera17"
	#$map.visible = false
	#txt_cam.text = "cam17"
	#
#func _on_button_city_18_pressed() -> void:
	#camera18.make_current()
	#animatronic.update_camera("camera18")
##	print("camera10")

func _on_comp_down_mouse_entered() -> void:
	cam_off.make_current()
	animatronic.update_camera("office")  # Для офиса
	now_cam = "office"
	$map.visible = true
	txt_cam.text = ""
	$next_cam.visible = false
	$back_cam.visible = false

func _on_world_pressed() -> void:
	map.make_current()
	$next_cam.visible = false
	$back_cam.visible = false
	
#////////////////////////////
#НОВЫЕ КАМЕРЫ
#////////////////////////////

func _on_btn_1_pressed() -> void:
	cam1.make_current()
	animatronic.update_camera("camera1")
	now_cam = "camera1"
	$map.visible = false
	txt_cam.text = "cam1"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_5_pressed() -> void:
	cam5.make_current()
	animatronic.update_camera("camera5")
	now_cam = "camera5"
	$map.visible = false
	txt_cam.text = "cam5"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_8_pressed() -> void:
	cam8.make_current()
	animatronic.update_camera("camera8")
	now_cam = "camera8"
	$map.visible = false
	txt_cam.text = "cam8"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_11_pressed() -> void:
	cam11.make_current()
	animatronic.update_camera("camera11")
	now_cam = "camera11"
	$map.visible = false
	txt_cam.text = "cam11"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_2_1_pressed() -> void:
	cam2_1.make_current()
	animatronic.update_camera("camera2.1")
	now_cam = "camera2.1"
	$map.visible = false
	txt_cam.text = "cam2.1"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_2_2_pressed() -> void:
	cam2_2.make_current()
	animatronic.update_camera("camera2.2")
	now_cam = "camera2.2"
	$map.visible = false
	txt_cam.text = "cam2.2"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_6_1_pressed() -> void:
	cam6_1.make_current()
	animatronic.update_camera("camera6.1")
	now_cam = "camera6.1"
	$map.visible = false
	txt_cam.text = "cam6.1"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_6_2_pressed() -> void:
	cam6_2.make_current()
	animatronic.update_camera("camera6.2")
	now_cam = "camera6.2"
	$map.visible = false
	txt_cam.text = "cam6.2" 
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_9_1_pressed() -> void:
	cam9_1.make_current()
	animatronic.update_camera("camera9.1")
	now_cam = "camera9.1"
	$map.visible = false
	txt_cam.text = "cam9.1"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_9_2_pressed() -> void:
	cam9_2.make_current()
	animatronic.update_camera("camera9.2")
	now_cam = "camera9.2"
	$map.visible = false
	txt_cam.text = "cam9.2"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_12_1_pressed() -> void:
	cam12_1.make_current()
	animatronic.update_camera("camera12.1")
	now_cam = "camera12.1"
	$map.visible = false
	txt_cam.text = "cam12.1"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_12_2_pressed() -> void:
	cam12_2.make_current()
	animatronic.update_camera("camera12.2")
	now_cam = "camera12.2"
	$map.visible = false
	txt_cam.text = "cam12.2"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_3_pressed() -> void:
	cam3.make_current()
	animatronic.update_camera("camera3")
	now_cam = "camera3"
	$map.visible = false
	txt_cam.text = "cam3"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_7_pressed() -> void:
	cam7.make_current()
	animatronic.update_camera("camera7")
	now_cam = "camera7"
	$map.visible = false
	txt_cam.text = "cam7"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_10_pressed() -> void:
	cam10.make_current()
	animatronic.update_camera("camera10")
	now_cam = "camera10"
	$map.visible = false
	txt_cam.text = "cam10"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_13_pressed() -> void:
	cam13.make_current()
	animatronic.update_camera("camera13")
	now_cam = "camera13"
	$map.visible = false
	txt_cam.text = "cam13"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_a_pressed() -> void:
	camA.make_current()
	animatronic.update_camera("cameraA")
	now_cam = "cameraA"
	$map.visible = false
	txt_cam.text = "camA"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = false

func _on_btn_b_pressed() -> void:
	camB.make_current()
	animatronic.update_camera("cameraB")
	now_cam = "cameraB"
	$map.visible = false
	txt_cam.text = "camB"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = false

func _on_btn_c_pressed() -> void:
	camC.make_current()
	animatronic.update_camera("cameraC")
	now_cam = "cameraC"
	$map.visible = false
	txt_cam.text = "camC"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = false

func _on_btn_d_pressed() -> void:
	camD.make_current()
	animatronic.update_camera("cameraD")
	now_cam = "cameraD"
	$map.visible = false
	txt_cam.text = "camD"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = false

func _on_btn_office_pressed() -> void:
	cam_off.make_current()
	animatronic.update_camera("camera_office")
	now_cam = "camera_office"
	$map.visible = false
	txt_cam.text = ""

func _on_btn_4_1_pressed() -> void:
	cam4_1.make_current()
	animatronic.update_camera("camera4.1")
	now_cam = "camera4.1"
	$map.visible = false
	txt_cam.text = "cam4.1"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true


func _on_btn_4_2_pressed() -> void:
	cam4_2.make_current()
	animatronic.update_camera("camera4.2")
	now_cam = "camera4.2"
	$map.visible = false
	txt_cam.text = "cam4.2" 
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_4_3_pressed() -> void:
	cam4_3.make_current()
	animatronic.update_camera("camera4.3")
	now_cam = "camera4.3"
	$map.visible = false
	txt_cam.text = "cam4.3"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true

func _on_btn_4_4_pressed() -> void:
	cam4_4.make_current()
	animatronic.update_camera("camera4.4")
	now_cam = "camera4.4"
	$map.visible = false
	txt_cam.text = "cam4.4"
	$next_cam.visible = true
	$back_cam.visible = true
	$flash.visible = true



#extends CanvasLayer
#
##@onready var scheme = $Scheme  # Схема (если нужно скрывать/показывать)
#@onready var camera_office = get_parent().get_node("camera_system/office1")
#@onready var camera1 = get_parent().get_node("camera_system/Camera1")
#@onready var camera2 = get_parent().get_node("camera_system/Camera2")
#@onready var camera3 = get_parent().get_node("camera_system/Camera3")
#@onready var camera4 = get_parent().get_node("camera_system/Camera4")
#@onready var camera5 = get_parent().get_node("camera_system/Camera5")
#@onready var camera6 = get_parent().get_node("camera_system/Camera6")
#@onready var camera7 = get_parent().get_node("camera_system/Camera7")
#@onready var world = get_parent().get_node("camera_system/world")
## Добавьте остальные камеры: camera3, camera4 и т.д.
#
#@onready var animatronic = get_parent().get_node("enemey")  # Замените на правильный путь к узлу аниматроника
#
## Переменные для вспышки
#var flashlight_battery = 100.0  # Заряд батареи (0-100)
#var flashlight_drain = 100.0     # Сколько тратится за использование
#var flashlight_recharge = 10   # Восстановление за секунду
#var flashlight_cooldown = 0   # Время до следующего использования
#var max_cooldown = 10          # Максимальный cooldown в секундах
#
#func _ready():
	#if camera_office == null:
		#print("Ошибка: CameraOffice не найден!")
		#return
	#camera_office.make_current()
	## Проверка на аниматроника
	#if animatronic == null:
		#print("Ошибка: Animatronic не найден!")
		#return
#func _process(delta: float) -> void:
	## Восстановление батареи и cooldown
	#if flashlight_battery < 100.0:
		#flashlight_battery += flashlight_recharge * delta
		#flashlight_battery = min(flashlight_battery, 100.0)
	#if flashlight_cooldown > 0.0:
		#flashlight_cooldown -= delta
#
## Функция для активации вспышки (вызывайте по сигналу кнопки)
#func _on_flash_pressed() -> void:
	#if flashlight_cooldown <= 0.0 and flashlight_battery >= flashlight_drain:
		#flashlight_battery -= flashlight_drain
		#flashlight_cooldown = max_cooldown
		#animatronic.flash_reset()  # Вызываем сброс аниматроника
		#print("Вспышка активирована! Заряд: ", flashlight_battery)
	#else:
		#print("Вспышка не готова! Заряд: ", flashlight_battery, ", Cooldown: ", flashlight_cooldown)
#func _on_button_city_1_pressed() -> void:
	#camera1.make_current()
#func _on_button_city_2_pressed() -> void:
	#camera2.make_current()
#func _on_button_city_3_pressed() -> void:
	#camera3.make_current()
#func _on_button_city_4_pressed() -> void:
	#camera4.make_current()
#func _on_button_city_5_pressed() -> void:
	#camera5.make_current()
#func _on_button_city_6_pressed() -> void:
	#camera6.make_current()
#func _on_button_city_7_pressed() -> void:
	#camera7.make_current()
#func _on_comp_down_mouse_entered() -> void:
	#camera_office.make_current()
#func _on_world_pressed() -> void:
	#world.make_current()

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

И ДЛЯ НОЧИ ЕСТЬ СВОЙ СКРИПТ


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

extends Node2D

@onready var hour = $hour
@onready var label_hours = $CanvasLayer/hours 
var AM = 0

func _ready() -> void:
	hour.start()
	label_hours.text = str(int(AM)) + "AM"
	
	

func _process(_delta: float) -> void:
	label_hours.text = str(int(AM)) + "AM"
	
func _on_hour_timeout() -> void:
	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	if AM < 5:
		AM += 1
	else:
		AM = 6
		victory()
func victory():
	get_tree().change_scene_to_file("res://victory.tscn")


func _on_map_mouse_entered() -> void:
	pass # Replace with function body.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
