# 0-8 used to draw a square
# extra buttons NEW GAME, SAME GAME

# goal is [1,1,1,1,0,1,1,1,1]
# 0 1 2 
# 3 4 5
# 6 7 8
# corner buttons affect the three adjacent lights
# edge buttons affect the two corners on that edge
# center button affects all edge buttons

# 0 flips 0,1,3,4
# 1: 0,1,2
# 2: 1,2,4,5
# 3: 0,3,6
# 4: 1,3,4,5,7
# 5: 2,5,8
# 6: 3,4,6,7
# 7: 6,7,8
# 8: 4,5,6,7

from random import randint
import time

# init
# flash the square
# choose a random config
class magic_square():
    def __init__(self, macropad, tones):
        # shows how the kets affect others
        self.keys = [
            0b110110000,
            0b111000000,
            0b011011000,
            0b100100100,
            0b010111010,
            0b001001001,
            0b000110110,
            0b000000111,
            0b000011011]
        self.state=0b0
        self.start = 0b0
        self.tones = tones
        self.color = 0xff0000
        self.macropad = macropad
        print ("Magic Square is initialized")
        #self.new_game()

    def new_game(self):
        print ("new Magic Square game")
        # show a square for fun
        self.macropad.pixels.fill((0,0,0))
        self.color = 0x0009ff
        self.state = 0b111101111
        self.show_leds()
        self.macropad.play_tone(self.tones[0], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.macropad.play_tone(self.tones[4], 0.5)
        self.color = 0xff0000
        #generate a new matrix
        for x in range(8):
            self.state=bin(randint(0, 511))
        if (self.state == 0b111101111):
            self.state = self.state + 1
        print ("starting",self.state)
        self.start = self.state
        self.show_leds()
        #need to change labels
        self.macropad.pixels[9]=0xff9900
        self.macropad.pixels[11]=0x00ff00
        
    
    def same_game(self):
        # show a square for fun
        self.color = 0xff9900
        self.state = 0b111101111
        self.show_leds()
        self.macropad.play_tone(self.tones[4], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.color = 0xff0000
        self.state = self.start
        self.show_leds()

    def show_off(self):
        # show a square for fun
        self.color = 0x0009ff
        self.state = 0b111101111
        self.show_leds()
        self.macropad.play_tone(self.tones[0], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.macropad.play_tone(self.tones[4], 0.5)
        self.color = 0xff0000
        
        #time.sleep(1)
    
    def winner(self):
        # do a winning thing
        self.color = 0x00ff00
        self.show_leds()
        self.macropad.play_tone(self.tones[0], 0.2)
        self.macropad.play_tone(self.tones[2], 0.2)
        self.macropad.play_tone(self.tones[4], 0.2)
        self.macropad.play_tone(self.tones[6], 0.2)
        self.macropad.play_tone(self.tones[4], 0.2)
        self.macropad.play_tone(self.tones[6], 0.5)
        print ("you are a weiner")
        
    def bits(self,n):
        #print (bin(int(n)))

        arr = [int(x) for x in bin(int(n))[2:]]
        for x in range (0,(9-len(arr))):
           arr.insert(0,0)
        print (arr)
        return arr

    def show_leds(self):
        # show the results
        matrix = self.bits(self.state)
        #print (matrix)
        for x in range (len(matrix)):
            if matrix[x]:
                self.macropad.pixels[x] = self.color
            else:
                self.macropad.pixels[x] = 0x000000

        # make boop
        #self.macropad.play_tone(self.tones[7], 0.5)
        

    def button(self,key):
        if key==9:
            self.same_game()
        elif key ==11:
            self.new_game()
        elif key <9:
            #print ("is",bin(self.state),", affects",bin(self.keys[key]))
            self.macropad.play_tone(self.tones[key], 0.2)
            self.state = int(self.state)^int(self.keys[key])
            if (self.state == 0b111101111):
                self.winner()
            else:
                self.show_leds()
        else: # it's another button, weirdo
            pass

    def encoderChange(self,newPosition, oldPosition):
        pass

# keypress
# take the key number, pull the modifier array, apply
# check for win
# show result
