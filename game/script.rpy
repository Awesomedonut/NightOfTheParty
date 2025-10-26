# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define Mikel = Character("Mikel", color="#FFFFFF")
define Friend = Character('Friend', color="#FFFFFF")
define unknown = Character('???', color="#FFFFFF")
define Jason = Character("Josh", color="FFFFFF")


# The game starts here.
init 800 python:
    class MouseParallax(renpy.Displayable):
        def __init__(self,layer_info):
            super(MouseParallax,self).__init__()
            self.xoffset,self.yoffset=0.0,0.0

            self.sort_layer=sorted(layer_info,reverse=True)
            cflayer=[]
            masteryet=False
            for m,n in self.sort_layer:
                if(not masteryet)and(m<0):
                    cflayer.append("master")
                    masteryet=True
                cflayer.append(n)
            if not masteryet:
                cflayer.append("master")
            cflayer.extend(["transient","screens","overlay"])
            config.layers=cflayer
            config.overlay_functions.append(self.overlay)
            return
        def render(self,width,height,st,at):
            return renpy.Render(width,height)
        def parallax(self,m):
            func = renpy.curry(trans)(disp=self, m=m)
            return Transform(function=func)
        def overlay(self):
            ui.add(self)
            for m,n in self.sort_layer:
                renpy.layer_at_list([self.parallax(m)],n)
            return
        def event(self,ev,x,y,st):
            import pygame
            if ev.type==pygame.MOUSEMOTION:
                self.xoffset,self.yoffset=((float)(x)/(config.screen_width))-0.5,((float)(y)/(config.screen_height))-1.0
            return

    def trans(d, st, at, disp=None, m=None):
        d.xoffset, d.yoffset = int(round(mdisp.xoffset)), int(round(mdisp.yoffset))
        if persistent.bg_parallax is False:
            d.xoffset, d.yoffset=0,0
        return 0

    mdisp = MouseParallax([(-20,"farthestBack"),(-50,"farBack"),(-80,"back"),(-30,"front"),(50,"inyourface")])

    config.tag_layer = {
    'effects': 'back', # particle effects etc.
    'sprite': 'back', 
    'bg' : 'farBack',

    # put your list of character images here
    'Josh': 'back',
    'jason': 'back',
    'mikel': 'back',
    'vivian2': 'back',
    
    # gif animations
    'friends': 'back',
    'paper': 'back',
    'shygirlstill': 'back',
    'mandshygirl': 'back',
    'happyend': 'back',
    }


init:

    python:
    
        import math

        class Shaker(object):
        
            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }
        
            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child
                
            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.                
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor
                
                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)
        
        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)
        
            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)
        
        class MouseCamera(renpy.Displayable):
            def __init__(self, child, xfactor=0.02, yfactor=0.02, **kwargs):
                super(MouseCamera, self).__init__(**kwargs)
                self.child = renpy.displayable(child)
                self.xfactor = xfactor
                self.yfactor = yfactor
                self.target_x = self.target_y = 0
                self.x = self.y = 0
                self.st = 0

            def event(self, ev, x, y, st):
                import pygame
                if ev.type == pygame.MOUSEMOTION:
                    # compute target offset: e.g., negative so movement is opposite mouse
                    self.target_x = - (x - (config.screen_width/2)) * self.xfactor
                    self.target_y = - (y - (config.screen_height/2)) * self.yfactor
                    renpy.redraw(self, 0)
                return ev

            def render(self, width, height, st, at):
                # simple smoothing:
                speed = (st - self.st) * 8  # faster smoothing factor
                self.x += (self.target_x - self.x) * speed
                self.y += (self.target_y - self.y) * speed
                self.st = st

                child_render = renpy.render(self.child, width, height, st, at)
                rv = renpy.Render(width, height)
                rv.blit(child_render, (self.x, self.y))
                # if still moving, schedule redraw
                if abs(self.x - self.target_x) > 0.5 or abs(self.y - self.target_y) > 0.5:
                    renpy.redraw(self, 0)
                return rv

            def visit(self):
                return [ self.child ]
    #

