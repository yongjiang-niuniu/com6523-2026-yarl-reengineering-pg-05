import os

def test_result():
    assert os.path.exists("notes.md"), 'Cannot find notes.md'
    assert os.path.getsize("notes.md") > 100, 'Your report is too short.'
