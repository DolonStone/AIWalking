import pygame
import pymunk
import random
from pymunk.pygame_util import DrawOptions
from networks import neuralnetwork
from networks import matrix
from networks import evolution



def floor_object(space, xcoord, ycoord, length,  width):
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (xcoord, ycoord)
    shape = pymunk.Poly.create_box(b, (length,width))
    shape.friction = 1
    space.add(b, shape)
    

def still_rectangle(space, xcoord, ycoord, length,  width, r,g,blue,t,cgroup):
  
    b = pymunk.Body(body_type=pymunk.Body.STATIC)
    b.position = (xcoord, ycoord)
    shape = pymunk.Poly.create_box(b, (length,width))
    shape.mass = 1
    shape.friction = 1
    shape.filter = pymunk.ShapeFilter(group = cgroup)
    shape.color = (r, g, blue, t)
    space.add(b, shape)
    return shape, b
  
def moving_rectangle(space, xcoord, ycoord, length,  width, r,g,blue,t,cgroup):
    b = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    b.position = (xcoord, ycoord)
    shape = pymunk.Poly.create_box(b, (length,width))
    shape.mass = 1
    shape.friction = 1
    shape.filter = pymunk.ShapeFilter(group = cgroup)
    shape.color = (r, g, blue, t)
    space.add(b, shape)
    
    return shape, b
  
class SimpleMotor:
  def __init__(self, b, b2, rate):
    self.joint1 = pymunk.SimpleMotor(b,b2,rate)
    space.add(self.joint1)

class PinJoint:
  def __init__(self, b, b2, a=(0, 0), a2=(0, 0)):
    self.joint = pymunk.PinJoint(b, b2, a, a2)
    self.joint.distance = 0
    space.add(self.joint)
    
class leg:
  def __init__(self, length,lowerleglength, xcoord,ycoord,layer,chestb):
    self.upperleg,self.upperlegbody = moving_rectangle(space, xcoord, ycoord, 10,length,255,0,0,100,layer)
    self.lowerleg,self.lowerlegbody = moving_rectangle(space, xcoord, ycoord+(length/2), 10,lowerleglength,255,0,0,100,layer)
    self.joint = PinJoint(self.upperlegbody,self.lowerlegbody,(0,length/2),(0,-lowerleglength/2))
    self.motor = SimpleMotor(self.upperlegbody,self.lowerlegbody,0)
    self.upperjoint = PinJoint(chestb,self.upperlegbody,(0,20),(0,-length/2))
    self.uppermotor = SimpleMotor(chestb,self.upperlegbody,0)
  
  def coords(self):
    x1,y1 = self.upperlegbody.position
    x2,y2 = self.lowerlegbody.position
    return x1,y1,x2,y2
    