#

label splashscreen:
    scene black
    with Pause(1)

    show text "An Interactive Short Story by Ayushi Singh" with dissolve
    with Pause(6)

    show text "Remember, choices matter. There are different endings in this game." with dissolve
    with Pause(6)

    hide text with dissolve

    return

label start:
    stop music fadeout 3.0
    show bg black
    with Pause(5)

    scene bg party
    with fade
    play music "audio/main.mp3" fadein 3.0 volume 1.5

    "(During the end of summer 2002...)"
    "(I'm in this party with my friends, ready to party hard and make our lasting memories together.)"
    
    show friends photos
    with dissolve

    "(We're gonna graduate soon and I want to make sure to have the most fun before college starts.)"


hide friends photos
with dissolve

"(But before I could continue on my fun, I could feel someone's eyes on me.)"
"(It was no other than Josh. The guy who just couldn't stop asking me out from freshman year.)"
"(He looks as happy as always and approaches me with no hesitation.)"

show jason happy gif
with easeinright
Jason "Hey! Quick Question." with dissolve
Jason "Gonna miss me once I'm off to college?"

"(As annoying as that question was, I knew I had to give an answer so he could leave.)"

menu:
    with dissolve
    "Yeah surrreee I'll miss you SO much ...":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump choices1_a

    "no. but if you leave in 5 seconds, maybe ...":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump choices1_b

label choices1_a:
    "Yeah surrreee I'll miss you SOOooOO much that I'll follow you. I'm sure you already knew that right? (rolls eyes internally)"
    show jason smug gif
    Jason "I knew that, aha." 

    "(Well, here goes his ego boosting up to Mars.)"
    
    jump choices1_common

label choices1_b:
    "No. But if you leave in 5 seconds, maybe I'll consider it. You wanna take that chance?" 

    show jason mad gif
    play sound "audio/ショックな時のピアノの不協和音_shock.mp3" volume 0.3
    Jason "!!!" with Shake((20, 20, 20, 20), 0.5, dist=10)
    pause 0.3

    "(Ouch. I think His ego just crashed down.)"

    show jason mad gif
    Jason "..."
    Jason "Naaaah. You're lying."

    "Yeah sure..."

    jump choices1_common

label choices1_common:
    show jason smug gif
    Jason "You're not really enjoying the party, are you?"
    hide jason smug gif

    show jason happy gif
    Jason "Now that I'm here, we can have some REAL fun."

"I ignore Josh as I look out for a certain someone."
"And then I see him..."
hide jason happy gif
with dissolve

show mikel mc sad away gif ## replace with an art splash of younger middle school mikel?
with dissolve
"There he was ... Mikel, my old best friend since middle school."

show mikel photo gif with dissolve

"He's always been kind and sweet, the best type of friend you could ask for."
"The first time we met in middle school, I thought he was arrogant and too cool for me, but surprisingly, he wanted to be my first friend."
"We stayed close since then and have looked out for each other."

hide mikel photo gif with fade

show mikel sad headdown gif with dissolve
pause 0.9

"I thought he would have fun being surrounded by everyone in this party but he looks sad and alone..." with dissolve
"should I go talk to him?"

menu:
    with dissolve
    "walk over to him":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump continue1_a

    "stay with friends":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending1_a

label continue1_a:
    scene bg party
    with fade

    "(I approach him confidently like any friend does and tap his shoulder)"

    "Hey, enjoying the party?"

    show mikel mc neutral gif
    with dissolve
    "(Mikel looks over to me with a sense of worry in his eyes.)" with dissolve
    hide mikel mc neutral gif

    show mikel happy gif
    Mikel "yeah...!" with hpunch
    Mikel ""
    Mikel "..."
    hide mikel happy

    show mikel mc neutral gif
    Mikel "..."
   
    "(I can tell that's not an honest reply.)"
    "(Mikel is still an idiot to think he can fool me.)"
    "(We've been so close that it's impossible to lie to each other, we'd know right away.)"
    
    "C'mon Mikel, you can be honest with me."
    

    hide mikel mc neutral gif
    show mikel happy armscrossed away gif
    Mikel "Ha...you know me so well..."

    show mikel mc sad away gif
    Mikel "Hmm..."
    
    "(Huh?)"

    "(I look over to where Mikel was staring at...He seems to be distracted with something.)"

    "(I guess he's looking at...)"

