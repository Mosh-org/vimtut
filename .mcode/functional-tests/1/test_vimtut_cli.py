import subprocess, sys, os
D = os.path.join(os.environ["WORKSPACE_DIR"], "vimtut")
CODE = """
import json, sys
sys.path.insert(0, %r)
from vimtut import Vimtut
v = Vimtut()
print(len(v.basic_lessons), len(v.advanced_lessons), len(v.lessons))
l = v.lessons[0]
print(v.get_lesson_by_id(l['id'])['id'] == l['id'], v.get_lesson_by_id('nope'))
print(isinstance(v.all_basic_lessons_complete(), bool))
"""
def run(code):
    return subprocess.run([sys.executable, "-c", code % D], capture_output=True, text=True, timeout=60, cwd=D)

def test_lesson_loading():
    r = run(CODE)
    assert r.returncode == 0, r.stderr
    a, b, c = map(int, r.stdout.split("\n")[0].split())
    assert a > 0 and b > 0 and c == a + b

def test_lesson_lookup():
    r = run(CODE)
    assert r.returncode == 0, r.stderr
    assert r.stdout.split("\n")[1] == "True None"