class person:
  def __init__(self,leglength,lowerleglength,numberoflegs,layer,humanleg):
    self.chest, self.chestb = moving_rectangle(space, 130, floorheight-235, 40,40,70,80,80,100,layer)
    self.legs = []
    if humanleg == True:
      self.humanleg = leg(leglength,lowerleglength,100,500,layer,self.chestb)
    self.brain = neuralnetwork(32,8,numberoflegs*2,numberoflegs*2)
    self.brain.createnetwork()
    self.switch1 = 1
  
    self.switch2 = 0
    for i in range(numberoflegs):
      self.legs.append(leg(leglength,lowerleglength, 100,floorheight-200,layer,self.chestb))

  
  def ChangeSpeed(self,leg,speed,upper):
    if upper == True:
      self.legs[leg].uppermotor.joint1.rate = speed
    else:
      self.legs[leg].motor.joint1.rate = speed


  def iteratehumanlegv2(self):
    
    if self.switch1 == 0:
      self.humanleg.uppermotor.joint1.rate = 0.75
      if self.chestb.rotation_vector.get_angle_degrees_between(self.humanleg.upperlegbody.rotation_vector) <= -40:
        self.switch1 = 1
    else:
      self.humanleg.uppermotor.joint1.rate = -0.75
      if self.chestb.rotation_vector.get_angle_degrees_between(self.humanleg.upperlegbody.rotation_vector) >= 22:
        self.switch1 = 0
    if self.switch2 == 0:
      self.humanleg.motor.joint1.rate = -0.75
      if self.humanleg.upperlegbody.rotation_vector.get_angle_degrees_between(self.humanleg.lowerlegbody.rotation_vector) >= 15:
        self.switch2 = 1
    elif self.switch2 == 1:
      self.humanleg.motor.joint1.rate = 0.75
      if self.humanleg.upperlegbody.rotation_vector.get_angle_degrees_between(self.humanleg.lowerlegbody.rotation_vector) <= 0:
        self.switch2 = 2
    elif self.switch2 == 2:
      self.humanleg.motor.joint1.rate = -0.75
      if self.humanleg.upperlegbody.rotation_vector.get_angle_degrees_between(self.humanleg.lowerlegbody.rotation_vector) >= 47:
        self.switch2 = 3
    else:
      self.humanleg.motor.joint1.rate = 0.75
      if self.humanleg.upperlegbody.rotation_vector.get_angle_degrees_between(self.humanleg.lowerlegbody.rotation_vector) <= 0:
        self.switch2 = 0


    
  def newbrain(self,brain):
    self.brain = brain

  #left leg info
  def GetRotationVector(self,leg):
   x = self.chestb.rotation_vector.get_angle_degrees_between(self.legs[leg].upperlegbody.rotation_vector)
   y = self.legs[leg].upperlegbody.rotation_vector.get_angle_degrees_between(self.legs[leg].lowerlegbody.rotation_vector)
   return x,y

  def GetCoords(self,leg):
   return self.legs[leg].coords()


  


numiterations = 1

grey = (217, 217, 217)
black = (0, 0, 0)



pygame.init()
normaltype = "yes"#input("Would you like to use factory settings?")
if normaltype == "Yes" or normaltype == "yes":
  iterationtime = 2
  numberofprosthetics = 2#random.randint(2,4)
  upperleglength = 70
  lowerleglength = 70
  population = 40//numberofprosthetics
  humanleg = False
else:
  iterationtime = int(input("Please enter the time of iteration you would like (longer time means better AIs move on):"))
  numberofprosthetics = int(input("Please enter the number of prosthetics on the body:"))
  while numberofprosthetics <1:
    numberofprosthetics = int(input("Please enter a number greater than 0, the simulation requires at least 1 prosthetic"))
  upperleglength = int(input("please enter the length of your upper leg in centimeters:"))
  lowerleglength = int(input("Please enter the length of your lower leg in centimeters:"))
  population = int(input("please enter the number of people in a population (a large population means a higher likelyhood to find a good one):"))
  while population < 1:
    population = int(input("Please enter a number greater than 0, the simulation requires at least 1 person, and 7 or more is prefered"))
  #humanleg = input("would you like to have a human leg included?")
  if humanleg == "yes" or humanleg == "y" or humanleg == "True":
    humanleg = True
start = True

