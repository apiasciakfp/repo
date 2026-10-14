"""Port of Java SmokeTest — re-targeted to Python (runtime version + scaffold wired)."""

import sys

import cardmultigame


def test_python_version_is_3_14():
    # Java original asserted the runtime was Java 21; here we assert Python 3.14.
    assert sys.version.startswith("3.14")


def test_scaffold_is_wired():
    # Java original asserted the "CardMultigame" name was non-empty.
    assert cardmultigame.__name__ == "cardmultigame"
