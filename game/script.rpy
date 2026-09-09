################################################################################
## Paradise Lost - Demo "Intermission"
##
## Structure: prologue P0 -> scenes S1..S5 -> epilogue.
## Five choice points C1..C5 feed the "attention" values used by C5.
################################################################################

## ------------------------------------------------------------------ characters
##
## Speaker callback: only the character who is talking is shown, everyone
## else is hidden. Attribute changes are still driven by explicit `show`
## statements in the script (renpy.get_attributes picks up the latest one).

init python:
    _speaker_defaults = {
        "satia": ("neutral",),
        "evira": ("happy",),
        "liris": ("downcast",),
    }

    # tag + attributes of the sprite currently on screen.
    _speaker_shown = None

    def _speaker_callback(tag):
        def cb(event, interact=True, **kwargs):
            global _speaker_shown

            if event != "begin":
                return

            attr = renpy.get_attributes(tag, if_hidden=_speaker_defaults[tag]) or _speaker_defaults[tag]
            target = (tag,) + tuple(attr)

            if _speaker_shown == target and renpy.showing(tag):
                return

            _speaker_shown = target

            for t in _speaker_defaults:
                if t != tag:
                    renpy.hide(t)
            renpy.show(" ".join(target))

            # quick crossfade only when the sprite actually changes
            renpy.with_statement(Dissolve(0.2))
        return cb

define satia = Character("幸子", who_color="#a78bfa", callback=_speaker_callback("satia"))
define evira = Character("千晴", who_color="#fb7185", callback=_speaker_callback("evira"))
define liris = Character("琉花", who_color="#5eead4", callback=_speaker_callback("liris"))
define edan = Character("千纮", who_color="#cbd5e1")

define agent_a = Character("中介A", who_color="#a09db2")
define agent_b = Character("中介B", who_color="#a09db2")
define agent_c = Character("中介C", who_color="#a09db2")
define keeper = Character("老板", who_color="#a09db2")

## Black-screen text cards, centered on screen (uses Ren'Py's built-in
## `centered_window` / `centered_text` styles, the same as the `centered`
## statement).
define card = Character(None,
    window_style="centered_window",
    what_style="centered_text",
    what_color="#eceaf2", what_size=56, what_line_leading=40)

define datecard = Character(kind=card, what_size=72, what_color="#a78bfa")
define titlecard = Character(kind=card, what_size=160)
define sectioncard = Character(kind=card, what_size=96)
define quotecard = Character(kind=card, what_size=44, what_color="#b9b5cf")

## Display menu captions as narrator text while choices are on screen.
define config.narrator_menu = True

## ------------------------------------------------------------------ audio

define audio.bgm_title = "audio/bgm-title.wav"
define audio.bgm_theme = "audio/bgm-theme.wav"
define audio.bgm_street = "audio/bgm-street.mp3"
define audio.bgm_talk = "audio/bgm-talk.ogg"
define audio.bgm_comedy = "audio/bgm-comedy.wav"

define audio.se_wind = "audio/se-soundreality-wind-blowing.mp3"
define audio.se_snow = "audio/se-snow-footstep.mp3"
define audio.se_crowd = "audio/se-crowd.wav"
define audio.se_oden = "audio/se-boiling-soup.mp3"
define audio.se_chime = "audio/se-EntranceChime.wav"
define audio.se_elevator = "audio/se-ElevatorAnnouncement 1.wav"

init python:
    # loopable ambient channel for wind / crowd / oden pot etc.
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)

## ------------------------------------------------------------------ layout
##
## Single speaker slot: uniform 1080x1920 sprites shown at zoom 1.0 on a
## 2560x1440 screen, so the frame crops at ~75% of body height (thigh-up
## framing), head near the top of the screen.

transform speaker_slot:
    xcenter 0.5
    ypos 0
    zoom 1.0

## ------------------------------------------------------------------ sprites
##
## All sprites are uniform 1080x1920 full-body transparent PNGs in images/.
## Explicit definitions are required (automatic filename registration is
## disabled in this Ren'Py version). Framing comes from
## config.default_transform = speaker_slot (see layout section below), which
## also applies to 2560x1440 backgrounds as an identity transform.

image satia neutral = "images/satia_neutral.png"
image satia eyebrow = "images/satia_eyebrow.png"
image satia serious = "images/satia_serious.png"
image satia smirk = "images/satia_smirk.png"

image evira neutral = "images/evira_neutral.png"
image evira happy = "images/evira_happy.png"
image evira sad = "images/evira_sad.png"
image evira anxious = "images/evira_anxious.png"
image evira short = "images/evira_short.png"

image liris downcast = "images/liris_downcast.png"
image liris side = "images/liris_side.png"
image liris blank = "images/liris_blank.png"
image liris front = "images/liris_front.png"

## Applied to every image shown without an `at` clause: identity placement
## for 2560x1440 backgrounds, thigh-up framing for 1080x1920 sprites.

define config.default_transform = speaker_slot

## ------------------------------------------------------------------ backgrounds

image bg overpass = "images/bg_overpass.jpg"
image bg conv store = "images/bg_conv_store.jpg"
image bg hospital dusk = "images/bg_hospital_dusk.jpg"
image bg livehouse = "images/bg_livehouse_room.jpg"
image bg street xmas = "images/bg_street_xmas.jpg"
image bg room a = "images/bg_room_a.jpg"
image bg room b = "images/bg_room_b.jpg"
image bg room c = "images/bg_room_c.jpg"
image bg room c night = "images/bg_room_c_night.jpg"
image bg rooftop = "images/bg_rooftop.jpg"
image bg agency = "images/bg_agency.jpg"