label threechoices:
    scene black
    hide mikel
    show screen scene_with_camera
    with dissolve

    call screen choicesButton
    with dissolve

menu: ##Backup if screen buttons are not working
    with dissolve 

    "The shy girl":
        jump ending2

        hover_sound "audio/hit_sfx/paper-245786.mp3"
        activate_sound "audio/hit_sfx/paper-slide-89980.mp3"

    "Crumpled piece of paper":
        jump ending3

    "a group laughing":
        jump ending4

label ending2:

    show shygirlstill gif 
    with fade

    "Are you looking at that girl over there?"

    show mikel neutral gif at left
    with dissolve
    
    Mikel "O-Oh...Yeah." with dissolve

    Mikel "..."
    hide mikel neutral gif at left

    show mikel sad away gif at left

    Mikel "She just looks alone over there..."

    "Do you know her?"
    hide mikel sad away gif at left

    show mikel sad headdown gif at left

    Mikel "Well, no-...uh...yes?"
    hide mikel sad headdown gif at left

    show mikel neutral gif at left
    Mikel "She just did something that surprised me today."

    "Yeah? Like what?"
    hide mikel neutral gif

    show mikel happy armscrossed gif at left
    Mikel "She may or may not have written me a letter..."
    hide mikel happy armscrossed gif

    show mikel happy gif at left

    Mikel "...with a confession."

    "(Mikel looks a little smug like he's testing me)"

    "(I have a funny feeling in my stomach hearing that but I ignore it.)"

    "Hey! Good for you lucky guy!"

    "Did you talk to her yet?"
    
    hide mikel happy gif

    show mikel happy armscrossed gif at left
    Mikel "No, not yet. I don't know if I should."
    hide mikel happy armscrossed gif

    show mikel neutral gif at left
    Mikel "What do you think?"
    hide mikel neutral gif 

    show mikel mc neutral gif at left


menu:
    with dissolve
    "Yeah, talk to her...":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending3_b
        
        
    
    "No, think over it...":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending2_a


