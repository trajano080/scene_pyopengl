# coding: utf-8

from math import pi, sin, cos, sqrt

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("Error: PyOpenGL not installed properly !!")
    sys.exit()

from primitives import wcs, floor
from models import Car, Crane


def gl_init():
    #  glClearColor(1.0,1.0,1.0,0.0);
    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)


def glut_init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutInitWindowSize(1200, 1000)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(sys.argv[0])


def glut_event(scene):
    glutDisplayFunc(scene.display)
    glutReshapeFunc(scene.reshape)
    glutKeyboardFunc(scene.on_keyboard_action)
    glutSpecialFunc(scene.on_special_key_action)
# glutIdleFunc(scene.animation)


class Scene:
    def __init__(self, size):
        self.firstTime = True
        self.theta_y = 45.0
        self.rho = sqrt(100)
        self.phi = 60*pi/180
        self.wcs_visible = True
        self.size = size
        self.car = Car(self.size)
        self.crane = Crane(self.size / 3.5)
        # self.crane = Crane(size)
        #self.camera = [0, 0, 5, 0, 0, 0, 0, 1, 0]
        #self.camera = [5, 5, 5, 0, 0, 0, 0, 1, 0]
        self.camera = [self.rho * sin(self.phi) * cos(self.theta_y), self.rho * cos(self.phi),
                       self.rho * sin(self.phi) * sin(self.theta_y), 0, 0, 0, 0, 1, 0]  # Camera perspective
        self.perspective = [60.0, 1.0, 0.1, 50.0]
        self.rotation_y = 0.0

        # Teapot initial state
        self.Teapot_position = [-3, 0.5, 3]
        self.Teapot_orientation = [45, 0, 1, 0]

    def set_initial_state(self):
        # Teapot
        self.Teapot_position0 = self.Teapot_position.copy()
        self.Teapot_orientation0 = self.Teapot_orientation.copy()

        # Car
        self.position0 = self.car.get_position()
        self.orientation0 = self.car.get_orientation()
        self.wheelTurn0 = self.car.get_wheel_turn()
        self.wheelRotation0 = self.car.get_wheel_rotation()

        # Crane
        self.arm_angle0 = self.crane.get_arm_angle_arm()
        self.forarm_angle0 = self.crane.get_forarm_angle()

    def display(self):
        gl_init()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        posx, posy, posz = self.camera[0], self.camera[1], self.camera[2]
        dirx, diry, dirz = self.camera[3], self.camera[4], self.camera[5]
        vupx, vupy, vupz = self.camera[6], self.camera[7], self.camera[8]
        gluLookAt(posx, posy, posz, dirx, diry, dirz, vupx, vupy, vupz)
        glRotatef(self.rotation_y, 0, 1, 0)
        if self.wcs_visible:
            wcs(self.size/2)
        floor(10*self.size)

        # Object to catch
        glPushMatrix()
        glTranslatef(
            self.Teapot_position[0], self.Teapot_position[1], self.Teapot_position[2])
        glRotatef(self.Teapot_orientation[0], self.Teapot_orientation[1],
                  self.Teapot_orientation[2], self.Teapot_orientation[3])
        glColor3f(1.0, 0.0, 1.0)
        glutSolidTeapot(self.size/5.0)
        glPopMatrix()

        # model to control
        glPushMatrix()
        glTranslatef(0, self.car.get_size()*0.8, 0)
        self.car.create()
        glTranslatef(0, self.car.get_size()/2, 0)
        self.crane.create()
        glPopMatrix()
        glutSwapBuffers()

        # To save the initial state of each object in the scene
        if self.firstTime:
            self.firstTime = False
            self.set_initial_state()

    def setCamera(self):
        self.camera = [self.rho * sin(self.phi) * cos(self.theta_y), self.rho * cos(self.phi),
                       self.rho * sin(self.phi) * sin(self.theta_y), 0, 0, 0, 0, 1, 0]

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.perspective[1] = width*1.0/height
        fovy, ratio, near, far = self.perspective
        gluPerspective(fovy, ratio, near, far)

    def on_keyboard_action(self, key, x, y):
        if key == b'a':
            glutIdleFunc(scene.animation)
        elif key == b'A':
            glutIdleFunc(None)
        elif key == b'h':
            print("----------------------------------------")
            print("Documentation Interaction  : LOPEZ Valentin et MENA Trajano")
            print("h : afficher cette aide")
            print("----------------------------------------")
            print("---------")
            print("Affichage")
            print("---------")
            print("a/A : lancer/Stopper l'animation")
            print("c/C : faces CW/CCW")
            print("f/F : faces/Aretes")
            print("r/R : redimensionner tous les objets")
            print("k/K : redimensioner le car")
            print("j/J : redimensioner le crane")
            print("i : etat initial de la scene")
            print("w/W : repere de scene visible/invisible")
            print("------")
            print("Camera")
            print("------")
            print("y/Y : tourner l'objet autour de l'axe Oy\n")
            print(
                "z/Z : d??placer la cam??ra pour se rapprocher, s'??loigner du centre de la sc??ne\n")
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

        elif key == b'b':
            self.crane.set_arm_angle(self.crane.get_arm_angle_arm() - 2)
        elif key == b'B':
            self.crane.set_arm_angle(self.crane.get_arm_angle_arm() + 2)
        elif key == b'c':
            glFrontFace(GL_CW)
        elif key == b'C':
            glFrontFace(GL_CCW)
        elif key == b'e':
            pass
        elif key == b'f':
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif key == b'F':
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif key == b'g':
            self.crane.set_forarm_angle(self.crane.get_forarm_angle() - 2)
        elif key == b'G':
            self.crane.set_forarm_angle(self.crane.get_forarm_angle() + 2)
        elif key == b'i':

            # Teapot reset
            self.Teapot_position = self.Teapot_position0
            self.Teapot_orientation = self.Teapot_orientation0

            # Car reset
            self.car.set_position(self.position0)
            self.car.set_orientation(self.orientation0)
            self.car.set_wheel_turn(self.wheelTurn0)
            self.car.set_wheel_rotation(self.wheelRotation0)
            self.crane.set_position(self.position0)
            self.crane.set_orientation(self.orientation0)
            self.crane.set_forarm_angle(self.forarm_angle0)
            self.crane.set_arm_angle(self.arm_angle0)
        elif key == b'n':
            pass
        elif key == b'N':
            pass
        elif key == b's':
            pass
        elif key == b'u':
            pass
        elif key == b'U':
            pass
        elif key == b'v':
            pass
        elif key == b'V':
            pass
        elif key == b'r':
            self.car.set_size(self.car.get_size() + 0.1)
            self.crane.set_size(self.crane.get_size() + 0.1/3)
        elif key == b'R':
            self.car.set_size(self.car.get_size() - 0.1)
            self.crane.set_size(self.crane.get_size() - 0.1/3)
        elif key == b'k':
            self.car.set_size(self.car.get_size() + 0.1)
        elif key == b'K':
            self.car.set_size(self.car.get_size() - 0.1)
        elif key == b'j':
            self.crane.set_size(self.crane.get_size() + 0.1/3)
        elif key == b'J':
            self.crane.set_size(self.crane.get_size() - 0.1/3)
        elif key == b'w':
            self.wcs_visible = False
        elif key == b'W':
            self.wcs_visible = True
        elif key == b'y':
            self.theta_y -= 1.0*pi/180
        elif key == b'Y':
            self.theta_y += 1.0*pi/180
        elif key == b'z':
            self.rho -= 0.05
        elif key == b'Z':
            self.rho += 0.05
        else:
            pass

        self.setCamera()
        glutPostRedisplay()

    def on_mouse_action(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                print("button down")
            else:
                print("button up")
        else:
            pass
        glutPostRedisplay()

    def on_special_key_action(self, key, x, y):
        position = self.car.get_position()
        orientation = self.car.get_orientation()
        wheelTurn = self.car.get_wheel_turn()
        wheelRotation = self.car.get_wheel_rotation()
        if key == GLUT_KEY_UP:
            position[0] += 0.1*self.size*sin(orientation*pi/180.0)
            position[2] += 0.1*self.size*cos(orientation*pi/180.0)
            wheelRotation += 5
            if wheelTurn > 0:
                wheelTurn -= 10
            elif wheelTurn < 0:
                wheelTurn += 10
        elif key == GLUT_KEY_DOWN:
            position[0] -= 0.1*self.size*sin(orientation*pi/180.0)
            position[2] -= 0.1*self.size*cos(orientation*pi/180.0)
            wheelRotation -= 5
            if wheelTurn > 0:
                wheelTurn -= 10
            elif wheelTurn < 0:
                wheelTurn += 10
        elif key == GLUT_KEY_LEFT:
            orientation += 5
            wheelRotation = 0
            if wheelTurn <= 30:
                wheelTurn += 10
        elif key == GLUT_KEY_RIGHT:
            orientation -= 5
            wheelRotation = 0
            if wheelTurn >= -30:
                wheelTurn -= 10
        else:
            pass
        self.car.set_position(position)
        self.car.set_orientation(orientation)
        self.car.set_wheel_turn(wheelTurn)
        self.car.set_wheel_rotation(wheelRotation)
        self.crane.set_position(position)
        self.crane.set_orientation(-orientation)
        glutPostRedisplay()

    def animation(self):
        self.rotation_y += 0.1
        if self.rotation_y > 360.0:
            self.rotation_y -= 360
        glutPostRedisplay()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("REV OpenGL scene")
    glClearColor(1.0, 1.0, 1.0, 1.0)
    dimension = 2.0
    scene = Scene(dimension)
    glut_event(scene)
    glutMainLoop()