## ------------------------------------------------------------------ title snow
##
## Layered falling-snow used on the title screen. Back-to-front layers share
## the CreateFlutterParticles system from the Immersive Particle VFX library
## (libs/immersive_particle_vfx). Files are referenced by explicit path so
## this does not depend on automatic image registration.

## Slowly-turn-and-sway helper for the foreground flakes (modelled on the
## library's own rotate_leaf transform).
transform rotate_snow(child, zoom=1.0, alpha=1.0):
    child
    zoom zoom alpha alpha
    choice:
        rotate 0
        linear 5.0 rotate 360
        repeat
    choice:
        rotate 0
        linear 4.6 rotate -360
        repeat
    choice:
        rotate -60
        ease 3.2 rotate 60
        ease 3.0 rotate -60
        repeat

define snow_back = CreateFlutterParticles(
    image=Transform("images/ImmersiveParticleVFX/feniks snow dust fireflies rain/snow1.webp",
                    xsize=7, fit="contain", alpha=0.4),
    particle_size=7,
    amount=220, fast=True,
    xysize=(config.screen_width, 650), mask_borders=(0, 0, 0, 100),
    xspeed=(-10, 10), yspeed=(60, 100),
    flutter_width=50, flutter_xtime=(6, 10),
)

define snow_mid = CreateFlutterParticles(
    image=Transform("images/ImmersiveParticleVFX/feniks snow dust fireflies rain/snow1.webp",
                    xsize=10, fit="contain", alpha=0.5),
    particle_size=10,
    amount=140, fast=True,
    xysize=(config.screen_width, 800), mask_borders=(0, 0, 0, 100),
    xspeed=(-20, 20), yspeed=(100, 200),
    flutter_width=100, flutter_xtime=(6, 10),
)

define snow_mid2 = CreateFlutterParticles(
    image=Transform("images/ImmersiveParticleVFX/feniks snow dust fireflies rain/snow1.webp",
                    xsize=15, fit="contain", alpha=0.6),
    particle_size=15,
    amount=90, fast=True,
    xysize=(config.screen_width, config.screen_height),
    xspeed=(-25, 25), yspeed=(180, 280),
    flutter_width=120, flutter_xtime=(6, 10),
)

define snow_front = CreateFlutterParticles(
    image=[
        rotate_snow("images/ImmersiveParticleVFX/npckc snowflakes leaves stars/npckc_snow_1.png",
                    zoom=0.10, alpha=0.55),
        rotate_snow("images/ImmersiveParticleVFX/npckc snowflakes leaves stars/npckc_snow_4.png",
                    zoom=0.10, alpha=0.55),
        rotate_snow("images/ImmersiveParticleVFX/npckc snowflakes leaves stars/npckc_snow_2.png",
                    zoom=0.08, alpha=0.55),
        rotate_snow("images/ImmersiveParticleVFX/npckc snowflakes leaves stars/npckc_snow_6.png",
                    zoom=0.10, alpha=0.55),
    ],
    particle_size=50,
    amount=6, fast=True, delay=(0.0, 2.0),
    xspeed=(-35, 35), yspeed=(260, 380),
)

## ------------------------------------------------------------------ layout
##
## Single speaker slot: uniform 1080x1920 sprites shown at zoom 1.0 on a
## 2560x1440 screen, so the frame crops at ~75% of body height (thigh-up
## framing), head near the top of the screen.

transform speaker_slot:
    xcenter 0.5
    ypos 0
    zoom 1.0

## Milton quote overlay, shown on top of the night window scene.
screen milton_quote():
    frame:
        background None
        vbox:
            xalign 0.5
            yalign 0.30
            spacing 26
            text "\"They hand in hand, with wandering steps and slow,\"":
                size 48
                color "#dcd9ea"
                text_align 0.5
                outlines [(2, "#000000cc", 0, 0)]
            text "\"Through Eden took their solitary way.\"":
                size 48
                color "#dcd9ea"
                text_align 0.5
                outlines [(2, "#000000cc", 0, 0)]
            null height 8
            text "— JOHN MILTON ・ PARADISE LOST ・ BOOK XII —":
                size 26
                color "#a09db2"
                text_align 0.5
                outlines [(2, "#000000cc", 0, 0)]

## ------------------------------------------------------------------ state

default att_satia = 0
default att_evira = 0
default att_liris = 0
default c1_pick = ""
default c4_pick = ""


################################################################################
## P0 - The people outside the gate
################################################################################

label start:
    jump p0


label p0:
    scene black with Dissolve(1.0)
    stop music
    stop ambient
    play ambient se_wind volume 0.22

    card "有些人生在乐园里。\n有些人，是被乐园赶出来的。"

    card "十二月二十一日，泉千晴被家庭除名。\n十二月二十四日，姬里琉花在雪地里停止了呼吸——\n大约，几分钟。"

    ## fragment shots: A overpass / C convenience store (B has no matching bg)
    scene bg overpass with Dissolve(0.4)
    pause 1.6
    scene black with Dissolve(0.4)
    pause 0.3
    scene bg conv store with Dissolve(0.4)
    pause 1.6
    scene black with Dissolve(0.4)
    pause 0.5

    card "现在是十二月二十五日，星期四。\n幸存者们，无处可去。"

    play music bgm_street fadein 4.0 volume 0.5

    quotecard "\"They hand in hand, with wandering steps and slow,\nThrough Eden took their solitary way.\""

    titlecard "失乐屋"

    card "DEMO ・ INTERMISSION"

    jump s1


################################################################################
## S1 - Prescription and side effects
################################################################################