while True:
  floorheight = 800#original = 400
  screenwidth = floorheight*(16/9)
  display = pygame.display.set_mode((screenwidth, floorheight))
  clock = pygame.time.Clock()
  space = pymunk.Space()
  space.gravity = (0, 981)
  draw_options = pymunk.pygame_util.DrawOptions(display)
  farthest = [0,-1000]

  floor_object(space, screenwidth/2, floorheight, 1920, 20) #the floor
  floor_object(space, 0, floorheight-200, 20, 1500) #the left wall
  #floor_object(space, 400, floorheight-300, 20, 20)
  floor_object(space, screenwidth, floorheight, 20, 800) #right wall
  #floor_object(space, 500, 400, 20, 100)
  FPS = 5000
  display.fill((217, 217, 217))
  textnumber = str(numiterations)
  
  if start:
    start = False
    peopledictionary = {0:person(upperleglength,lowerleglength,numberofprosthetics,1,humanleg)}
    for i in range (1,population):
      peopledictionary.update({i:person(upperleglength,lowerleglength,numberofprosthetics,1,humanleg)})
  else:
    peopledictionary = {0:person(upperleglength,lowerleglength,numberofprosthetics,1,humanleg)}
    for i in range (1,population):
      peopledictionary.update({i:person(upperleglength,lowerleglength,numberofprosthetics,1,humanleg)})
    for j in range (0,population):
      peopledictionary[j].brain = newpopulation.children[j]


  font = pygame.font.Font("freesansbold.ttf", 32)
  text = font.render("iteration number "+textnumber, True, black, grey)
  textRect = text.get_rect()
  textRect.center = (200, floorheight-200)
  
  currenttime = 0
  while currenttime<iterationtime:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              print("thanks for using this project!")
              exit()

      display.fill((217, 217, 217))
      display.blit(text, textRect)
      space.debug_draw(draw_options)

      space.step(1 / 50)
      currenttime = currenttime + 0.01
      
      

      for i in range(population):
        if humanleg == True:
          peopledictionary[i].iteratehumanlegv2()
          
        matrix1 = matrix(2,1)
        list2 = []
        
        for j in range(numberofprosthetics):
          xcoord1,ycoord1,xcoord2,ycoord2 = peopledictionary[i].GetCoords(j)
          list2.append(-(ycoord1-floorheight+30))
          list2.append(-(ycoord2-floorheight+30))
          #list2.append(xcoord1)
          #list2.append(xcoord2)
        
        matrix1.createnormal(list2)
    
        movements = peopledictionary[i].brain.runthrough(matrix1)
        
        for j in range(len(movements)//2):
          movements[j] = [movements[j][0],movements[j+1][0]]
          movements.pop(j+1)
        
        for j in range(numberofprosthetics):
          upperangledifference,lowerangledifference = peopledictionary[i].GetRotationVector(j)
          if lowerangledifference < -135 and movements[j][0] > 0:
            peopledictionary[i].ChangeSpeed(j,0,False)
          elif lowerangledifference > 135 and movements[j][0] < 0:
            peopledictionary[i].ChangeSpeed(j,0,False)
          else:
            peopledictionary[i].ChangeSpeed(j,movements[j][0]*2,False)
          if upperangledifference < -90 and movements[j][1] > 0:
            peopledictionary[i].ChangeSpeed(j,0,True)
          elif upperangledifference > 90 and movements[j][1] < 0:
            peopledictionary[i].ChangeSpeed(j,0,True)
          else:
            peopledictionary[i].ChangeSpeed(j,movements[j][1]*2,True)
            
            

        
      pygame.display.update()
      clock.tick(FPS)
  
  for i in range (0,population):
    distances = []
    heights = []
    for j in range(0,numberofprosthetics):
      x,y,x1,y1 = peopledictionary[i].GetCoords(j)
      
      x3,y3 = peopledictionary[i].chest.body.position
      distances.append(x)
      distances.append(x1)
      heights.append((-y3)+floorheight-10)
      
    #print(((sum(distances,0)/numberofprosthetics)/8) , (sum(heights,0)))
    distance = ((sum(distances,0)/numberofprosthetics)/4) + (sum(heights,0))
    if distance > farthest[1]:
      farthest[0] = i
      farthest[1] = distance
    else:
      pass
  #print(farthest)
  
  numiterations += 1
  if((numiterations % 10 == 0) & (iterationtime<14)):
      iterationtime += 2
  #newpopulation = evolution(population,peopledictionary[farthest[0]].brain)
  if(farthest[1] > 250 and numiterations<=15):         
      newpopulation = evolution(population,peopledictionary[farthest[0]].brain)
  else:
      if(farthest[1] > 400):
          newpopulation = evolution(population,peopledictionary[farthest[0]].brain)
      else:
          start = True
          numiterations = 0
  
