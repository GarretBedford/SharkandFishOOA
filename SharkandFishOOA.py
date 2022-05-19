"""
Created on Wed Nov 18 14:41:17 2020
This is an object oriented animation in which the user can drag a shark (named
Jaws) through a school of fish. When dragging the shark, the fish will try to avoid
being chowed down and swim away. If the fish gets to close to the mouth of the shark they
get eaten. There is also a custom deepsea background for ambiance. (did you know that
ambiance, and ambience are both correct spellings of the same word, English needs to choose)

Current issues: 
- You need to start dragging the forward facring area of the shark's body
- I can't really see anything else wrong though 

We took inspiration from this example of boids that were created in python:
https://medium.com/better-programming/boids-simulating-birds-flock-behavior-in-python-9fff99375118

ondrag functionality crash fix from the following link (see dragging method for more info):
https://stackoverflow.com/questions/47598953/how-to-make-the-turtle-follow-the-mouse-in-python-3-6
@author: Garret Bedford, Brice Wilson, Luca Damian, Larry Ditton 
"""

import turtle,random,colorsys,math,time

height = 1000
width = 1000

#Starting Variables
sharkx = 0
sharky = 0
mouthx = 60
mouthy = 0

undersea = "undersea.gif"

#=================Panel Setup=============================
turtle.tracer(0)
panel = turtle.Screen()
panel.setup(width, height)
panel.colormode(255)
# panel.bgpic(undersea)
turtle.listen()
        
RUNNING = True  