label s1:
    scene bg hospital dusk with Dissolve(1.0)
    play ambient se_wind volume 0.15

    "医院门诊楼门口的长椅上，坐着三个不太搭配的人。"
    "穿皮夹克的那个在转硬币。硬币在她指节间翻过来，又翻过去，像一只永远不出错的节拍器。"
    "穿米色大衣的那个在抄笔记，抄得极认真，仿佛这门课期末要考。"
    "最里面的那个，抱着一只白色药袋，看着自己的鞋尖。"

    liris "「……回去吧。」"
    satia "「急什么。医生说的，『多晒太阳』。」"
    satia "「今天的太阳余额不足，正在充值。我们等。」"

    "她说着，从琉花手里抽走了药袋，抖出说明书，眯起眼睛。"

    show satia eyebrow

    satia "「我看看……『常见副作用：嗜睡、口干、食欲改变、头晕』。」"
    satia "「好家伙，你确定这不是毒药？」"

    show liris side with dissolve

    "琉花的嘴角动了一下。很小的一下，像水面底下的鱼。"

    evira "「这个不好笑。」"
    "千晴凑过来，指着说明书下半页，语速比平时快了半拍。"
    evira "「『一日三次，饭后服用』。琉花，记住了吗？饭后。」"
    satia "「你干嘛，要替她考这个吗。」"
    evira "「嗯。」（认真点头）「饭前记不住，饭后会忘。所以要写下来。」"

    "幸子转硬币的手，停了半拍。"

    show satia serious

    satia "「……行吧。那就写下来。」"

    "她不只是写。本子旁边还摆着一只一周分格的药盒，早、中、晚，每一格都贴了小小的标签。"
    "幸子拿起来端详了两秒。"

    show satia smirk

    satia "「又不是期末复习，写这么仔细。」"
    evira "「复习是为了及格。及格是不够的。」"
    "琉花抱着药袋，看了看那只药盒，又看了看千晴。"
    "她把药袋轻轻放在了药盒旁边。像把什么东西，托付出去了。"

    "天色沉下去。霓虹灯次第亮起来，把长椅的影子拉得很长很长。"
    "幸子把说明书折成方块塞回药袋，袋口拧了两圈。她看了琉花一眼——看了很久，久到不像她。"

    menu:
        "怎么问出那句话——「你现在，感觉怎么样」"

        "直接问":
            $ att_liris += 1
            $ c1_pick = "ask"
            show satia neutral
            satia "「喂。现在，感觉怎么样。」"
            liris "「……还活着。」"
            satia "「行。」"

        "先递一颗话梅糖":
            $ att_liris += 1
            $ c1_pick = "candy"
            show satia neutral
            "幸子从夹克内袋摸出一颗皱巴巴的话梅糖，隔着药袋的边缘递过去。"
            liris "「……」（接了）"
            liris "「……甜的。」"
            "她把糖纸折成一个很小的方块，收进口袋。"

        "不问，宣布开饭":
            $ att_evira += 1
            $ c1_pick = "dinner"
            show satia neutral
            satia "「走了。吃饭。圣诞节，总得吃点热的。」"
            "琉花站起来的动作，比这个下午任何时刻，都要快一点点。"

    ## ---- merge ----
    stop ambient fadeout 2.0
    $ renpy.music.set_volume(0.25, delay=2.0, channel="music")

    "千晴忽然站住了。她仰起头。"
    evira "「……雪。」"
    "初雪落在她的睫毛上，没有立刻化掉。"

    if c1_pick == "dinner":
        show satia neutral
        satia "「哦，雪。……快点，趁热。」"
    else:
        show satia neutral
        satia "「哦，雪。」（起身，拍掉外套上的灰）「走了。圣诞节，总得吃点热的。」"

    play sound se_snow

    jump s2


################################################################################
## S2 - A lie that only shines one month a year
################################################################################