label ending2_a:
    "No offense Mikel..."
    "... I know you tend to act spontaneous and all-"
    "-and go with the flow but..."
    "...I think you should think over it."
    "This is someone's feelings you're dealing with."

    show mikel mc neutral gif at left
    hide mikel mc neutral gif

    show mikel neutral gif at left

    Mikel ""
    hide mikel neutral gif 

    show mikel happy armscrossed gif at left 
    with dissolve
    
    Mikel "Oh wow."
    hide mikel happy armscrossed gif 

    show mikel happy gif at left

    Mikel "Okay, yeah. You got me."
    hide mikel happy gif at left

    show mikel happy armscrossed away gif at left 
    
    Mikel "I think I should give it some time and think over it, for sure."
    hide mikel happy armscrossed away gif

    show mikel happy armscrossed gif at left 

    Mikel "In fact, since you know me so well, you know what I'm gonna say next-"

    "You're gonna say="

    "-that you're so bored of this party and music that you wanna step out for a smoke?"

    hide mikel happy gif

    show mikel happy armscrossed gif at left
    "Yup. Right as always."
    hide mikel happy armscrossed gif at left 
    hide shygirlstill gif

    "( Mikel shows a satisfied smirk and nods his head up at me, gesturing us to move... )"

    "( ... We try and slip in between the crowd at the party and walk towards the backdoor. )" 

    stop music fadeout 2.0

    play music "audio/outdoormusic.mp3" volume 2.0 fadein 3.0

    show bg outdoor with fade
    pause 0.5

    "( When we open the door and step into the backyard, the fresh air hits us and the music fades out. )"

    "( Mikel opens the box and pulls out the cigarette. )"

    "( He pulls another one out and passes it to me. )"

    "( We both use my lighter to light up the cigarette... )"

    show mikel outdoor neutral away with dissolve
    
    Mikel "..."

    "( Mikel gazes at the grass and fences ahead and breathes in the smoke for a second.)"

    hide mikel outdoor neutral away 

    show mikel outdoor neutral 

    Mikel "Phew, that party is packed with just sweat and noise."

    Mikel "I'm glad we're out."

    "I thought you like that scene?"

    hide mikel outdoor neutral

    show mikel outdoor sad

    Mikel "Thought I did too..."

    hide mikel outdoor sad

    show mikel outdoor sad away

    Mikel "But the company I have there feels so....tiring ..."

    Mikel "I...."

    hide mikel outdoor sad away

    show mikel outdoor neutral

    Mikel "... would rather be with you alone right now."

    "Oh.."

    "( I try not to focus so hard on how my heart skips a beat from that sentence...)"

    "Me too. My friends were gonna make me have another shot, I'm glad I ran with you here."

    "I almost escaped the dreadful vomit session that comes with it, aha."

    Mikel "So I saved you is what you're saying. heh."

    "When you word it that way, yeah!"
    
    "Thanks for saving me."
    hide mikel outdoor neutral

    show mikel outdoor neutral away

    Mikel "Pleasures all mine."

    "(I stare at Mikel and notice his furrowed brows...)"
    
    "(He's still in deep thought about something...)"

    "You're thinking about pooping?"

    hide mikel outdoor neutral away

    show mikel outdoor shock

    "What??"

    Mikel "No! I did that- before the- Urgh I mean-"

    hide mikel outdoor shock
    show mikel outdoor sad away

    Mikel "..."
    hide mikel outdoor sad away
    show mikel outdoor sad

    Mikel "I'm just thinking about the friends we have..."


    Mikel "I spent all my parties and fun with those people but I know..."

    hide mikel outdoor sad

    show mikel outdoor sad away

    Mikel "... We're not gonna be so close once we drift apart to different colleges..."
    
    Mikel "and I..."

    hide mikel outdoor sad away

    show mikel outdoor sad

    Mikel "And...I wish ..."
    
    Mikel "I got to spend more time with you instead."

    Mikel "And I feel sorry that I didn't."

    "Oh wow. I ..."
    
    "... I was thinking the same thing actually."

    "I know we were busy with college applications and stuff so I can't blame you."

    hide mikel outdoor sad

    show mikel outdoor neutral    
    Mikel "I'm still glad we're here talking..."

    "Me too."

    hide mikel outdoor neutral with fade

    "(We both smoke the last bit of the cigarette and stare out in the sky.)"

    "(the crowd at the party was slowly dying down since it was 2 am.)"

    "(I say my goodbyes to Mikel and grab a cab back home.)"

    jump happyending



label ending3:
    show paper inspect
    with fade
    "(I look at the piece of paper that looks to be crumpled with some writing in it)"
    "(before I can inspect it further, I try to ask Mikel about it.)"
    "Were you looking at this?"
    hide paper inspect
    with dissolve

    show mikel mc neutral gif
    with dissolve 
    "(Mikel softens his eyes and sighs a bit.)"
    Mikel "..."
    pause 0.9

    show mikel neutral gif
    Mikel "I found it in my locker actually and didn't think much of it."
    Mikel "...till I was at the party."
    Mikel "I realised I stuffed it in my jacket and opened it then."
    
    "what was in it?"

    hide mikel neutral gif

    show mikel sad away gif
    Mikel "...It was a love letter."
    "(???)" ## Add surprised SFX ?
    " to you??"
    hide mikel sad away gif

    show mikel neutral gif
    Mikel "yeah."

    "who wrote it?"
    hide mikel neutral gif

    show mikel sad away gif
    Mikel "that girl over there-"
    hide mikel sad away gif 
    with fade

    show shygirlstill gif with dissolve

    "(I look over to a girl standing in the corner alone. She's drinking quietly and nodding to the music meekly)" with dissolve
    "I...don't know her." 
    
    show mikel neutral gif at left
    with dissolve

    Mikel "neither did I till today."
    Mikel "Apparently she knew me-"
    hide mikel neutral gif
    
    
    show mikel sad away gif at left    
    Mikel "-more like had a crush on me since the beginning of the year."
    Mikel "She wrote in the letter asking if I was willing to give her a chance."
    "Well, did you give her an answer?"
    hide mikel sad away gif

    show mikel neutral gif at left
    Mikel "Not yet. I don't know what to say."

    Mikel "What do you think?"

    "well I..."

