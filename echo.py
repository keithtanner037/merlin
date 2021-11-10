#echo
# 
# extra buttons NEW GAME, SAME GAME

# new game: Merlin asks for a length
# generate random sequence of that length
# play it
# user copies it
# beep on correct, buzz on error
# show score or make win noise


from random import randint
import time

# init
# flash the square
# choose a random config
class echo():
    def __init__(self, macropad, tones):
        # shows how the keys affect others
        self.tones = tones
        self.color = 0xff0000
        self.macropad = macropad
        self.gameMode ="select"
        self.puzzle=[]
        self.clear = [
            0xf400fd,0xd516ed,0xb71edc,
        0x9a21cb,0x7f21b8,0x651fa5,
        0x4c1c91,0x34177d,0x1d1268,
        0xff9900,0x000,0x00ff00]
        self.tempo = 150 # bpm
        self.player = []
        print ("Echo is initialized")
        #self.new_game()

    def new_game(self):
        print ("new Echo game")
        self.puzzle.clear()
        self.player.clear()
        self.gameMode ="select"
        self.macropad.pixels.fill((0,0,0))
        # run dots through every active button
        for x in range (9):
            self.macropad.pixels[x]=0x000099
            time.sleep(0.1)
            self.macropad.pixels[x]=self.clear[x]
         
        
    def start_game(self, length):
        print ("player has selected", length)
        self.macropad.play_tone(self.tones[0], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.macropad.play_tone(self.tones[4], 0.5)
        #clear and light up new/same buttons
        self.macropad.pixels.fill((0,0,0))
        time.sleep(0.5)
        for x in range(length):
            self.puzzle.append(randint(0, 8))
        self.play_puzzle()
        
        
        #self.macropad.pixels[9]=0xff9900
        #self.macropad.pixels[11]=0x00ff00
    def play_puzzle(self):
        delay = 60/self.tempo
        for x in self.puzzle:
            self.macropad.pixels[x]=0x0a0014
            self.macropad.play_tone(self.tones[x], delay)
            self.macropad.pixels[x]=0x000000
            time.sleep(0.05)
        self.clear_board()
        self.gameMode ="playing"
        
    def end_game(self):
        self.gameMode ="ended"
        self.clear_board()
        print ("END GAME OF ECHO")
        score = 0
        # compare the two arrays
        for x in range (len(self.puzzle)):
            if self.puzzle[x]==self.player[x]:
                score = score +1
        
        if score == len(self.puzzle):
            # we have a weiner
            self.winner()
        else:
            # you are loser
            for x in range (score):
                self.macropad.pixels[x]=0x009900
            for x in range (score,len(self.puzzle)):
                self.macropad.pixels[x]=0x990000
        
        # give score
        # wait
        


    def same_game(self):
        # show a square for fun
        self.gameMode ="playing"
        self.clear_board()
        self.macropad.play_tone(self.tones[4], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.macropad.pixels.fill((0,0,0))
        time.sleep(0.5)
        self.player.clear()
        #now play the puzzle
        self.play_puzzle()
        

    
    def winner(self):
        # do a winning thing
        self.macropad.pixels.fill((0,200,0))
        self.macropad.play_tone(self.tones[0], 0.2)
        self.macropad.play_tone(self.tones[2], 0.2)
        self.macropad.play_tone(self.tones[4], 0.2)
        self.macropad.play_tone(self.tones[6], 0.2)
        self.macropad.play_tone(self.tones[4], 0.2)
        self.macropad.play_tone(self.tones[6], 0.5)
        print ("you are a weiner")
        self.clear_board()
        
    
    def clear_board(self):
        # show the results
        for x in range (len(self.clear)):
            self.macropad.pixels[x] = self.clear[x]
        
        # make boop
        #self.macropad.play_tone(self.tones[7], 0.5)
        

    def button(self,key):
        #check to see if we're in selectionMode
        if self.gameMode =="select":
            if (key < 9):
                self.macropad.play_tone(self.tones[key], 0.2)
                self.macropad.pixels[key]=0x009900
                self.selectionMode = False
                self.start_game(key+1)
            else: 
                #ignore
                pass
        elif self.gameMode=="playing":
            if key==9:
                self.same_game()
            elif key ==11:
                self.new_game()
            elif key <9:
                #print ("is",bin(self.state),", affects",bin(self.keys[key]))
                #do the game thing
                
                self.clear_board()
                if key == self.puzzle[len(self.player)]:
                    #correct
                    self.macropad.pixels[key]=0x000099
                    self.macropad.play_tone(self.tones[key], 0.2)
                    
                else:
                    self.macropad.pixels[key]=0x990000
                    self.macropad.play_tone(100, 0.7)
                    
                self.player.append(key)

                if len(self.player) == len(self.puzzle):
                    #game is done
                    #evaluate
                    self.end_game()
                #self.state = int(self.state)^int(self.keys[key])
                #if (self.state == 0b111101111):
                #    self.winner()
                #else:
                #    self.show_leds()
                
            else: # it's another button, weirdo
                pass
        else:
            #game is over, ignore all but game control buttons
            if key==9:
                self.same_game()
            elif key ==11:
                self.new_game()

    def encoderChange(self,newPosition, oldPosition):
        self.tempo = self.tempo +(newPosition-oldPosition)*5
        print ("new tempo",self.tempo,"bpm")

# keypress
# take the key number, pull the modifier array, apply
# check for win
# show result
