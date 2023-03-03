# coding: utf-8

from math import pi,sin,cos

try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

from primitives import wcs,floor
from models import Car,Crane

def gl_init() :
#  glClearColor(1.0,1.0,1.0,0.0);
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

def glut_init() :
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
  glutInitWindowSize(1200,1000)
  glutInitWindowPosition(100,100)
  glutCreateWindow(sys.argv[0])

def glut_event(scene):
  glutDisplayFunc(scene.display)
  glutReshapeFunc(scene.reshape)
  glutKeyboardFunc(scene.on_keyboard_action)
  glutSpecialFunc(scene.on_special_key_action);
##  glutIdleFunc(scene.animation)

class Scene :
  def __init__(self,size) :
    self.size=size
    self.model=Car(size)
##    self.camera=[0,0,5,0,0,0,0,1,0]    
    self.camera=[2,3,7,0,0,0,0,1,0]    
    self.perspective=[60.0,1.0,0.1,50.0]
    self.rotation_y=0.0
  def display(self) :
    gl_init()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    posx,posy,posz=self.camera[0],self.camera[1],self.camera[2]
    dirx,diry,dirz=self.camera[3],self.camera[4],self.camera[5]
    vupx,vupy,vupz=self.camera[6],self.camera[7],self.camera[8]
    gluLookAt(posx,posy,posz,dirx,diry,dirz,vupx,vupy,vupz)
    glRotatef(self.rotation_y,0,1,0)
    floor(10*self.size) 
    # Object to catch
    glPushMatrix()
    glTranslatef(-3,0.5,3)
    glRotatef(45,0,1,0)
    glColor3f(1.0,0.0,1.0)
    glutSolidTeapot(self.size/5.0)
    glPopMatrix()
    # model to control 
    self.model.create()
    glutSwapBuffers()

  def reshape(self,width,height) :
    glViewport(0,0, width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    self.perspective[1]=width*1.0/height
    fovy,ratio,near,far=self.perspective
    gluPerspective(fovy,ratio,near,far)

  def on_keyboard_action(self,key, x, y) :
    if key==b'a':
      glutIdleFunc(scene.animation)
    elif key==b'A':
      glutIdleFunc(None)
    elif key==b'h':
      print("----------------------------------------") 
      print("Documentation Interaction  : Nom-Prenom ") 
      print("h : afficher cette aide")
      print("s : sortie d'application")
      print("----------------------------------------") 
      print("---------") 
      print("Affichage")
      print("---------") 
      print("a/A : lancer/Stopper l'animation")
      print("c/C : faces CW/CCW")
      print("f/F : faces/Aretes")
      print("r/R : redimensionner la scene")
      print("i : etat initial de la scene")
      print("w : repere de scene visible/invisible")
      print("------") 
      print("Camera")
      print("------") 
      print("n/N : se rapprocher/s'eloigner de la scene")
      print("u/U : tourner autour de la scene")
      print("----") 
      print("Voiture")
      print("----")
      print("fleches up/down : avancer/reculer la voiture sur le plan")
      print("fleches left/right : tourner la voiture dans le plan")
      print("----") 
      print("Grue")
      print("----")
      print("b/B : faire pivoter le bras")
      print("g/G : faire pivoter l'avant-bras")
      print("...: ....")
      print("----") 
      print("...")
      print("----")
      print("...: ....")
     
    elif key== b'b' :
      pass
    elif key== b'B':
      pass
    elif key== b'c' :
      glFrontFace(GL_CW)
    elif key== b'C' :
      glFrontFace(GL_CCW)
    elif key== b'e' :
      pass  
    elif key== b'f':
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    elif key== b'F':
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    elif key== b'g' :
      pass
    elif key== b'G':
      pass
    elif key == b'n' :
      pass
    elif key == b'N' :
      pass
    elif key== b's' :
      pass
    elif  key == b'u' :
      pass
    elif  key == b'U' :
      pass
    elif  key == b'v' :
      pass
    elif  key == b'V' :
      pass
    elif  key == b'w' :
      pass
    elif  key == 'W' :
      pass
    else :
      pass
    glutPostRedisplay()

  def on_mouse_action(self,button,state,x,y) :
    if  button==GLUT_LEFT_BUTTON :
      if state==GLUT_DOWN :
        print("button down")
      else:
        print("button up")
    else :
      pass
    glutPostRedisplay()

  def on_special_key_action(self,key, x, y) :
    position=self.model.get_position()
    orientation=self.model.get_orientation()
    if key ==  GLUT_KEY_UP :
        position[0]+=0.1*self.size*sin(orientation*pi/180.0)
        position[2]+=0.1*self.size*cos(orientation*pi/180.0)
    elif  key ==  GLUT_KEY_DOWN :
        position[0]-=0.1*self.size*sin(orientation*pi/180.0)
        position[2]-=0.1*self.size*cos(orientation*pi/180.0)
    elif key ==  GLUT_KEY_LEFT :
        orientation+=5
    elif  key ==  GLUT_KEY_RIGHT :
        orientation-=5
    else :
        pass
    self.model.set_position(position)
    self.model.set_orientation(orientation)
    glutPostRedisplay()

  def animation(self) :
    self.rotation_y+=0.1
    if self.rotation_y > 360.0 :
      self.rotation_y-=360
    glutPostRedisplay()

if __name__ == "__main__" :
   glutInit(sys.argv)
   glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
   glutInitWindowSize (500, 500)
   glutInitWindowPosition (100, 100)
   glutCreateWindow ("REV OpenGL scene")
   glClearColor(1.0,1.0,1.0,1.0)
   dimension=2.0
   scene=Scene(dimension)
   glut_event(scene)
   glutMainLoop()
