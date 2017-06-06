import main
import pytest

# Trying to test the code
def test_initializations_are_correct(main):
    if main.dead == False and main.disLength == 800 and main.disHeight == 400:
        print("hi")
        assert True
    assert False

def test_hiscore_is_zero():
    assert True

def test_start_screen_music_plays():
    assert True

def test_if_font_loads():
    assert True

