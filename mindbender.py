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
class mindbender():
    def __init__(self, macropad, tones):
        # shows how the keys affect others
        self.tones = tones
        self.color = 0xff0000
        self.macropad = macropad
        self.gameMode ="select"
        self.puzzle=[]
        self.tries = 0
        self.clear = [
            0xf400fd,0xd516ed,0xb71edc,
        0x9a21cb,0x7f21b8,0x651fa5,
        0x4c1c91,0x34177d,0x1d1268,
        0xff9900,0x000,0x00ff00]
        self.tempo = 150 # bpm
        self.player = []
        print ("Mindbender is initialized")
        #self.new_game()

    def new_game(self):
        print ("new Mindbender game")
        self.puzzle.clear()
        self.player.clear()
        self.tries = 0
        self.gameMode ="select"
        self.macropad.pixels.fill((0,0,0))
        # run dots through every active button
        for x in range (9):
            self.macropad.pixels[x]=0x000099
            time.sleep(0.1)
            self.macropad.pixels[x]=self.clear[x]
         
        
    def start_game(self, length):
        print ("player has selected", length)
        self.gameMode ="playing"
        self.macropad.play_tone(self.tones[0], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        self.macropad.play_tone(self.tones[4], 0.5)
        #clear and light up new/same buttons
        self.macropad.pixels.fill((0,0,0))
        time.sleep(0.5)
        for x in range(length):
            rando = randint(0, 8)
            self.puzzle.append(rando)
        
        print ("Merlin has chosen",self.puzzle)
        self.clear_board()
         
    def evaluate(self):
        #increment the try counter
        self.tries = self.tries+1
        #let's get ready
        self.macropad.pixels.fill((0,0,0))
        print ("evaluating",self.player,"against",self.puzzle)
        # red light for so wrong
        # yellow for correct digit, wrong place
        # green for correct
        green = 0
        yellow = 0
        red = 0
        tracker = self.puzzle.copy()
        #evaluate...somehow
        # first check for win
        if self.puzzle == self.player:
            self.winner()
        else:
            #check for correct in correct place
            print ("checking for matches")
            for x in range (len(self.player)):
                print ("player",self.player[x],", puzzle",tracker[x])
                if self.player[x]==tracker[x]:
                    green = green +1
                    tracker[x]=-1
                    self.player[x]=-1
                    print("match! green")
            #now check the leftovers
            print ("checking leftovers")
            for x in range (len(tracker)):
                if tracker[x]>=0:
                    print ("looking for",tracker[x])
                    try:
                        pos = self.player.index(tracker[x])
                        yellow = yellow+1
                        print(tracker[x],":yellow")
                        tracker[x]=-1
                        self.player[x]=-1
                    except ValueError:
                        red = red+1
                        print(tracker[x],":red")
                    

            print ("score is",green,yellow,red)
            #show results
            for x in range (green):
                self.macropad.pixels[x]=0x146401
            for x in range (green,green+yellow):
                self.macropad.pixels[x]=0x645501
            for x in range (green+yellow,green+yellow+red):
                self.macropad.pixels[x]=0x640101
            #pause?
            #how to continue?
            self.gameMode ="evaluated"
            self.player.clear()
            #play again button
            self.macropad.pixels[10]=0x7f21b8


    def same_game(self):
        # show a square for fun
        print ("restart game")
        self.macropad.pixels.fill((0,0,0))
        self.macropad.play_tone(self.tones[4], 0.5)
        self.macropad.play_tone(self.tones[2], 0.5)
        #time.sleep(0.5)
        self.macropad.pixels.fill((0,0,0))
        self.player.clear()
        self.score=0
        self.gameMode ="playing"
        self.clear_board()
        #now play the puzzle
        #self.play_puzzle()
        

    
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
        print ("only took you",self.tries,"tries")
        time.sleep(0.5)
        self.macropad.pixels.fill((0,0,0))
        light_count = 9 
        tens = 0
        for x in range (self.tries):
        #for x in range (32):
            if x==light_count:
                self.clear_board()
                #print ("clear")
                self.macropad.pixels[9]=0x000099
                #print (x,"blue")
                time.sleep(0.2)
                tens = tens+1
                #self.macropad.pixels[10]=0x0a0014
            elif x==(light_count)*2+1:
                self.clear_board()
                #print ("clear")
                self.macropad.pixels[9]=0x000099
                self.macropad.pixels[10]=0x000099
                #print (x,"aka 10 blue")
                time.sleep(0.2)
                tens = tens+1
                #self.macropad.pixels[10]=0x0a0014
            elif x==(light_count)*3+2:
                self.clear_board()
                #print ("clear")
                self.macropad.pixels[9]=0x0a0014
                self.macropad.pixels[10]=0x000099
                #print (x,"aka 9 blurple")
                time.sleep(0.2)
                tens = tens+1
                #self.macropad.pixels[10]=0x0a0014
            elif x==(light_count)*4+3:
                self.clear_board()
                #print ("clear")
                self.macropad.pixels[9]=0x0a0014
                self.macropad.pixels[10]=0x0a0014
                #print (x,"aka 10 plurple")
                time.sleep(0.2)
                tens = tens+1
                #self.macropad.pixels[10]=0x0a0014
            else:
                self.macropad.pixels[(x-tens)%light_count]=0x000099
                #print ((x-tens)%light_count,"blue")
                time.sleep(0.2)
                self.macropad.pixels[(x-tens)%light_count]=0x0a0014
                #print ((x-tens)%light_count,"blurple")
        for x in range(9,12):
            self.macropad.pixels[x]=self.clear[x]      
        self.gameMode ="ended"
    
    def clear_board(self):
        # show the results
        for x in range (len(self.clear)):
            self.macropad.pixels[x] = self.clear[x]
        
        # make boop
        #self.macropad.play_tone(self.tones[7], 0.5)
        
        

    def button(self,key):
        #check mode
        if self.gameMode =="select":
            if (key < 9):
                self.macropad.play_tone(self.tones[key], 0.2)
                self.macropad.pixels[key]=0x009900
                self.start_game(key+1)
            else: 
                #ignore
                pass
        elif self.gameMode =="evaluated":
            if key == 10:
                #do it again
                self.gameMode="playing"
                self.clear_board()
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
                self.macropad.pixels[key]=0x000099
                self.macropad.play_tone(self.tones[key], 0.2) 

                self.player.append(key)
                print ("player",self.player)
                if len(self.player) == len(self.puzzle):
                    #game is done
                    #evaluate
                    self.evaluate()
                
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
