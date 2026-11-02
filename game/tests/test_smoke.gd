extends "res://tests/test_case.gd"


func test_main_scene_loads() -> void:
	var path: String = ProjectSettings.get_setting("application/run/main_scene")
	var scene := load(path) as PackedScene
	check(scene != null, "main scene %s should load" % path)
	if scene:
		var root := scene.instantiate()
		check_eq(root.name, &"Main", "main scene root name:")
		root.free()
