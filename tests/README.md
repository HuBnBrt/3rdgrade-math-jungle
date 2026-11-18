# Screen and behavior tests (Playwright)

The scripts expect to live in /tmp/t and read the built test page:

    mkdir -p /tmp/t && cp tests/*.py /tmp/t/ && cd /tmp/t
    python3 sizes.py   # home screen at many sizes
    python3 hm.py      # home: normal vs "המצב שלי" - nothing may move
    python3 fit.py     # every topic x small phones: text fits, card fits
    python3 gap.py     # check/hint buttons keep a gap from the card edge and the menu
    python3 stab.py    # nothing moves between question and feedback
    python3 sheet.py   # every teacher-sheet exercise accepts its right answer
    python3 enter.py   # Enter checks, Enter again moves on; additive merge unit test
    python3 drag.py    # ordering by drag and tap
    python3 res.py     # resume an interrupted practice
    python3 hw.py      # answers typed as Hebrew number words
    python3 adm2.py    # dashboard table fits without sideways scrolling

shot.py / chk.py hold the shared setup (Firebase replaced by stubs). The page path is set in shot.py.