#==========================CLASSES==========================================
class Fish:
    def __init__(self,x,y,heading,speed,color):
        self.heading = heading
        self.FISH = turtle.Turtle()
        self.FISH.shape('circle')
        self.FISH.shapesize(.25,1,2)
        self.FISHFINS = turtle.Turtle()
        self.FISHFINS.shapesize(1.25,1,2)
        self.FISHFINS.color(color)
        self.FISH.color(color)
        self.FISH.speed = 0
        self.FISHFINS.speed = 0
        self.FISH.penup()
        self.FISHFINS.penup()
        self.FISH.goto(x,y)
        self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
        self.FISH.setheading(self.heading)
        self.FISHFINS.setheading(self.FISH.heading())
        self.speed = speed       
        
    def swimming(self):
        '''Will by default call the align func to choose a new
           direction, and will be interuppted by the ALARM if
           the Shark is within a certain radius'''
        global fishList,sharkx,sharky,height,width
        
        ALARM = sharkdist(self.FISH.xcor(), self.FISH.ycor())
        
        if ALARM > 0:
            
            #   Each Alarm finds the degree away from the shark then runs away at a different speed
            if ALARM == 1:
                
                self.speed = 5
                self.heading = math.degrees(math.atan2((sharky-self.FISH.ycor()),(sharkx-self.FISH.xcor())))+180
                self.FISH.setheading(self.heading)
                self.FISHFINS.setheading(self.FISH.heading())
                self.FISH.forward(self.speed*5)
                self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
                self.heading = self.FISH.heading()
                
            elif ALARM == 2:
                
                self.speed = 7
                self.heading = math.degrees(math.atan2((sharky-self.FISH.ycor()),(sharkx-self.FISH.xcor())))+180
                self.FISH.setheading(self.heading)
                self.FISHFINS.setheading(self.FISH.heading())
                self.FISH.forward(self.speed*5)
                self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
                self.heading = self.FISH.heading()                
                
            elif ALARM == 3:
                
                self.speed = 9
                self.heading = math.degrees(math.atan2((sharky-self.FISH.ycor()),(sharkx-self.FISH.xcor())))+180
                self.FISH.setheading(self.heading)
                self.FISHFINS.setheading(self.FISH.heading())
                self.FISH.forward(self.speed*5)
                self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
                self.heading = self.FISH.heading()

        else:
        
            Move = random.randint(0,1)
            self.speed = 2           

            #   Uses the align finction to make fish schools, also only uses it half the time so it is less computationally hard on the computer
            if Move == 0:
                self.FISH.setheading(self.align())
                self.FISHFINS.setheading(self.FISH.heading())
                self.FISH.forward(self.speed*4)
                self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
                self.heading = self.FISH.heading()
      
            else:
                self.FISH.forward(self.speed*4)
                self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
         
        #   Checks if the fish is off the screen and if it is then puts it back into the playing area
        if self.FISH.xcor() > width/2:
            self.FISH.goto(-width/2,-self.FISH.ycor())
            self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
            self.heading = self.FISH.heading()          
        
        if self.FISH.xcor() < -width/2:
            self.FISH.goto(width/2,-self.FISH.ycor())
            self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
            self.heading = self.FISH.heading()
            
        if self.FISH.ycor() > height/2:
            self.FISH.goto(-self.FISH.xcor(),-height/2)
            self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
            self.heading = self.FISH.heading()
            
        if self.FISH.ycor() < -height/2:
            self.FISH.goto(-self.FISH.xcor(),height/2)
            self.FISHFINS.goto(finslocation(self.FISH.xcor(),self.FISH.ycor(),self.FISH.heading(),7))
            self.heading = self.FISH.heading()
        
    def align(self):
        '''Chooses a new degree direction for the fish based off the rules:
           Alignment, Seperate, and Cohesion, also changes speed for fish'''
        
        allheadings = self.FISH.heading()
        numberfish = 1
        numberclose = 1
        runaway = 0
        runawayV = self.FISH.heading()
        xmass = self.FISH.xcor()
        ymass = self.FISH.ycor()
        
        perception = 100
        bump = 15
        
        Cweight = 3   #   The centering weight, for the average
        Aweight = 1   #   The alignment weight, for the average
        Sweight = 2   #   The seperation weight, for the average
        
        for w in range(len(fishList)):
            distance = math.sqrt(pow(fishList[w].FISH.xcor()-self.FISH.xcor(),2)+(pow(fishList[w].FISH.ycor()-self.FISH.ycor(),2)))

            if 0 < distance < perception:                   #   This is what the fish can see in relation to the other fish
                numberfish += 1                             #   Adds all the fish in perception range
                
                allheadings += fishList[w].FISH.heading()   #   First step of the alignment direction vector
                    
                xmass += fishList[w].FISH.xcor()            #   First step of the centering direction vector
                ymass += fishList[w].FISH.ycor()            #   First step of the centering direction vector
                
                if distance < bump:                         #   This is the area where the seperate direction vector is created
                    runaway += math.degrees(math.atan2((fishList[w].FISH.ycor()-self.FISH.ycor()),(fishList[w].FISH.xcor()-self.FISH.xcor())))+180  #   Adds the direction away from close fish together 
                    numberclose += 1                        #   Adds all the fish in bump range
                
                    self.speed += random.randint(0,2)       #   Modulates speed to help fish get untangled
                
                    if runaway > self.FISH.heading():       #   Adds all the normalized the SEPERATE vectors
                        runawayV += (self.FISH.heading()+90)
                    elif runaway < self.FISH.heading():
                        runawayV += (self.FISH.heading()-90)
                    else:
                        runawayV += self.FISH.heading()

        xmass /= numberfish                                 #   Finds the x-average or middle
        ymass /= numberfish                                 #   Finds the y-average or middle
        
        centerdistance = math.sqrt(pow(xmass-self.FISH.xcor(),2)+(pow(ymass-self.FISH.ycor(),2)))   #   Finds the distance from the fish to the middle
        
        if centerdistance > perception/2:
            self.speed += random.randint(0,2)               #   Modulates speed to help the fish get untangled
        
        centerV = math.degrees(math.atan2((ymass-self.FISH.ycor()),(xmass-self.FISH.xcor())))   #   Finds the COHESION directional vector
        alignmentV = (allheadings/numberfish)

        if centerV > self.FISH.heading() and numberfish > 1:    #   Checks the COHESION vector against the current heading, creates the final COHESION vector
            centerVnorm = (self.FISH.heading()+15)
        elif centerV < self.FISH.heading() and numberfish > 1:
            centerVnorm = (self.FISH.heading()-15)
        else:
            centerVnorm = self.FISH.heading()
        
        if alignmentV > self.FISH.heading():                    #   Checks the ALIGNMENT vector against the current heading, creates the final ALIGNMENT vector
            alignmentVnorm = (self.FISH.heading()+45)
        elif alignmentV < self.FISH.heading():
            alignmentVnorm = (self.FISH.heading()-45)
        else:
            alignmentVnorm = self.FISH.heading()

        seperateVnorm = (runawayV/numberclose)                  #   Divides the total runawayV by the amount of fish, creates the final SEPERATE vector
        
        #   Creates a weighted average using the weights for each directional vector and also a random vector to keep things interesting
        newheading = (((centerVnorm*Cweight)+(alignmentVnorm*Aweight)+(seperateVnorm*Sweight)+(random.randint(int(self.FISH.heading())-60,int(self.FISH.heading())+60)))/(Cweight+Aweight+Sweight+1))
          
        newheadingV = newheading-(int(newheading/360)*360)      #   Makes sure the final heading is within normal small numbers
        
        return newheadingV

