from math import pi,sin,cos

try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

def wcs(size) :
  glBegin(GL_LINES)
  glColor3ub(255,255,255)
  glVertex2f(0,0)
  glVertex2f(0,size)
  glVertex2f(0,0)
  glVertex2f(size,0)
  glVertex2f(0,0)
  glVertex3f(0,0,size)
  glEnd()

def square(size) :
# face avant : sommets de couleurs RGBW
  glBegin(GL_POLYGON)
  glColor3f(1.0,0.0,0.0)   # Red 
  glVertex2f(-size,-size)
  glColor3f(0.0,1.0,0.0)   # Green
  glVertex2f(size,-size)
  glColor3f(0.0,0.0,1.0)   # Blue
  glVertex2f(size,size)
  glColor3f(1.0,1.0,1.0)   #  White
  glVertex2f(-size,size)
  glEnd()
#face arriere : couleur uniforme White
  glBegin(GL_POLYGON)
  glVertex2f(-size,-size)
  glVertex2f(-size,size)
  glVertex2f(size,size)
  glVertex2f(size,-size)
  glEnd()

def cube(size) :
  glBegin(GL_QUADS)
  glColor3ub(255,0,0)            # face rouge
  glVertex3d(size,size,size)
  glVertex3d(size,size,-size)
  glVertex3d(-size,size,-size)
  glVertex3d(-size,size,size)
  glColor3ub(0,255,0)            # face verte
  glVertex3d(size,-size,size)
  glVertex3d(size,-size,-size)
  glVertex3d(size,size,-size)
  glVertex3d(size,size,size) 
  glColor3ub(0,0,255)            # face bleue
  glVertex3d(-size,-size,size)
  glVertex3d(-size,-size,-size)
  glVertex3d(size,-size,-size)
  glVertex3d(size,-size,size) 
  glColor3ub(255,255,0)          #  face jaune
  glVertex3d(-size,size,size)
  glVertex3d(-size,size,-size)
  glVertex3d(-size,-size,-size)
  glVertex3d(-size,-size,size)
  glColor3ub(0,255,255)          # face cyan
  glVertex3d(size,size,-size)
  glVertex3d(size,-size,-size)
  glVertex3d(-size,-size,-size)
  glVertex3d(-size,size,-size)
  glColor3ub(255,0,255)        # face magenta
  glVertex3d(size,-size,size)
  glVertex3d(size,size,size)
  glVertex3d(-size,size,size)
  glVertex3d(-size,-size,size)
  glEnd()

def sphere(radius) :
  longitude,latitude=10,20
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluSphere(params,radius,longitude,latitude)
  gluDeleteQuadric(params)

def cylinder(base,top,height,slices=10,stacks=5) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluCylinder(params,base,top,height,slices,stacks)
  gluDeleteQuadric(params)

def disk(inner,outer,slices=10,loops=5) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluDisk(params,inner,outer,slices,loops)
  gluDeleteQuadric(params)

def stick(base,top,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  glColor3f(1,0,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  glColor3f(0,1,0)
  cylinder(base,top,height,slices,stacks)
  glPushMatrix()
  glTranslatef(0,0,height)
  glColor3f(1,0,0)
  disk(0,top,slices,stacks)
  glPopMatrix()

def cone(base,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  cylinder(base,0,height,slices,stacks)

def joint(radius) :
  longitude,latitude=10,20
  sphere(radius,longitude,latitude)

def torus(inner,outer,sides=10,rings=5) :
  glutSolidTorus(inner, outer, sides, rings)

def axe(base,height,slices=10,stacks=5) :
  # TODO : create 3D axe with disk, cylinder,cone
  stick(base,base,height,slices,stacks)

# def wcs(size) :
  # TODO : redefine  WCS  with 3D axes (Ox,Oy,Oz)

  
def floor(size,tiles=10) :
  tile_size=size/tiles
  for i in range(10+1) :
    for j in range(10+1) :
        glPushMatrix()
        glTranslatef(-size/2.0+tile_size*i,0.0,-size/2.0+tile_size*j)
        # glTranslatef(-size/2.0+tile_size*i,-1.0,-size/2.0+tile_size*j)
        if (i+j)%2 == 0 :
            glColor3f(1.0,1.0,1.0)
            glRotatef(-90,1,0,0)
            glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
        else :
            glColor3f(0.0,0.0,0.0)
            glRotatef(90,1,0,0)
            glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
        glPopMatrix()

def display() :
  global size,position,orientation
  # openGL init
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)
  # model/view 
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  posx,posy,posz=2,5,10
  dirx,diry,dirz=0,0,0
  vupx,vupy,vupz=0,1,0
  gluLookAt(posx,posy,posz,dirx,diry,dirz,vupx,vupy,vupz)
  # scene creation  : begin
  floor(10*size) 
  x,y,z=position[0],position[1],position[2]
  glPushMatrix()
  glTranslatef(x,y,z)
  glRotatef(orientation,0,1,0)
  glColor3f(1.0,0.0,1.0)
  # glutSolidTeapot(self.size/5.0)
  axe(0.2*size,size) 
  glPopMatrix()
  # scene creation  : end
  glutSwapBuffers()

def reshape(width,height) :
  glViewport(0,0, width,height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  fovy,ratio,near,far=60.0,width*1.0/height,0.1,50.0
  gluPerspective(fovy,ratio,near,far)

def on_mouse_action(button,state,x,y) :
  if  button==GLUT_LEFT_BUTTON :
    if state==GLUT_DOWN :
      print("button down")
    else:
      print("button up")
  else :
    pass
  glutPostRedisplay()

def on_special_key_action(key,x,y) :
  global size,position,orientation
  if key ==  GLUT_KEY_UP :
      position[0]+=0.1*size*sin(orientation*pi/180.0)
      position[2]+=0.1*size*cos(orientation*pi/180.0)
  elif  key ==  GLUT_KEY_DOWN :
      position[0]-=0.1*size*sin(orientation*pi/180.0)
      position[2]-=0.1*size*cos(orientation*pi/180.0)
  elif key ==  GLUT_KEY_LEFT :
      orientation+=5
  elif  key ==  GLUT_KEY_RIGHT :
      orientation-=5
  else :
      pass
  glutPostRedisplay()

if __name__ == "__main__" : 
  size=2.0
  orientation=0
  position=[0,0,0]
  glutInit(sys.argv)
  glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutInitWindowSize (500, 500)
  glutInitWindowPosition (100, 100)
  glutCreateWindow ("REV OpenGL primitives")
  glClearColor(1.0,1.0,1.0,1.0)
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutSpecialFunc(on_special_key_action);
  glutMainLoop()