menu:
    with dissolve

    "Think over it...":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending3_a
    
    "talk to her...":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending3_b


    
label ending3_a: ## IGNORE HER
    show mikel neutral gif at left
    hide shygirlstill gif
    with dissolve

    "well...you can think about it later and respond back"
    "And it looks like she left too."
    hide mikel neutral gif

    show mikel sad away gif
    with dissolve
    Mikel "Oh..yeah you're right."
    hide mikel sad away gif

    show mikel mc sad away gif
    "Mikel stood there in deep thought."
    "I can't tell what he's thinking but it looks like its been on his mind for a while."
    "before I can ask him about that, he breaks the silence."
    hide mikel mc sad away gif

    show mikel happy armscrossed away gif
    Mikel "well the funny thing is..."

    "what?"
    hide mikel happy armscrossed away gif

    show mikel happy armscrossed gif
    Mikel "..."
    Mikel "well...I..."

    "yes...?"

    Mikel "I...uh... maybe thought..."
    hide mikel happy armscrossed gif

    show mikel happy armscrossed away gif
    Mikel "that you wrote it... The letter to me."
    hide mikel happy armscrossed away gif

    show mikel mc happy armscrossed gif

    "oh okay."

    "............"

    "Wait- WHAT?" with Shake((5, 2, 4, 0), 0.5, dist=5)

    hide mikel mc happy armscrossed gif

    show mikel happy armscrossed gif
    Mikel "yeah..."

    "uh...I mean...- Well I-"
    hide mikel happy armscrossed gif

    show mikel happy gif
    Mikel "forget about it. I just thought the handwriting looked like yours, that's all. Aha."

    "Oh okay, aha."
    
    "I mean I wouldn't pull a prank like that on you anyways."

    hide mikel happy gif

    show mikel happy armscrossed away gif

    Mikel "A prank on me...yeah..."

    Mikel "Aha....."
    "uhh... (I didn't mean it to sound that way.)"
    "I mean...."
    "did you want it...to be me..?"
    hide mikel happy armscrossed away gif

    show mikel neutral gif
    Mikel "would it sound crazy to say if I did?"

    "No- I-"

    "(before I could continue I feel a pair of arms around me, giving me a tight hug.)"
    "(It's one of my friends )"
    Friend "HEYYY SO YOU'RE HEREE ! ! ! !" with vpunch

    Friend "C'MON LET'S DANCE !!!!"

    "(My friend pulls me by her side and we rush into the crowd...)" with hpunch

    hide mikel neutral gif
    with dissolve
    
    show mikel happy armscrossed gif
    with dissolve
    "(I look back at Mikel smiling gently with him mouthing something" 
    hide mikel happy armscrossed gif
    with dissolve

    show mikel happy gif 
    with dissolve 

    "\"have fun!\"" with dissolve

    hide mikel happy gif 
    with dissolve

    "(The hours went by with us dancing and drinking some more)"

    "(But the conversation with Mikel didn't leave my mind for a second.)"

    "(the party continued on till 2 am and it was starting to get tiring)"

    "(So my friends and I decide to catch a cab and go back home.)"
    hide scene bg party
    stop music fadeout 1.0

    jump happyending