class School:
    def __init__(self,NUMBER,COLORS):
        self.NUMBER = NUMBER
        self.COLORS = COLORS
        self.side = int(width/2)
        self.top = int(height/2)
    
    def spawn(self):
        '''Creates school of fish with the fish func and chooses their colors'''
        global fishList
        
        fishList= []
        
        colors = choosecolors(self.COLORS)  #   Uses the choosecolors callback function to create a randomized color palette for the fish
        
        for i in range(self.NUMBER):
            xcoord = random.choice([-1,1])*random.randint(0,self.side)
            ycoord = random.choice([-1,1])*random.randint(0,self.top)
            
            fishList.append(Fish(xcoord,ycoord,random.randint(0,360),2,colors[random.randint(0,self.COLORS-1)]))    #   Spawns the fish randomly and also adds them to the list
     
     
class Shark:
    def __init__(self):
        
        #Shark Colors
        
        self.gray = [94, 100, 110]
        self.cheeks = [151, 21, 12]
        self.eerieBlack = [21, 21, 20]

        #Turtles that make up shark body:
            
        self.fin = turtle.Turtle(shape = "classic")
        self.tail = turtle.Turtle(shape = "classic")
        self.body = turtle.Turtle(shape = "circle")
        self.mouth = turtle.Turtle(shape = "triangle")
        
        #Sharkbody setup:
        
        self.body.speed(0)
        self.fin.speed(0)
        self.mouth.speed(0)
        self.tail.speed(0)
        self.body.shapesize(1.75,7,2)
        self.mouth.shapesize(.6,1.2,2)
        self.fin.shapesize(7,4,2)
        self.tail.shapesize(4,2.5,2)
        self.body.color(self.eerieBlack,self.gray)
        self.mouth.color(self.eerieBlack,self.cheeks)
        self.fin.color(self.eerieBlack,self.gray)
        self.tail.color(self.eerieBlack,self.gray)
        self.mouth.setheading(180)
        self.body.up()
        self.mouth.up()
        self.fin.up()
        self.tail.up()
        self.body.goto(0,0)
        self.tail.goto(finslocation(self.body.xcor(),self.body.ycor(),self.body.heading(),55))
        self.body.goto(0,0)
        self.mouth.goto(finslocation(self.body.xcor(),self.body.ycor(),self.body.heading(),-62))
        self.fin.goto(finslocation(self.body.xcor(),self.body.ycor(),self.body.heading(),-30))
        self.fin.setheading(self.body.heading())
    
        #Make Shark Start moving
        #Takes a few seconds to register response but moves fine after a couple seconds
        self.SharkMove()

    #The following code heavily modified from user cdlane at stack overflow
    #See comments at tope for exact URL.
    #native python turtle ondrag functionality crashes
    #this method (setting none and then recursivley calling) fixes crashing
    
    def dragging(self, x, y):
        '''Creates (non-crashing) drag functionality for Shark (and corresponding parts)'''
        global sharkx,sharky,mouthx,mouthy
        
        self.body.ondrag(None)
        self.body.setheading(self.body.towards(x, y))
        self.mouth.setheading(self.body.heading()+180)
        self.fin.setheading(self.body.heading())
        self.tail.setheading(self.body.heading())
        self.body.goto(x,y)
        self.tail.goto(finslocation(self.body.xcor(),self.body.ycor(),self.body.heading(),55))
        self.body.goto(x,y)
        self.mouth.goto(finslocation(self.body.xcor(),self.body.ycor(),self.body.heading(),-62))
        self.fin.goto(finslocation(self.body.xcor(),self.body.ycor(),self.body.heading(),-30))
      
        self.body.ondrag(self.dragging)
        
        sharkx = self.body.xcor()   #   sharkx,y used for the fish to run away
        sharky = self.body.ycor()
        
        mouthx = self.mouth.xcor()  #   mouthx,y used to find if fish are getting eaten
        mouthy = self.mouth.ycor()
        
        return self.body.xcor(), self.body.ycor()    
    
    def SharkMove(self):
        '''Call dragging method and update animation'''
            
        self.body.ondrag(self.dragging)
        time.sleep(.005)

