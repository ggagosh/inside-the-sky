## Headless test runner: `mise run test`.
## Runs every `test_*` method in `res://tests/test_*.gd`. A test fails if a check fails
## or if it raises a script error. Exits with code 1 on any failure.
# ponytail: ~50-line runner, no addon. Move to GUT or gdUnit4 if we need mocks, fixtures or reports.
extends SceneTree


class ErrorCounter:
	extends Logger
	var count := 0

	func _log_error(
		_function: String,
		_file: String,
		_line: int,
		_code: String,
		_rationale: String,
		_editor_notify: bool,
		_error_type: int,
		_script_backtraces: Array[ScriptBacktrace]
	) -> void:
		count += 1


func _initialize() -> void:
	var errors := ErrorCounter.new()
	OS.add_logger(errors)
	var passed := 0
	var failed := 0
	for file in DirAccess.get_files_at("res://tests"):
		if not (file.begins_with("test_") and file.ends_with(".gd")) or file == "test_case.gd":
			continue
		var script: GDScript = load("res://tests/" + file)
		for method in script.get_script_method_list():
			var test_name: String = method.name
			if not test_name.begins_with("test_"):
				continue
			var test: RefCounted = script.new()
			var errors_before := errors.count
			test.call(test_name)
			var problems: PackedStringArray = test.failures
			if errors.count > errors_before:
				problems.append(
					"raised %d script error(s), see log above" % (errors.count - errors_before)
				)
			if problems.is_empty():
				passed += 1
				print("  ok    %s :: %s" % [file, test_name])
			else:
				failed += 1
				print("  FAIL  %s :: %s" % [file, test_name])
				for problem in problems:
					print("        - " + problem)
	print("\n%d passed, %d failed" % [passed, failed])
	quit(1 if failed > 0 or passed == 0 else 0)
