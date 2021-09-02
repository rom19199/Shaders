# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:18:48 2021

@author: hugo_
"""

import struct
import random
import numpy
from obj import Obj
from collections import namedtuple
from math import sin


V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])


def sum(v0, v1):
 
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
 
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
 
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
 
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
 
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()

  return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

def barycentric(A, B, C, P):
 
  cx, cy, cz = cross(
    V3(B.x - A.x, C.x - A.x, A.x - P.x), 
    V3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if abs(cz) < 1:
    return -1, -1, -1

  # [cx cy cz] = [u v 1]

  u = cx/cz
  v = cy/cz
  w = 1 - (u + v)

  return w, v, u





def char(c):
  """
  Input: requires a size 1 string
  Output: 1 byte of the ascii encoded char 
  """
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  """
  Input: requires a number such that (-0x7fff - 1) <= number <= 0x7fff
         ie. (-32768, 32767)
  Output: 2 bytes
  Example:  
  >>> struct.pack('=h', 1)
  b'\x01\x00'
  """
  return struct.pack('=h', w)

def dword(d):
  """
  Input: requires a number such that -2147483648 <= number <= 2147483647
  Output: 4 bytes
  Example:
  >>> struct.pack('=l', 1)
  b'\x01\x00\x00\x00'
  """
  return struct.pack('=l', d)

def color(r, g, b):
  """
  Input: each parameter must be a number such that 0 <= number <= 255
         each number represents a color in rgb 
  Output: 3 bytes
  Example:
  >>> bytes([0, 0, 255])
  b'\x00\x00\xff'
  """
  return bytes([b, g, r])



BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)




class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()
    
    

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)] 
      for y in range(self.height)
    ]
    
    self.zbuffer = [
        [-9999999 for x in range(self.width)]
        for y in range(self.height)
        ]

  def write(self, filename):
    f = open(filename, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel data (width x height x 3 pixels)
    for x in range(self.height):
      for y in range(self.width):
        f.write(self.pixels[x][y])

    f.close()

  def display(self, filename='out.bmp'):
    """
    Displays the image, a external library (wand) is used, but only for convenience during development
    """
    self.write(filename)

    try:
      from wand.image import Image
      from wand.display import display

      with Image(filename=filename) as image:
        display(image)
    except ImportError:
      pass  # do nothing if no wand is installed

  def set_color(self, color):
    self.current_color = color

  def point(self, x, y, color = None):
    # 0,0 was intentionally left in the bottom left corner to mimic opengl
    try:
      self.pixels[y][x] = color or self.current_color
    except:
      # To avoid index out of range exceptions
      pass
  
  def shader(self,x,y):
      
      center_x, center_y = 215,215
      radius = 25
      
      center_x2, center_y2 = 215,215
      radius2 = 20
      
      if y >= 100 and y <= 160  + sin (x/3.1416):
          # return color(222,184,135)
          return color(194,155,97)
      
      elif y >= 160 and y <= 180 + sin (x/3.1416) :
          return color(222,184,135)
      
      elif (x-center_x)**2 + (y-center_y)**2 < radius**2 and (x-center_x2)**2 + (y-center_y2)**2 < radius2**2 :
            return color(128,64,0)
      
      elif (x-center_x)**2 + (y-center_y)**2 < radius**2:
          return color(205,133,63)
   
      elif y >= 180 and y <= 220 + sin (x/3.1416):
          return color(128,64,0)
      
      elif y >= 220 and y <= 280 + sin (x/3.1416):
          return color(222,184,135)
      
      elif y >= 280 and y <= 320 + sin (x/3.1416):
          return color(128,64,0)
      
      elif y >= 330 and y <= 337  + sin (x/3.1416):
          # return color(222,184,135)
          return color(194,155,97)
      
      elif y >= 320 and y <= 340 + sin (x/3.1416) :
          return color(222,184,135)
      
      elif y >= 340 and y <= 400 + sin (x/3.1416) :
          # return color(222,184,135)
          return color(194,155,97)
      
      
      
     
      
      # else:
      #      return color(194,155,97)
       
     
          
      
      
      
      # if y > 200 and y < 210:
      #     return color(255,255,255)
      
      # else:
      #     return color(194,155,97)
      
     
      
     
      
    

      
      
      
      
      
    
  def line(self, start, end, color = None):
   
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x, color)
        else:
            self.point(x, y, color)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2

 

  def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    # returns a vertex 3, translated and transformed
    return V3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2])
    )

  def triangle(self, A, B, C, color=None, texture=None, texture_coords=(), intensity=1):
    bbox_min, bbox_max = bbox(A, B, C)

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V2(x, y))
        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
          continue
        
        if texture:
          tA, tB, tC = texture_coords
          tx = tA.x * w + tB.x * v + tC.x * u
          ty = tA.y * w + tB.y * v + tC.y * u
          
          color = texture.get_color(tx, ty, intensity)
          
        color = self.shader(x,y)

        z = A.z * w + B.z * v + C.z * u

        if x < 0 or y < 0:
          continue
      
        

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, color)
          self.zbuffer[x][y] = z

  def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    # returns a vertex 3, translated and transformed
    return V3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2])
    )
    
  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)):
   
    model = Obj(filename)

    light = V3(0,0,1)

    for face2 in model.vfaces:
        vcount = len(face2)

        if vcount == 3:
          f1 = face2[0][0] - 1
          f2 = face2[1][0] - 1
          f3 = face2[2][0] - 1

          a = self.transform(model.vertices[f1], translate, scale)
          b = self.transform(model.vertices[f2], translate, scale)
          c = self.transform(model.vertices[f3], translate, scale)

          normal = norm(cross(sub(b, a), sub(c, a)))
          intensity = dot(normal, light)
          grey = round(255 * intensity)
          if grey < 0:
            continue  
          
          self.triangle(a, b, c, color(grey, grey, grey))

        else:
          # assuming 4
          f1 = face2[0][0] - 1
          f2 = face2[1][0] - 1
          f3 = face2[2][0] - 1
          f4 = face2[3][0] - 1   

          vertices = [
            self.transform(model.vertices[f1], translate, scale),
            self.transform(model.vertices[f2], translate, scale),
            self.transform(model.vertices[f3], translate, scale),
            self.transform(model.vertices[f4], translate, scale)
          ]

          normal = norm(cross(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))  # no necesitamos dos normales!!
          intensity = dot(normal, light)
          grey = round(255 * intensity)
          if grey < 0:
            continue

       
  
          A, B, C, D = vertices 
        
          self.triangle(A, B, C, color(grey, grey, grey))
          self.triangle(A, C, D, color(grey, grey, grey))
         
          
          
r = Render(800, 600)
r.load('./sphere.obj', (1, 1, 1), (250, 250, 250))
r.display('planet.bmp')
          