label s2:
    scene bg street xmas with Dissolve(1.0)
    stop ambient fadeout 1.0
    $ renpy.music.set_volume(0.55, delay=1.5, channel="music")
    play ambient se_crowd volume 0.18

    "商店街的拱廊下，圣诞灯饰还亮着。"
    "二十五号晚上的商业街，像一场散了一半的宴席——卷帘门拉下大半，还亮着的店不到三成，音乐有一搭没一搭。"

    satia "「两个人，一共，」（在口袋里数硬币）「三十七块五。」"
    satia "「今晚的伙食预算。董事会已经批复了，不许有异议。」"

    scene bg conv store with dissolve
    stop ambient fadeout 1.0
    play sound se_chime
    play ambient se_oden volume 0.4

    "便利店的关东煮锅冒着白汽。玻璃盖上凝着水珠，一颗一颗，慢慢滚回锅里去。"

    evira "「请问……」"
    "千晴站在柜台前，郑重得像在答辩。"
    evira "「萝卜，为什么要煮这么久？」"
    satia "「因为它便宜。」"
    satia "「久煮，是它唯一的尊严。」"
    evira "「……不对吧。是因为它很难入味，需要时间。」"
    satia "「一个意思。尊严这种东西，也很难入味。」"
    evira "「这个说法不对。但是我说不过你。」"

    "琉花站在两人身后，隔着半步的距离，看着关东煮的白汽。"

    menu:
        "关东煮之夜，谁付钱"

        "幸子请":
            $ att_satia += 1
            "幸子把硬币一枚一枚码在柜台上，码得整整齐齐，像在数一副不完整的牌。"
            satia "「今晚我请。穷人的志气，懂吗。」"
            "付完钱，她的钱包里剩下两枚一块的。她看了一眼，很快合上——快到另外两个人都没有看见。"

        "千晴请":
            $ att_evira += 1
            "千晴掏出手机去扫码，被幸子按住了手腕。"
            satia "「你的钱要撑到找到工作。省着。」"
            evira "「可是，三十七块五是预算……」"
            satia "「预算重新分配。董事长特权。」"
            "千晴看着她。半晌，小声地——"
            evira "「……谢谢。」"
            "这是她离家之后，第一次清楚地意识到：自己再也不是「有家底的人」了。"

        "AA":
            $ att_liris += 1
            "三个人把钱摊在便利店窗台上数。硬币、纸币、零钱，摊开小小的一片。"
            satia "「史无前例的财政透明。」"
            evira "「两个人，一共出了十八块七。」"
            liris "「……我，十二块八。」"
            "店员撇了他们一眼。"

    ## ---- merge ----
    "三个纸杯，三串关东煮。萝卜、魔芋丝、鱼豆腐，各按各的预算。"
    "琉花把自己那块萝卜，夹进了千晴的纸杯里。"
    evira "「……诶？」"
    liris "「……尊严，给你。」"
    "她进店以来第一个主动的动作，快得像没有发生过。"
    "千晴看着纸杯里多出来的萝卜，认真想了想，得出了结论。"
    evira "「这是最贵的部分。」"
    "她说得那么认真，琉花差点笑出来。"
    "差点。"

    "出了便利店，三个人沿着大街慢慢走。谁也没说话，可是脚步走得很齐——左，右，左。路灯把三个影子拉长，又收短，又拉长。"
    "千晴小口小口地喝汤。喝到一半，忽然说："
    evira "「原来关东煮，是热的呀。」"
    satia "「……它一直是热的。你是第一次站在关东煮的这一边。」"
    "千晴想了想这句话，没有反驳。她把汤喝完了，一滴也没剩。"

    scene bg overpass with Dissolve(1.0)
    stop ambient fadeout 1.5
    play ambient se_wind volume 0.3
    $ renpy.music.set_volume(0.2, delay=2.0, channel="music")

    "天桥上，风大。整座城市在栏杆外铺开，一直铺到看不见的地方——灯火连成一片浅浅的海。"

    satia "「今晚睡哪，我跟老板说好了。白桥，一个开 livehouse 的哥们儿，休息间能挤。代价是明天帮他搬音响。」"
    evira "「搬音响……很重吗？」"
    satia "「双十五寸主音箱，一只四十公斤。两只。」"
    evira "「我会努力的。」"
    satia "「你负责扶门。」"

    "琉花一直没说话。她看着桥下的车流，围巾被风掀起一角。"
    liris "「……我那边。」"
    liris "「那边，不会再回去了。」"
    "没有人问「为什么」。幸子只是伸手，把她的围巾按了回去。"
    satia "「行。那就都住 livehouse。」"
    "好像「回去」是一件不需要理由的事。像雪不需要理由就下。"

    liris "「圣诞的灯……过完元旦，就会拆掉了。」"
    satia "「嗯。」"
    liris "「一年，只亮一个月的谎话。」"
    satia "「至少它诚实地预告了散场。」"

    "千晴听不太懂，但她听得很认真。她把这句话记在了本子上。"
    "然后她合上本子，看向那片灯火。"

    satia "「神谷町，一千万人。」"
    satia "「今晚亮着的窗，一扇，都不是我们的。」"
    "这句话说完，风都显得多余。"

    evira "「那就去找一扇。」"
    "她说得那么直，像在说「那就去买一张明天的车票」。"
    "幸子看了她两秒。"
    satia "「……行啊。」"
    satia "「找一扇。」"

    scene black with Dissolve(1.0)
    stop ambient fadeout 1.0
    stop music fadeout 3.0

    datecard "2025.12.26 – 12.31"

    jump s3


################################################################################
## S3 - New year family meeting
################################################################################