#===================FUNCTIONS============================================

def fishWho(x,y,buffer):
    '''Returns the fish that is within the buffer of the x,y unless there
       are no fish within the zone then it returns -1'''
    global fishList
    
    for i in range(len(fishList)):
        FISHX = fishList[i].FISH.xcor() # get x position of each fish
        FISHY = fishList[i].FISH.ycor() # get y position of each fish

        if FISHX - buffer < x < FISHX + buffer and FISHY - buffer < y < FISHY + buffer:
            return i
    else:
        return -1

def sharkdist(selfx,selfy):
    '''Finds the distance between any x,y and the shark, then returns 
       the ALARM value based off of that distance'''
    global sharkx,sharky
        
    howFar = math.sqrt(pow(selfx-sharkx,2)+(pow(selfy-sharky,2)))

    if howFar <= 75:
        return 3                    # This basically just returns how scared the fish should be
    elif 75 < howFar <= 100:
        return 2       
    elif 100 < howFar <= 150:      
        return 1
    else:        
        return 0

def choosecolors(howmany):
    '''Chooses "howmany" amount of random complimentary colors'''
    Color1 = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    Rcolor1 = colorsys.rgb_to_hls(Color1[0], Color1[1], Color1[2])

    increase = 1/howmany
    colorlist = []
    
    for i in range(howmany):    
        
        H1 = abs((Rcolor1[0] + increase*(i+1)) - 1)     #   Uses basic color theory to create complimentary colors based off the color wheel
        color2 = colorsys.hls_to_rgb(H1, Rcolor1[1], Rcolor1[2])    
        colorlist.append((int(color2[0]),int(color2[1]),int(color2[2])))
        
    return colorlist

def murder(sharkx,sharky):
    '''If the shark mouth is within the buffer zone of a fish it hides the fish
       and if no fish are within it does nothing'''
    fishdead = fishWho(sharkx,sharky,30)
                
    if fishdead > -1:
                    
        fishList[fishdead].FISH.hideturtle()                #   Hides the fish and removes it from the list when it gets eaten
        fishList[fishdead].FISHFINS.hideturtle()
        fishList.pop(fishdead)

def finslocation(x,y,heading,distance):
    '''Does the math required to put a turtle behind another turtle a certain
       distance given the x,y,heading,and distance away of the first turtle'''
    xfin = math.cos(math.radians(heading))*-distance    #  Creates a ratio with the given degree and sin/cos to add the given distance to find the new location
    yfin = math.sin(math.radians(heading))*-distance
    
    xfin += x
    yfin += y
    
    return xfin,yfin

#============OBJECT INSTANTIATION AND RUNNING=======================

fishies = School(75,10)
fishies.spawn() 
        
Jaws = Shark()

while RUNNING:
    global fishList
    
    for number in range(len(fishList)):
        fishList[number].swimming()
        
    murder(mouthx,mouthy)
    time.sleep(.005)
    panel.update()
    
panel.mainloop()