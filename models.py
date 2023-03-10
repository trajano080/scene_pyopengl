from math import pi, sin, cos

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("Error: PyOpenGL not installed properly !!")
    sys.exit()

from primitives import *


class Model:
    def __init__(self, size=1.0):
        self.size = size
        self.angle = 0.0
        self.position = [0.0, 0.0, 0.0]
        self.wheelTurn = 0.0
        self.wheelRotation = 0.0
    # getter/setter

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def set_orientation(self, angle):
        # print(angle)
        self.angle = angle

    def get_orientation(self):
        return self.angle

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position.copy()

    # Wheels rotation around Y axe
    def set_wheel_turn(self, angle):
        self.wheelTurn = angle

    def get_wheel_turn(self):
        return self.wheelTurn

    # Wheels rotation around Z axe
    def set_wheel_rotation(self, angle):
        self.wheelRotation = angle

    def get_wheel_rotation(self):
        return self.wheelRotation

    def create(self):
        raise NotImplementedError


class Car(Model):
    def __init__(self, size=1.0):
        Model.__init__(self, size)
        glPushMatrix()
        glRotate(90, 0, 1, 0)
        glTranslatef(0, 2, 0)
        self.create()
        glPopMatrix()

    def create(self):
        glPushMatrix()
        #glScalef(1, 1, 2)
        x, y, z = self.position[0], self.position[1], self.position[2]
        glTranslatef(x, y, z)
        glRotatef(self.angle, 0, 1, 0)
        # car body
        Zshift = -self.size
        axe(0.5*self.size, 2*self.size, Zshift=Zshift)

        # roue av gauche
        glPushMatrix()
        glTranslatef(0.5*self.size, -0.5*self.size, self.size*0.3+Zshift)
        glRotatef(90, 0, 1, 0)
        glRotatef(self.wheelRotation, 0, 0, 1)
        self.wheel()
        glPopMatrix()

        # roue av droite
        glPushMatrix()
        glTranslatef(-0.5*self.size, -0.5*self.size, self.size*0.3+Zshift)
        glRotatef(-90, 0, 1, 0)
        glRotatef(-self.wheelRotation, 0, 0, 1)
        self.wheel()
        glPopMatrix()

        # roue ar gauche
        glPushMatrix()
        glTranslatef(0.5*self.size, -0.5*self.size, 1.6*self.size+Zshift)
        glRotatef(90, 0, 1, 0)
        glRotatef(self.wheelTurn, 0, 1, 0)
        glRotatef(self.wheelRotation, 0, 0, 1)
        self.wheel()
        glPopMatrix()

        # roue ar droite
        glPushMatrix()
        glTranslatef(-0.5*self.size, -0.5*self.size, 1.6*self.size+Zshift)
        glRotatef(-90, 0, 1, 0)
        glRotatef(self.wheelTurn, 0, 1, 0)
        glRotatef(-self.wheelRotation, 0, 0, 1)
        self.wheel()
        glPopMatrix()

        glPopMatrix()

    def bolt(self, radius, height):
        glColor3f(0.1, 0.1, 0.1)
        cylinder(radius, radius, height)

        glPushMatrix()
        disk(0, radius)
        glPopMatrix()

        glColor3f(0, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0, height)
        cylinder(1.3*radius, 1.3*radius, 0.1*height)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, height*1.1)
        disk(0, 1.3*radius)
        glPopMatrix()

    def wheel(self, boulons=5):
        inner = 0.1*self.size
        outer = 0.3*self.size
        boltLength = 0.15
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        torus(inner, outer, 15, 30)
        glPopMatrix()
        for i in range(boulons):
            glPushMatrix()
            glRotatef(i*360/boulons, 0, 0, 1)
            glTranslatef(0, (outer)/2, -boltLength)
            self.bolt(0.02*self.size, boltLength)
            glPopMatrix()
        

class Crane(Model):
    def __init__(self, size=1.0):
        Model.__init__(self, size)
        self.arm_angle = 30.0           # arm angle rotation
        self.forarm_angle = 30.0        # forarm angle rotation

    def set_arm_angle(self, angle):
        self.arm_angle = angle

    def get_arm_angle_arm(self):
        return self.arm_angle

    def set_forarm_angle(self, angle):
        self.forarm_angle = angle

    def get_forarm_angle(self):
        return self.forarm_angle

    def create(self):

        glPushMatrix()

        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-self.angle, 0, 1, 0)
        glColor3f(1.0, 0.0, 0.0)
        cube(self.size)

        glTranslatef(0, self.size*2, 0)
        glRotatef(-self.arm_angle, 1, 0, 0)
        glColor3f(1.0, 0.0, 0.0)
        sphere(self.size)

        glColor3f(0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.0, 0.7*self.size)
        cylinder(self.size*0.7, self.size*0.7, 3*self.size)

        glRotatef(-self.forarm_angle, 1, 0, 0)
        glTranslatef(0, 3*self.size*sin(-self.forarm_angle*pi/180), 3*self.size*cos(-self.forarm_angle*pi/180))
        glColor3f(1.0, 0.0, 0.0)
        sphere(self.size)

        glTranslatef(0, 0, 0.7*self.size)
        glColor3f(0.0, 1.0, 0.0)
        cylinder(0.7*self.size, 0.7*self.size, 3*self.size)

        glTranslatef(0, 0, 3*self.size)
        glColor3f(0.0, 0.0, 1.0)
        cone(self.size*1.3, self.size)

        glPopMatrix()

def display():
    size = 2.0
    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    posx, posy, posz = 2, 5, 10
    #posx, posy, posz = 0, 0, 5
    dirx, diry, dirz = 0, 0, 0
    vupx, vupy, vupz = 0, 1, 0
    gluLookAt(posx, posy, posz, dirx, diry, dirz, vupx, vupy, vupz)
    # scene creation  : begin
    floor(10*size)
    glPushMatrix()
    glColor3f(1.0, 0.0, 1.0)
    # glutSolidTeapot(self.size/5.0)
    Car(size)
    glPopMatrix()
    # scene creation  : end
    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fovy, ratio, near, far = 60.0, width*1.0/height, 0.1, 50.0
    gluPerspective(fovy, ratio, near, far)


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("REV OpenGL modeles")
    glClearColor(1.0, 1.0, 1.0, 1.0)
    dimension = 1.0
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()