label s3:
    scene bg livehouse with Dissolve(1.0)
    play music bgm_talk volume 0.65

    "白桥，livehouse 休息间。"
    "一个灯泡，三个睡袋，半墙的酒箱和音响残骸。摇滚海报的边角翘起来，露出底下更老的一张，一层压着一层，像这栋楼的年轮。"
    "他们在这里住了七天。第七天，是新年。"

    "昨晚的跨年，是用一锅泡面跨的。电视里放着跨年晚会，幸子跟着倒数——「五、四、三、二、一，新年不快乐。」千晴认真地纠正：「新年快乐。」争到一半，两个人发现琉花在第二声倒数里就睡着了。"
    "于是跨年变成了两个人的，和一个人的呼吸声。"

    "千晴把一块纸箱板立在三人中间，顶上写着一行字——「新年家庭会议・第一次」。"

    satia "「家庭会议。」"
    satia "「我们家谁定的这个词。」"
    evira "「我。有什么问题吗。」"
    satia "「问题是没有问题。就是，土。」"
    evira "「土，但是清楚。」"

    "琉花裹着睡袋坐在最外面，只露出半张脸。"
    liris "「……像个，词。」"
    satia "「她都说像个词了。开始吧，主席。」"

    evira "「议题一。我们还有多少钱。」"
    "千晴翻开本子。本子上是密密麻麻的表格——这七天每一笔开销，精确到五毛。"

    evira "「住宿抵劳务，不计。伙食，七天，四百六十二块。交通——」"
    satia "「直接说结论。」"
    evira "「合计，五万。」"
    "幸子把这两个字重复了一遍，像在试音。"
    satia "「五万。全买关东煮，能买三千三百三十三碗。不带汤。」"
    evira "「没有人会这么做。」"
    satia "「我在做可行性分析。」"
    evira "「可行性是，零。」"

    "笑声在小小的休息间里显得很大。"
    "琉花在睡袋里，很小声地跟着笑了一下。没有人看她，但都听见了。"

    show satia smirk

    satia "「收入这边。下个月我有两场零工，调音，一场八百。另外，存款——」（顿了顿）「存款就是刚才那个五万。」"

    show satia neutral

    evira "「记上了。收入项。」"
    "安静了一小会儿。然后，睡袋里传出很小的声音。"
    liris "「……我，也有。」"
    "两拍。她说的「也有」是什么，没有人问。"
    satia "「好。资产充足。下一题。」"

    satia "「议题二，住哪。我先说个方案。」"
    satia "「三个 loser 合租，房租砍三刀，省下的钱还能买台二手 Switch。」"
    evira "「什么是 loser。」"
    satia "「赢家眼里的其他人。」"
    evira "「……我们不是 loser。」"
    satia "「哦？」"
    evira "「我们只是，还没有开始赢。」"

    "幸子被这句话噎了一下。她低头转硬币，转得比平时快。"

    show satia serious

    satia "「……行。还没有开始赢的人，合租。」"

    "千晴已经开始在本子上画表格了。房租、押金、通勤、伙食、水电——五列，往下是空的。"
    evira "「两室或者三室。人均不能超过一千五。要在地铁站一公里以内——」"
    satia "「停。你在做毕业论文吗。」"
    evira "「这是预算表。」"
    evira "「预算表可以救人。」"

    "琉花看着那张越画越满的表格，看了很久。"

    liris "「……家庭会议。」"
    evira "「嗯？」"
    liris "「好奇怪的词。」"
    satia "「嫌弃？那叫『破产者同盟第一次代表大会』。」"
    liris "「……不是。」"

    "她的声音低下去，低到几乎贴着地面。"
    liris "「只是，有点，像——」"
    "那个词她没有说出口。它躺在休息间的空气里，所有人都听得见它的形状，没有人去捡。"
    "像，家。"

    "琉花把脸埋进睡袋的边缘，只露出眼睛。再看出来的时候，眼睛看着灯泡。"
    liris "「……我会拖累你们。」"

    "灯泡嗡嗡地响。"
    "这句话之后的安静，是这七天里最长的一次。"

    stop music fadeout 2.5

    menu:
        "「我会拖累你们。」——由谁回应"

        "幸子回应":
            $ att_satia += 1
            "幸子把硬币往纸箱上一拍，不转了。"
            show satia serious
            satia "「『拖累』这个词，撤回。」"
            satia "「你自己算算。你会写，会画，看书比我喝水多。这屋里最值钱的东西就是你的脑子。还拖累。」"
            liris "「……那不产生现金流。」"
            satia "「谁说钱是唯一的现金流。」"
            "幸子往椅背上一靠，摘下一只耳机，看着她。"
            satia "「那就用别的方式还。你会写——写点什么。写给我们这个破同盟的，什么都行。」"
            "琉花看着她。很久。"
            liris "「……高利贷。」"
            satia "「利息面议。」"
            show satia neutral

        "千晴回应":
            $ att_evira += 1
            "千晴放下笔。她没有马上说话，先深呼吸了一次——她每次要说重要的话之前，都这样。"
            show evira sad
            evira "「琉花。五月的时候，你对我讲过一句话。」"
            liris "「……」"
            evira "「『我想成为的是我自己，然后才是女性。』」"
            evira "「那时候我不懂。现在，懂了一半。」"
            evira "「是你把我带到这里的。所以——」"
            "千晴把那句话，一个字一个字地，还给她。"
            evira "「现在，轮到我说给你听。」"
            "琉花的指尖在睡袋里蜷了一下。"
            liris "「……抄我的，要注明出处。」"
            evira "「嗯。我会注明。」"
            show evira happy

        "沉默":
            "谁都没有说话。"
            "十秒。二十秒。灯泡嗡嗡地响，把沉默照得发亮。"
            "然后幸子动了。她从包里摸出手机和一副耳机，插上分线器，把一只耳机递给千晴，另一只越过睡袋，塞进琉花手里。"
            play music bgm_talk volume 0.18 fadein 2.0
            "播放键按下去。"
            "没有解释，没有安慰。歌是幸子自己做的，鼓点很轻，像有人在很远的地方敲门。"
            "三个人的肩膀，靠着同一面墙。同一副耳机，一人一只。"
            "有些歌就是为这种时刻写的——词是多余的，所以没写词。"

    ## ---- merge: bring the talk bgm back ----
    if renpy.music.is_playing(channel="music"):
        $ renpy.music.set_volume(0.65, delay=2.5, channel="music")
    else:
        play music bgm_talk volume 0.65 fadein 2.0
    play sound se_crowd volume 0.5

    "夜深了。"

    evira "「议题三。钱，从哪里来。」"
    "千晴说这句话的时候，握着笔的手指收紧了。"
    evira "「我——有一个哥哥。」"
    satia "「嗯。」"
    evira "「如果我开口，他会给的。」"
    evira "「但是，哥他……不是坏人。只是，他的温柔总是从很远的地方绕过来。绕很远。」"
    satia "「绕多远？」"
    evira "「大概，绕一个『对不起』那么远。」"

    "幸子没有接话。她把硬币收进口袋，像是把某个问题也一起收了进去。"

    show satia serious

    satia "「打给他。」"
    evira "「可是——」"
    satia "「借的。记账。以后还。」"
    satia "「我们这种还没有开始赢的人，最擅长的就是『以后』。」"

    "千晴看着她，然后点头。她把这一条也写进了预算表。备注栏里，写的是：借款，待还。"

    "很久以后回头看，那个晚上，这个世界上多了一张三个人共用的资产负债表——负债栏里写着两个家庭，资产栏里，写着彼此。"

    show satia neutral

    satia "「散会。」"
    "幸子躺回睡袋，双手枕在脑后。"
    satia "「那就——先找一个地方住下吧。」"

    "黑暗还没来之前，千晴的声音从睡袋里冒出来，闷闷的。"
    evira "「那个——新年快乐。」"
    "这次没有争。幸子对着天花板，看了一会儿那个昏黄的灯泡。"
    satia "「……新年快乐。」"
    "又过了很久，久到两个人都以为她睡着了。睡袋里，传出很小很小的声音。"
    liris "「……快乐。」"

    "灯灭了。黑暗里，三个人的呼吸，慢慢变成同一个节奏。"
    "窗外，新年第一天的雪，落得悄无声息。"

    scene black with Dissolve(1.5)
    stop music fadeout 3.0

    jump s4