label ending3_b: ## TALK TO HER
    show shygirlstill gif
    show mikel mc neutral gif at left
    "i Think you should talk to her. Give her a chance."
    hide mikel mc neutral gif

    show mikel neutral gif at left
    Mikel "You think so?"

    "yeah."

    show mikel happy armscrossed away gif at left
    Mikel "I guess I'll do that! I don't think I should avoid the situation. She might be a nice girl."

    "Well anyone would be lucky to talk to you."
    hide mikel happy armscrossed away gif

    show mikel happy gif at left
    Mikel "Heh. Thanks."
    hide mikel happy gif

    show mikel mc happy armscrossed gif at left

    "(Even when I said yes, some part of me didn't want to ... )"
    
    "( ... I wanted him to stay with me longer but it felt selfish.)"

    "(And I was too scared to confess, I didn't want him to be robbed of something I could never bring myself to do.)"
    hide mikel mc happy armscrossed gif

    show mikel happy armscrossed gif at left

    Mikel "I guess I'll see you later then."

    hide mikel happy armscrossed gifS
    with dissolve

    hide shygirlstill gif

    show mandshygirl gif
    with dissolve

    "(As Mikel walks off towards the girl and dances with her I felt my heart sting)" 
    hide mandshygirl gif
    with dissolve

    "(Yeah...Maybe some other time...)"
    "(I continue on and party with my friends)"
    "(we laugh and drink some more till one of my friend ends up puking in the kitchen.)"
    "(it pisses off the guy who's hosting the party.)"
    "(We look at eachother and decide it's better if we all just leave.)"
    hide scene bg party
    stop music fadeout 2.0

    show bg black with fade
    "(we grab our stuff and walk out, taking the cab back home.)"

    "END."

    return

label ending4:

    show grouplaughing_idle:
        xalign 0.5
        yalign 0.5

    
    "Wait, that's Rohan, Clair and Alex. That's your crew right?" with dissolve

    hide grouplaughing_idle

    show mikel mc sad away gif with dissolve

    Mikel "..." with dissolve

    "(Mikel doesn't look back and keeps his back facing towards them.)"

    show mikel neutral gif

    Mikel "Yeah, they're there..."
    hide mikel neutral gif

    show mikel mc neutral gif

    "Guess you went ahead to get their drinks as they're waiting for you?"
    hide mikel mc neutral gif

    show mikel happy gif

    Mikel "Hah! No, they're pretty drunk already as you can see."

    "Oh yeah, I see it ..."

    "... Rohan's famous sleezy drunk smile says everything."
    hide mikel happy gif

    show mikel happy armscrossed away gif

    "(Mikel grins a little thinking of that image but, he's still silent.)"

    "Hey Mikel..."

    hide mikel happy armscrossed away gif

    show mikel neutral gif

    Mikel "Yeah?"
    
    "You're alright....right?"
    hide mikel neutral gif

    show mikel happy gif

    Mikel "....Yeah, of course! I was just on my way taking a breather."
    hide mikel happy gif

    show mikel happy armscrossed away gif

    Mikel "I think I need a break from partying too hard."

    "Oh yeah, I feel that..."
    hide mikel happy armscrossed away gif

    show mikel mc happy armscrossed gif

    "(I could still feel that Mikel is feeling down and is not saying much...)"

    "(something must be really on his mind...maybe he doesn't want to be here...)"

    "You know what Mikel, let's ditch this party and..."

menu:
    "let's drive back to my place.":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending4_a ## Car crash ending

    "let's step outside for a smoke.":
        play sound "audio/hit_sfx/paper-245786.mp3"
        jump ending4_b ## Happy ending

