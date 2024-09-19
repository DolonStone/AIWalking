import random
import math
import copy
from numba import njit


class matrix:
    def __init__(self, rows, cols):
        self._rows = int(rows)
        self._cols = int(cols)
        self._matrices = []
    def createrandom(self):
        for i in range(self._rows):
            self._matrices.append([])
            for j in range(self._cols):
                self._matrices[i].append(random.uniform(-1,1))
        return(self._matrices)
    def createnormal(self, numberlist):
      p = 0
      for i in range(self._rows):
            self._matrices.append([])
            for j in range(self._cols):
                self._matrices[i].append(numberlist[p])
                p = p+1
    def copy(self, old_matrix):
      try:
        self._rows = len(old_matrix)
        self._matrices = old_matrix
        self._cols = len(old_matrix[0])
        
      except:
        self._rows = old_matrix._rows
        self._matrices = old_matrix._matrices
        self._cols = old_matrix._cols
        

    def sigmoid(self):
      
      for i in range (0,self._rows):

        for j in range (0,self._cols):
          try:
            
            self._matrices[i][j] = ((1/(1+(math.exp(-(self._matrices[i][j])))))-0.5)*2
          except:
            pass
 
    def tanh(self):
      for i in range (0,self._rows):

        for j in range (0,self._cols):
          try:
            self._matrices[i][j] = (math.exp(self._matrices[i][j])-math.exp(-(self._matrices[i][j])))/(math.exp(self._matrices[i][j])+math.exp(-(self._matrices[i][j])))
          except:
            pass
      
  
    def __mul__(self,new_matrix):
      tempmatrix = []
      for i in range(self._rows):
        tempmatrix.append([])
        for j in range(new_matrix._cols):
          tempmatrix[i].append(0)
          
      for i in range(self._rows):
        for j in range(new_matrix._cols):
          for k in range (new_matrix._rows):
            
            tempmatrix[i][j] = (tempmatrix[i][j] + (new_matrix._matrices[k][j]*self._matrices[i][k]))
      return(tempmatrix)
      


class neuralnetwork:
  def __init__(self, hiddenlayers, hiddennodes, inputnodes, outputnodes):
    self._cols = int(hiddenlayers)
    self._rows = int(hiddennodes)
    self._inodes = int(inputnodes)
    self._onodes = int(outputnodes)
    self._neuralnetwork = []
  def createnetwork(self):
    matrixtemp1 = matrix(self._rows,self._inodes)
    matrixtemp1.createrandom()
    self._neuralnetwork.append(matrixtemp1)
    for i in range (self._cols-1):
      matrixtemp2 = matrix(self._rows,self._rows)
      matrixtemp2.createrandom()
      self._neuralnetwork.append(matrixtemp2)
    matrixtemp3 = matrix(self._onodes,self._rows)
    matrixtemp3.createrandom()
    self._neuralnetwork.append(matrixtemp3)
    
  def copynetwork(self):
    newnetwork = copy.deepcopy(self)
    return newnetwork
    
  
  def runthrough(self, inputvalues):
    tempmatrix = matrix(1,1)
    tempmatrix.copy(self._neuralnetwork[0]*inputvalues)
    for i in range(1,self._cols+1):
      tempmatrix.tanh()
      lastmatrix = matrix(1,1)
      lastmatrix.copy(tempmatrix)
      tempmatrix.copy(self._neuralnetwork[i]*lastmatrix)
    tempmatrix.sigmoid()
    return tempmatrix._matrices
  
    
class evolution:
  def __init__(self,offspring,parent):
    self.offspring = offspring
    self.children = {}
    self.parent = parent
    self.populate()

    self.evolvetype2()
  def populate(self):
    for i in range (self.offspring):
      tempnetwork = self.parent.copynetwork()
      
      self.children.update({i:tempnetwork})
      
          
            



  def evolvetype2(self):
    for i in range(self.offspring-1):
      randomtype = random.randint(1,3)

      if randomtype == 1:
          for j in range(self.children[i]._rows): #inputlayer
            for k in range(self.children[i]._inodes):
              self.changenetworksmall(i,0,j,k)
          for l in range(1,self.children[i]._cols): #hidddenlayers
            for j in range(self.children[i]._rows):
              for k in range(self.children[i]._rows):
                self.changenetworksmall(i,l,j,k)
          
          for j in range(self.children[i]._onodes): #outputlayer
            for k in range(self.children[i]._rows):
              self.changenetworksmall(i,self.children[i]._cols,j,k)
          
      elif randomtype == 2:
          for j in range(self.children[i]._rows): #inputlayer
            for k in range(self.children[i]._inodes):
              self.changenetworkmedium(i,0,j,k)
          for l in range(1,self.children[i]._cols): #hidddenlayers
            for j in range(self.children[i]._rows):
              for k in range(self.children[i]._rows):
                self.changenetworkmedium(i,l,j,k)
          
          for j in range(self.children[i]._onodes): #outputlayer
            for k in range(self.children[i]._rows):
              self.changenetworkmedium(i,self.children[i]._cols,j,k)
          #print(self.children[i]._neuralnetwork[0].matrices[0][0])
      else:
          for j in range(self.children[i]._rows): #inputlayer
            for k in range(self.children[i]._inodes):
              self.changenetworklarge(i,0,j,k)
          for l in range(1,self.children[i]._cols): #hidddenlayers
            for j in range(self.children[i]._rows):
              for k in range(self.children[i]._rows):
                self.changenetworklarge(i,l,j,k)
          
          for j in range(self.children[i]._onodes): #outputlayer
            for k in range(self.children[i]._rows):
              self.changenetworklarge(i,self.children[i]._cols,j,k)
          #print(self.children[i]._neuralnetwork[0].matrices[0][0])



  def changenetworksmall (self,child,layer,row,collumn):
    randomtype = random.randint(1,2)
    if randomtype == 1:
        self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = self.children[child]._neuralnetwork[layer]._matrices[row][collumn] + random.uniform(-0.001,0.001)
    else:
        pass
    self.checkifover(child,layer,row,collumn)

  
    
  def changenetworkmedium (self,child,layer,row,collumn):
    randomtype = random.randint(1,2)
    if randomtype == 1:
        self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = self.children[child]._neuralnetwork[layer]._matrices[row][collumn] + random.uniform(-0.01,0.01)
    else:
        self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = self.children[child]._neuralnetwork[layer]._matrices[row][collumn] + random.uniform(-0.1,0.1)   
    self.checkifover(child,layer,row,collumn)
    
  def changenetworklarge(self,child,layer,row,collumn):
    randomtype = random.randint(1,2)
    if randomtype == 1:
        self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = self.children[child]._neuralnetwork[layer]._matrices[row][collumn] + random.uniform(-0.1,0.1)
    else:
        self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = self.children[child]._neuralnetwork[layer]._matrices[row][collumn] + random.uniform(-1,1)   
    self.checkifover(child,layer,row,collumn)
    
  def checkifover(self,child,layer,row,collumn):
    if self.children[child]._neuralnetwork[layer]._matrices[row][collumn]>1:
      self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = 1
    elif self.children[child]._neuralnetwork[layer]._matrices[row][collumn]<-1:
      self.children[child]._neuralnetwork[layer]._matrices[row][collumn] = -1
    else:
      pass
    

 