################################################################################
## S4 - House hunting, or the bankrupt alliance
################################################################################

label s4:
    datecard "2026.1.2"
    scene bg livehouse with Dissolve(1.0)
    play music bgm_comedy volume 0.6

    "一月二日，上午。"
    "千晴站在 livehouse 后面的楼道里打电话。画面只有她的侧脸，和她呼出的白气。"

    show evira anxious with dissolve

    edan "「喂。」（电话音）"
    evira "「哥。」"
    edan "「……嗯。」"
    evira "「那个，我，想跟你借一笔钱。租房。会还的，我记了账——」"
    edan "「地址发我。」"
    evira "「诶？」"
    edan "「中介的，还是房东直租的。」"
    evira "「还，还没找……」"
    edan "「找好发我。押几付几，先问清楚。」"
    evira "「哥——」"
    edan "「别被赶两次。」"

    hide evira with dissolve

    "千晴握着手机，在楼道里站了很久。很久。"
    "门没有关严。门缝里，幸子正把一张租房广告研究得格外认真——认真到广告上每一个错别字都被她用笔圈了出来。"

    show evira anxious with dissolve

    evira "「……你都听见了。」"
    satia "「楼道回音好。声学条件不错，这楼。」"
    evira "「谢谢。」"
    satia "「谢什么。我又没听见。」"

    hide evira with dissolve
    hide satia with dissolve

    "她把笔帽按上，把广告折好，塞回原处。两个人都假装这件事没有发生过。"

    ## ---- room A ----
    datecard "2026.1.5 ・ 银光区"
    scene bg room a with Dissolve(1.0)
    play sound se_elevator

    "房源 A，银光区，三十八层。"
    "中介是个油光锃亮的年轻人，西装的折痕锋利得能切菜。"
    agent_a "「三位的眼光，独到。银光新区，人送外号『人造丛林』。落地窗，俯瞰全城——」"
    satia "「多少钱。」"
    agent_a "「押二付一，另外有一笔礼金——」"
    satia "「等等。什么是礼金。」"
    agent_a "「就是，感谢房东的，一笔心意。」"
    satia "「感谢他什么？」"
    agent_a "「感谢他把房子，租给我们。」"
    satia "「我们付钱，还要感谢收钱的？」"
    satia "「这是什么业态。」"

    "中介笑得像没听懂，又像听懂了装没听懂。幸子拉开样板间的冰箱。空的。连灯都没装。"
    satia "「空的。连瓶假酒都不摆。心不诚。」"

    "pass。判词由幸子当场宣读——"
    satia "「房子是好房子。我们是穷得刚正不阿的人。告辞。」"

    ## ---- room B ----
    datecard "2026.1.8 ・ 旧见坂"
    scene bg room b with Dissolve(1.0)
    play sound se_snow

    "房源 B，旧见坂，老公寓，便宜得可疑。"
    "中介阿姨五十多岁，全程没什么话。开门。闪身。抱臂。"
    "客厅很大，采光可以。问题在卧室——"
    "一整面墙，全是钩子。粗的，细的，成排，成列，从天花板一直排到腰的高度。"

    evira "「请问……这些钩子，是？」"
    agent_b "「别问。」"
    evira "「好的。」"

    "千晴的笔停在预算表上，不知道该把「钩子」归入哪一栏。"

    satia "「前任房客，什么职业？」"
    agent_b "「你别管。」"
    satia "「行。我不想知道。」"

    "琉花慢慢走到那面墙前面。她伸出手，隔着几厘米，顺着钩子的队列划过去，像在检阅一支沉默的军队。"
    liris "「……这里，挺好。」"
    satia "「不好。」"
    evira "「不好。」"
    "两个人难得地意见一致，快得像排练过。没有人知道琉花是不是在开玩笑。包括她自己。"

    "pass。判词——"
    satia "「走。这面墙让我睡不好。」"
    evira "「……你睡眠很好。」"
    satia "「从今晚开始不好。」"

    ## ---- room C ----
    datecard "2026.1.12 ・ 新见坂"
    scene bg room c with Dissolve(1.0)
    $ renpy.music.set_volume(0.25, delay=1.5, channel="music")

    "房源 C，新见坂，九十平，三室。"
    "中介小哥戴眼镜，今年大概第一次带看这么年轻的三人组。进门介绍之前，先把胸卡扶正了三次。"
    agent_c "「三室，一厅，东南朝向。老小区，但是安静。楼顶可以上，物业睁一只眼闭一只眼。离旧见坂商圈也近——呃，两位小姐，和一个……」"

    "他卡住了。视线在幸子和琉花之间来回了两趟，没敢下结论。"
    satia "「一个『和他们的胃口』。」"
    agent_c "「……好的。和他们的胃口。」"

    "琉花在玄关站了一会儿，先走了进去。"
    "客厅朝南。一月的太阳很低，斜斜地铺进来，铺在空荡荡的地板上，一直铺到窗边。"

    "千晴一间一间地看，在预算表上打钩。三个房间，押一付一，预算之内。"
    "幸子去敲了敲墙——「实心的。隔音，及格。」"
    "琉花一个人走到阳台上。"
    "她在阳台上站了很久。久到千晴的表格都画完了，久到中介小哥悄悄看了三次表。"
    "没有人去催她。"

    menu:
        "拍板之前——最看重的是什么"

        "价格":
            $ c4_pick = "price"
            satia "「就它了。理由充分——便宜。」"
            "中介小哥大概头一次见到看得这么快、还当场拍板的客户。"

        "三个房间":
            $ c4_pick = "rooms"
            evira "「三个房间。不多，不少。刚刚好。」"
            "她当场在纸箱板背面画了户型图，一人认领一间——用她那种答辩一样认真的语气。"

        "采光和屋顶":
            $ c4_pick = "light"
            satia "「这太阳，白送的。楼顶也算一半面积。」"
            agent_c "「楼顶能看到海。天气好的时候。」"
            satia "「天气好的时候的海，也是海。」"
            scene bg rooftop with dissolve
            pause 1.2
            scene bg room c with dissolve

    ## ---- merge: sign & move ----
    $ renpy.music.set_volume(0.6, delay=1.5, channel="music")
    datecard "1.12 签约 ・ 1.13 – 1.15 搬家"

    "签约那天，千晴把每一条款都读出了声，连中介小哥都听感动了。"

    "签字签到最后一个名字的时候，千晴的手机震了一下。转账，到账，附言一行小字——「押一付一。多退少补。」"
    "幸子看了一眼那行字，什么也没说。千晴把手机屏幕朝下，扣在桌上，然后把最后一笔签完了。"
    "这一笔，一式三份，房东一份，中介一份，他们一份。三个人传着签：幸子的字锋利，千晴的字端正，琉花的字很小，小得几乎要缩进纸里。"

    "然后是搬家。三天，四趟，一辆借来的面包车。"

    "幸子叉着腰站在一张沙发床前面，和老板对视。"
    keeper "「八百。」"
    satia "「六百。」"
    keeper "「七百八。」"
    satia "「六百。现金。现在搬。」"
    "老板看了看她指节上的旧茧，又看了看她身后抱着台灯的两个人，最后看了看自己店的卷帘门。"
    keeper "「……六百五。」"
    satia "「成交。——千晴，记账。」"

    "琉花盘腿坐在地板上，面前摊着一只书架的全部零件和说明书。"
    satia "「要帮忙吗。」"
    liris "「……说明书，是最诚实的文学。」"
    "她照着步骤，一步一步，不跳页，不怀疑。四个小时后，书架立起来了。"
    "很直。"

    "千晴把整个家的地板拖了三遍。第三遍的时候，幸子从她手里抢走了拖把。"
    satia "「这是家，不是考场。地板不会给你打分。」"
    evira "「可是干净——」"
    satia "「干净了。及格了。休息。」"

    "最后一样大件是床垫，面包车塞不下，幸子骑摩托驮回来的，绑了四道绳。"
    "雪后初晴。床垫在摩托后座上晃晃悠悠，像一块巨大的、打了补丁的吐司。"

    "一月十五日，日落之前，最后一个纸箱搬进了客厅。"

    scene black with Dissolve(1.2)
    stop music fadeout 2.5

    jump s5