label ending4_a:

    "You know what, F this party and let's drive back to my place!!"

    hide mikel mc happy armscrossed gif

    show mikel neutral gif

    "(Mikel is suprised by my sudden suggestion but doesn't reject it.)"

    Mikel "Right now?"

    "Yeah!! C'mon. Let's relive our memories of middle school!"

    "We go back to my place and play the same old board games we used to play as kids."
    
    "I'll drive Alex's car since you're holding on to his car key as usual."
    hide mikel neutral gif

    show mikel happy armscrossed away gif

    Mikel "Huh, yeah. Old habit from freshman year I guess."
    hide mikel happy armscrossed away gif

    show mikel happy armscrossed gif
    Mikel "Alex always needed me to hold on to his keys because he kept losing them."

    "Well this bascially means that he's letting you borrow his car, riighhhtt?"

    "(I grin wide at Mikel the same old way I did back then when we were kids.)"

    "(Mikel couldn't say no to that smile.)"
    hide mikel happy armscrossed gif

    show mikel happy gif

    Mikel "You know what, I like that idea. I wanna see you attempt to drive back home in this state. It'll be fun."

    "YEAH!" with Shake((5, 5, 5, 5), 0.5, dist=10)

    Mikel "YEAH! AHA!" with Shake((5, 5, 5, 5), 0.5, dist=10)

    hide mikel happy gif with dissolve

    "(We try and slip inbetween the crowd at the party... )"  with dissolve

    "(.... The crowd felt tighter the more we tried to move past but we eventually reach the backdoor.)"

    show bg black with dissolve

    stop music fadeout 2.0
    show bg carpark
    pause 2.0

    "(We step out and take in the fresh air. Mikel eyes Alex's car parked in the corner.)" with dissolve

    "(We sit inside the car and I grip the steering wheel while twisiting the keys to start the car.)"

    "(Mikel holds back his smile but I can tell he's excited)"

    "Ready?"

    Mikel "Ready."

    play sound "audio/cardrive.mp3"

    show bg cardrive with dissolve

    "( I drive as fast as I can on the road and I hear Mikel scream with laughter. )" with dissolve
    "( The air felt colder and the harsh breeze hit Mikel's face as he looks out the window... )"
    "( The night finally started feeling right... I hold on the wheel tighter, ready to drive at full force till-- )"

    "(--Suddenly I hear the wheel puncture and-- )"

    show bg black

    play sound "audio/carcrash.mp3"

    "" with Shake((10, 10, 10, 10), 0.5, dist=30)

    "END."

    return


label ending4_b:
    "Actually, I need a smoke break. Wanna step out with me?"

    "C'mon, I know you're bored of this party."

    show mikel neutral gif with dissolve
    pause 3.0

    hide mikel neutral gif

    show mikel happy armscrossed

    Mikel "Wow, You've read my mind, let's go."

    hide mikel happy armscrossed gif 

    show mikel mc happy armscrossed gif

    "( Mikel shows a satisfied smirk and nods his head up at me, gesturing us to move... )"
    hide mikel mc happy armscrossed gif with dissolve

    "(We try and slip in between the crowd at the party... )"  with dissolve

    "(.... The crowd felt tighter the more we tried to move past but we eventually reach the backdoor.)"

    stop music fadeout 2.0

    play music "audio/outdoormusic.mp3" volume 2.0 fadein 3.0

    show bg outdoor with fade
    pause 0.5

    "( When we open the door and step into the backyard, the fresh air hits us and the music fades out. )"

    "( Mikel opens the box and pulls out the cigarette. )"

    "( He pulls another one out and passes it to me. )"

    "( We both use my lighter to light up the cigarette... )"

    show mikel outdoor neutral away with dissolve
    
    Mikel "..."

    "( Mikel gazes at the grass and fences ahead and breathes in the smoke for a second.)"

    hide mikel outdoor neutral away 

    show mikel outdoor neutral 

    Mikel "Phew, that party is packed with just sweat and noise."

    Mikel "I'm glad we're out."

    "I thought you like that scene?"

    hide mikel outdoor neutral

    show mikel outdoor sad

    Mikel "Thought I did too..."

    hide mikel outdoor sad

    show mikel outdoor sad away

    Mikel "But the company I have there feels so....tiring ..."

    Mikel "I...."

    hide mikel outdoor sad away

    show mikel outdoor neutral

    Mikel "... would rather be with you alone right now."

    "Oh.."

    "( I try not to focus so hard on how my heart skips a beat from that sentence...)"

    "Me too. My friends were gonna make me have another shot, I'm glad I ran with you here."

    "I almost escaped the dreadful vomit session that comes with it, aha."

    Mikel "So I saved you is what you're saying. heh."

    "When you word it that way, yeah!"
    
    "Thanks for saving me."
    hide mikel outdoor neutral

    show mikel outdoor neutral away

    Mikel "Pleasures all mine."

    "(I stare at Mikel and notice his furrowed brows...)"
    
    "(He's still in deep thought about something...)"

    "You're thinking about pooping?"

    hide mikel outdoor neutral away

    show mikel outdoor shock

    "What??"

    Mikel "No! I did that- before the- Urgh I mean-"

    hide mikel outdoor shock
    show mikel outdoor sad away

    Mikel "..."
    hide mikel outdoor sad away
    show mikel outdoor sad

    Mikel "I'm just thinking about the friends we have..."


    Mikel "I spent all my parties and fun with those people but I know..."

    hide mikel outdoor sad

    show mikel outdoor sad away

    Mikel "... We're not gonna be so close once we drift apart to different colleges..."
    
    Mikel "and I..."

    hide mikel outdoor sad away

    show mikel outdoor sad

    Mikel "And...I wish ..."
    
    Mikel "I got to spend more time with you instead."

    Mikel "And I feel sorry that I didn't."

    "Oh wow. I ..."
    
    "... I was thinking the same thing actually."

    "I know we were busy with college applications and stuff so I can't blame you."

    hide mikel outdoor sad

    show mikel outdoor neutral    
    Mikel "I'm still glad we're here talking..."

    "Me too."

    hide mikel outdoor neutral with fade

    "(We both smoke the last bit of the cigarette and stare out in the sky.)"

    "(the crowd at the party was slowly dying down since it was 2 am.)"

    "(I say my goodbyes to Mikel and grab a cab back home.)"

    jump happyending


