## Base class for tests. Extend it, add `func test_*()` methods, use the checks below.
extends RefCounted

var failures: PackedStringArray = []


func check(ok: bool, message := "check failed") -> void:
	if not ok:
		failures.append(message)


func check_eq(actual: Variant, expected: Variant, message := "") -> void:
	if actual != expected:
		failures.append("%s expected %s, got %s" % [message, expected, actual])
