#music machine
# 

# button 0 is octave below C
# buttons 1-8 are C scale
# button 9 is octave up
# button 10 is rest
# button 11 is "play"
# start over: select with encoder

#this one has custom tones
import time

# init
class music_machine():
    def __init__(self, macropad, tones):
        # shows how the keys affect others
        #provided tones are ignored as they are boring
        self.tones = [196, 262, 294, 330, 350, 392, 440, 494, 523, 587,0]
        self.colors = [
        0xf400fd,0xd516ed,0xb71edc,
        0x9a21cb,0x7f21b8,0x651fa5,
        0x4c1c91,0x34177d,0x1d1268,
        0x010c54,0x000000,0x009900,
        ]
        self.macropad = macropad
        self.sequence=[]
        self.gameMode = "recording"
        self.tempo = 150 # bpm #make this adjustable via encoder??
        print ("Music Machine is initialized")
        #self.new_game()

    def new_game(self):
        print ("new Music Machine game")
        self.sequence.clear()
        self.macropad.pixels.fill((0,0,0))
        # run dots through every active button
        for x in range (len(self.colors)):
            self.macropad.pixels[x]=0x000099
            time.sleep(0.1)
            self.macropad.pixels[x]=self.colors[x]
        #sing a song
        self.macropad.play_tone(self.tones[0], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.macropad.play_tone(self.tones[4], 0.5)
        #clear and light up new/same buttons
        #self.clear_board()
        self.gameMode = "recording"
        

    def play(self):
        self.macropad.pixels.fill((0,0,0))
        self.macropad.pixels[11]=0x000099
        delay = 60/self.tempo
        for x in self.sequence:
            self.macropad.pixels[x]=self.colors[x]
            self.macropad.play_tone(self.tones[x], delay)
            self.macropad.pixels[x]=0x000000

        self.macropad.pixels[11]=0x009900
        
    
    def clear_board(self):
        # show the results
        for x in range (len(self.colors)):
            self.macropad.pixels[x] = self.colors[x]
        
        # make boop
        #self.macropad.play_tone(self.tones[7], 0.5)
        

    def button(self,key):
        #check to see if we're in selectionMode
        if self.gameMode=="recording":
            if key<11:
            #record it
                self.macropad.pixels[key]=0x009900
                self.macropad.play_tone(self.tones[key], 0.2)
                self.macropad.pixels[key]=self.colors[key]
                self.sequence.append(key)
                  
        if key ==11:
            print("playback")
            self.gameMode ="playing"
            self.play()
            
        
        else:
            # someone pushed the encoder button
            pass

    def encoderChange(self,newPosition, oldPosition):
        # use for tempo change??
        self.tempo = self.tempo +(newPosition-oldPosition)*5
        print ("new tempo",self.tempo,"bpm")

# keypress
# take the key number, pull the modifier array, apply
# check for win
# show result