################################################################################
## S5 - The night of naming
################################################################################

label s5:
    scene bg room c night with Dissolve(1.5)

    "夜。"
    "客厅里只有一盏二手落地灯亮着。灯罩上还留着上一个主人补的一块补丁，暖黄的光从补丁旁边漏出来，落在没拆完的纸箱上。"
    "晚饭是外卖煎饺，三大盒，摆在地板中央。"

    satia "「Wi-Fi 还没通。」"
    satia "「我们仨现在，officially，是信息社会的失踪人口。」"
    evira "「失踪人口，不需要报备吗？」"
    satia "「报备需要 Wi-Fi。完美闭环。」"

    "幸子从便利店塑料袋里掏出三罐不同的饮料，像发牌一样，一人面前放了一罐——可乐、桃子汽水、乌龙茶。"
    satia "「听天由命。」"

    "琉花看了一眼自己面前的桃子汽水，又看了一眼千晴面前的乌龙茶。她把两罐换了过来。"
    satia "「诶，为什么换。」"
    liris "「……她昨晚，念了两次可乐的广告。」"
    "千晴愣住了。昨晚她确实盯着手机，小声念了两遍广告词——「畅爽，开怀」——以为没有人听见。"
    evira "「你，你听到了。」"
    liris "「……嗯。」"
    "千晴抱着那罐可乐，半天没打开。耳朵红的。"

    "然后她像是下了什么决心，抬手，把假发摘了下来。"
    "银白色的短发塌下来。她把假发端端正正放在沙发扶手上，长长地、舒服地，叹了一口气。"

    show evira short with dissolve

    evira "「在家里，就不用戴了。」"

    "琉花看着她。看了两秒。"
    "然后，很轻地——"
    liris "「……好看。」"

    "千晴的眼睛睁大了。她大概准备了很久，准备应对任何一种反应——沉默，回避，或者客气。"
    "唯独没准备这一种。"
    evira "「……诶。」"
    evira "「谢谢。」"

    show evira short with dissolve

    "她说完，笑了。笑得整张脸都亮了，像那盏打了补丁的落地灯。"
    "琉花低下头去喝茶。耳朵也是红的。"

    "气氛好到幸子觉得，必须有人出来破坏一下。"

    show satia smirk

    satia "「行了行了，差不多得了。甜得我血糖升高。」"
    satia "「煎饺吃完了。办正事。」"
    evira "「正事？」"

    show satia neutral

    satia "「这房子，还没有名字。」"
    evira "「房子，需要名字吗？」"
    satia "「乐队都有名字。我们比乐队多两个房间，凭什么没有。」"

    "幸子清了清嗓子。"

    show satia smirk

    satia "「我先来。一号方案——『绝对零度分室』。」"
    evira "「否决。冷。」"
    satia "「二号方案——『彩虹莓果庄』。」"
    evira "「像女子宿舍。」"
    satia "「本来就是。」"
    evira "「……这个理由成立。但是还是像宿舍。」"

    "千晴想了想，认真地说——"
    evira "「『向阳庄』。太阳照进来的『向』。」"
    satia "「诶，这个有水平。谁教你的？」"
    evira "「没人教。客厅朝南。我想的。」"

    "轮到琉花了。"
    "琉花没有马上说话。她把乌龙茶罐放下，扶着膝盖，站了起来，走到窗边。"
    "雪停了。窗外的城市一直铺到天边，灯火一层压着一层，像退潮之后搁浅的星星。"

    liris "「弥尔顿写——」"

    ## first and only front-face reveal of the demo
    show liris front with dissolve

    "她的声音变了。不是平时那种贴着地面的声音，是另一种——一字一字，像在朗读，像在念给很远的人听。"

    liris "「『他们手拉着手，以彷徨而迟缓的脚步，走过伊甸，走上孤独的路。』」"

    show screen milton_quote
    with dissolve

    "玻璃上映着她的脸。窗外是一千万人，窗内是一个人。"

    hide screen milton_quote
    with dissolve

    liris "「乐园的门，关上了。钥匙，也没有发给我们。」"
    liris "「但是——门外，也可以有屋子。」"

    "她回过头。落地灯的暖光落在她脸上。"

    liris "「既然回不去，就在门外，自己搭一间。」"
    liris "「给被赶出来的人。给无处可去的人。」"

    "她看着幸子，又看着千晴。她的眼睛里有什么东西，安静地烧着。"

    liris "「……『失乐屋』，怎么样。」"

    show liris side with dissolve

    "客厅里安静了几秒。"

    evira "「失乐屋……」"
    liris "「……不喜欢？」"
    evira "「不。」"
    evira "「很喜欢。」"

    "幸子靠在纸箱上，转了两秒硬币。"

    show satia smirk

    satia "「土。」"
    satia "「土得像文学部毕业生起的名字。」"
    liris "「……本来就是。」"

    show satia neutral

    satia "「我知道。」"
    "她把可乐罐举了起来。"

    show satia smirk

    satia "「所以——挺好。」"

    "千晴从沙发底下把那块纸箱板翻了出来——从 livehouse 一路搬到新家，边角都磨圆了。她拿起马克笔，把四个名字挨个写上去：「绝对零度分室」「彩虹莓果庄」「向阳庄」。"
    "最后，在顶上，一笔一画地写了三个字。"
    "她没有划掉任何一个。"

    ## C4 echo
    if c4_pick == "price":
        satia "「当初就是它便宜。」"
        liris "「……嗯。还有别的。」"
    elif c4_pick == "rooms":
        evira "「三个房间。不多，不少。」"
    elif c4_pick == "light":
        liris "「……这扇窗。当时，就是它。」"

    "然后千晴做了一件事。她跑回自己房间，从还没拆的箱子里翻出相机——那台从家里带出来的、唯一没有被没收的东西。"
    evira "「第一顿饭。要拍下来。」"
    "幸子抬手挡脸：「本人肖像权很贵的。」"
    "千晴没有放下相机。她调了调参数，很认真地——"
    evira "「拍的是饭。你们只是背景。」"
    "快门响的时候，琉花悄悄往镜头里挪了半步。"
    "没有人看见。除了千晴。"

    "千晴站了起来。琉花也举起了罐子。三只罐子，凑到落地灯下面。"

    satia "「为『失乐屋』——等等，正式点。」"
    satia "「为失乐屋。和我们仨。」"

    menu:
        "碰杯之前——此刻，为谁举杯"

        "为幸子":
            $ att_satia += 1
            "她愣住了。硬币在指间停住，转不下去了。"
            satia "「……矫情。」"
            "然后她一仰头，把可乐喝掉了一半。"
            if att_satia > att_evira and att_satia > att_liris:
                "她把罐子捏扁的那个动作，比平时轻。轻得不像她。"

        "为千晴":
            $ att_evira += 1
            "千晴的眼睛一下子亮起来。她郑重其事地站起来，站得笔直，举汽水的姿势像举奖杯。"
            evira "「我，我会努力的。」"
            if att_evira > att_satia and att_evira > att_liris:
                "后来大家发现，纸箱板的背面，「向阳庄」三个字写得工工整整——她没有划掉，也没有解释。"

        "为琉花":
            $ att_liris += 1
            liris "「……为屋子。」"
            "她摇了头。但是举罐子的时候，她举得最高。"
            if att_liris > att_satia and att_liris > att_evira:
                "今晚，她看了我们很多次。以前，都是反过来的。"

        "为这间屋子":
            "谁都没有说话。三只罐子碰在一起。"
            "很奇怪，明明是最没有戏剧性的一个选项，三个人却都笑了。笑得最放松的一次。"
            "像已经是住了一辈子的家。"

    ## ---- merge: the toast, main theme enters in full for the first time ----
    play music bgm_street fadein 5.0 volume 0.7

    "罐子和罐子碰在一起，很轻的一声。"
    "落地灯的暖光下，可乐、汽水、乌龙茶——世界上最便宜的酒，敬世界上最小的家。"

    "窗外，一千万扇窗亮着。"
    "从今晚起，其中一扇，是他们的。"

    jump ending


################################################################################
## END - epilogue cards
################################################################################

label ending:
    scene black with Dissolve(2.0)

    card "十二月二十四日那晚，\n摩托在雪里开了三十公里。"

    card "关于那一晚——\n以及其他所有的夜晚——"

    sectioncard "《失乐屋》第一幕"
    card "敬请期待"

    quotecard "\"They hand in hand, with wandering steps and slow,\nThrough Eden took their solitary way.\""
    card "FIN ・ DEMO ・ INTERMISSION"

    card "企划 ・ 剧本 ・ 美术 ・ 音乐 ・ 演出"

    stop music fadeout 5.0

    return
