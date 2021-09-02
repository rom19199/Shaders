# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 16:05:25 2021

@author: hugo_
"""


class Obj1(object):
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        ##
        try:
            f = open(fileName)
            for line in f:
                prefix,value = line.split(' ',1)
                print(value)
             
                if line[:2] == "v ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                    self.vertices.append(vertex)

                elif line[0] == "f":
                    string = line.replace("//", "  ").replace("/", " ")
                   
                    
                   
                    ##
                    i = string.find(" ") + 1
                    
                    face = []
                    for item in range(string.count(" ")):
                        if string.find(" ", i) == -1:
                            face.append((string[i:-1]))
                            break
                        face.append(string[i:string.find(" ", i)])
                        i = string.find(" ", i) + 1
                    ##
                    
                    
                    # print(face)
                    # results = list(map(int, face))
                    (self.faces.append(list(face)))
                    # self.faces.append([list(map(int, fa.split('/'))) for fa in a.split(' ')])

            f.close()
        except IOError:
            print(".obj file not found.")

class Obj2(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
              prefix, value = line.split(' ', 1) 
             

              if prefix == 'v':
                self.vertices.append(list(map(float, value.split(' '))))
              elif prefix == 'f':
                  
                # for face in value.split(' '):
                 self.faces.append([list(map(int , face.split('/'))) for face in value.split(' ')])
                 # if face.split('/') or face.split('//'):
                     # self.faces.append([list(map(int,face.split('//')))])
            
# cara = Obj('./stormtrooper.obj')
# print(cara.vertices)
# print(cara.faces)

def try_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val


class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.vfaces.append([list(map(try_int, face.split('/'))) for face in value.split(' ')])