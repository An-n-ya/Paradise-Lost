################################################################################
## Automated flow tests for the Paradise Lost demo.
##
## Four full playthroughs cover all 16 choice options across C1..C5 and the
## conditional dialogue each branch unlocks. Run with:
##
##     renpy.sh "<project dir>" test
##
## The suite exits with code 0 when every testcase passes, 1 on any failure.
################################################################################

## The engine only registers the label-tracking callback on script reload,
## so register it here to make "until label <name>" work on a cold start.
init python:
    _label_cb = renpy.test.testexecution.add_reached_label
    if _label_cb not in renpy.config.label_callbacks:
        renpy.config.label_callbacks.append(_label_cb)


testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 10.0
        $ preferences.text_cps = 0
        $ preferences.afm_enable = False

        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit


## C1 ask / C2 satia pays / C3 satia responds / C4 price / C5 toast satia
testcase full_satia_path:
    click "开始游戏"

    # P0 prologue cards.
    advance until "INTERMISSION"

    # C1 - ask directly.
    advance until screen "choice"
    click "直接问"
    advance until "还活着"

    advance until label s2

    # C2 - satia pays.
    advance until screen "choice"
    click "幸子请"
    advance until "今晚我请"

    advance until label s3

    # C3 - satia responds.
    advance until screen "choice"
    click "幸子回应"
    advance until "利息面议"

    advance until label s4

    # C4 - pick by price.
    advance until screen "choice"
    click "价格"
    advance until "理由充分"

    advance until label s5

    # C4 echo in the naming scene.
    advance until "当初就是它便宜"

    # C5 - toast satia, attention check.
    advance until screen "choice"
    click "为幸子"
    advance until "轻得不像她"
    assert eval att_satia == 3
    assert eval att_liris == 1
    assert eval att_evira == 0

    advance until screen "main_menu"


## C1 candy / C2 evira pays / C3 evira responds / C4 rooms / C5 toast evira
testcase full_evira_path:
    click "开始游戏"

    advance until screen "choice"
    click "先递一颗话梅糖"
    advance until "甜的"

    advance until label s2

    advance until screen "choice"
    click "千晴请"
    advance until "有家底的人"

    advance until label s3

    advance until screen "choice"
    click "千晴回应"
    advance until "轮到我说给你听"

    advance until label s4

    advance until screen "choice"
    click "三个房间"
    advance until "刚刚好"

    advance until label s5

    # C4 echo in the naming scene.
    advance until "不多，不少"

    # C5 - toast evira, attention check.
    advance until screen "choice"
    click "为千晴"
    advance until "工工整整"
    assert eval att_evira == 3
    assert eval att_liris == 1

    advance until screen "main_menu"


## C1 dinner / C2 split bill / C3 silence / C4 light / C5 toast liris
testcase full_liris_path:
    click "开始游戏"

    advance until screen "choice"
    click "不问，宣布开饭"
    advance until "反而就轻了"

    advance until label s2

    advance until screen "choice"
    click "AA"
    advance until "史无前例的财政透明"

    advance until label s3

    # C3 - silence: music restarts inside the branch.
    advance until screen "choice"
    click "沉默"
    advance until "靠着同一面墙"
    assert eval renpy.music.is_playing(channel="music")

    advance until label s4

    # C4 - pick by light, rooftop detour included.
    advance until screen "choice"
    click "采光和屋顶"
    advance until "也是海"

    advance until label s5

    # C4 echo in the naming scene.
    advance until "当时，就是它"

    # C5 - toast liris, attention check.
    advance until screen "choice"
    click "为琉花"
    advance until "以前，都是反过来的"
    assert eval att_liris == 2
    assert eval att_evira == 1

    advance until screen "main_menu"


## C1 ask / C2 satia pays / C3 satia responds / C4 price / C5 toast the house
## Also verifies the ending card sequence.
testcase full_house_toast:
    click "开始游戏"

    advance until screen "choice"
    click "直接问"

    advance until label s2
    advance until screen "choice"
    click "幸子请"

    advance until label s3
    advance until screen "choice"
    click "幸子回应"

    advance until label s4
    advance until screen "choice"
    click "价格"

    advance until label s5

    # C5 - toast the house itself, no attention gain.
    advance until screen "choice"
    click "为这间屋子"
    advance until "最没有戏剧性"
    assert eval att_satia == 2
    assert eval att_liris == 1

    # Ending cards.
    advance until "敬请期待"
    advance until "FIN"

    advance until screen "main_menu"