label ending1_a:
    hide mikel mc sad lookaway gif with dissolve

    "(Yeah...Maybe some other time...)"
    "(I continue on and party with my friends)"
    "(we laugh and drink some more till one of my friend ends up puking in the kitchen.)"
    "(it pisses off the guy who's hosting the party.)"
    "(We look at each other and decide it's better if we all just leave.)"
    hide scene bg party
    stop music fadeout 2.0

    show bg black with fade
    "(we grab our stuff and walk out, taking the cab back home.)"

    "END."

    return

label happyending:
    stop music fadeout 2.0

    show bg bedroom with fade   
    pause 5.0

    play music "audio/evening-sound-effect-in-village-348670.mp3" fadein 2.0 volume 0.5

    "(I was finally back home as tired as ever...)"

    "(I was ready to hit the bed but the conversation just couldn't leave my mind.)"

    "(I always wanted to confess my feelings but I was too scared to do it...)"

    "(....)"

    "I think...I should do it."

    "(I grab a paper and a pen from my desk and sit on the chair.)"

    "(regaining my energy back, I put in all my feelings into writing...)"

    "(... from the day I met him to the moment I realised I felt more than a friend would.)"

    "(After writing everything down, I slipped the letter in the envelope and stamped it with his address written.)"

    "(The only thing is that, I couldn't confess now...I still wasn't sure how he felt about me...)"

    "(And we're moving apart after graduating school and entering into different colleges...)"

    "(I couldn't tell him now...but he will know in the future when its right...)"

    

    stop music fadeout 1.0
    show bg happyend with fade
    pause 5.0

    play music "audio/cinematic-piano-loop-sentimental-melancholy-379037.mp3" fadein 4.0
    "5 YEARS LATER..."


    unknown "\"....?\""

    show happyend photo 1 gif with dissolve

    unknown "\"What's this?\"" 

    show happyend photo 2 gif with dissolve

    Mikel "..." ## Mikel with the letter art photo

    Mikel "Ha...I knew it...you idiot." ## slight change of mikel's expression with the same art photo

    Mikel "Ha...aha ha..." ## Mikel's hand on phone photo art

    show happyend photo 3 gif with dissolve

    Mikel "You better pick up now." ##Same as above

    stop music fadeout 2.0

    hide happyend 3 gif

    show bg black with dissolve

    "END." with fade
