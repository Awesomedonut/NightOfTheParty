screen choicesButton:
    imagebutton:
        xalign 0.1
        yalign 0.5

        hover_sound "audio/hit_sfx/paper-245786.mp3"
        activate_sound "audio/hit_sfx/paper-slide-89980.mp3"

        idle "paper_idle"
        hover "paper_hover"
   
        action Jump("ending3")

    imagebutton:
        xalign 0.8
        yalign 0.5

        idle "girl_idle"
        hover "girl_hover"

        hover_sound "audio/hit_sfx/paper-245786.mp3"
        activate_sound "audio/hit_sfx/paper-slide-89980.mp3"

        action Jump("ending2")

    imagebutton:
        xalign 0.5
        yalign 0.5

        idle "grouplaughing_idle"
        hover "grouplaughing_hover" 

        hover_sound "audio/hit_sfx/paper-245786.mp3"
        activate_sound "audio/hit_sfx/paper-slide-89980.mp3"

        action Jump("ending4")
    

