
"""Real-Time Fluid Dynamics for Games by Jos Stam (2003).
Parts of author's work are also protected
under U. S. patent #6,266,071 B1 [Patent].

Original paper by Jos Stam, "Real-Time Fluid Dynamics for Games".
Proceedings of the Game Developer Conference, March 2003

http://www.dgp.toronto.edu/people/stam/reality/Research/pub.html

Tested on
  python 2.4
  numarray 1.1.1
  PyOpenGL-2.0.2.01.py2.4-numpy23
  glut-3.7.6

How to use this demo:
  Add densities with the right mouse button
  Add velocities with the left mouse button and dragging the mouse
  Toggle density/velocity display with the 'v' key
  Clear the simulation by pressing the 'c' key

(porting by Alberto Santini)
"""

from numpy import zeros, float64
from solver import vel_step, dens_step
from kelvin_table import kelvin_table

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print('ERROR: PyOpenGL not installed properly.')
    exit(1)

N = 64 # resolution
size = N + 2 # size of grid and data

dt = 0.1 # time step
diff = 0.0 # diffusion
visc = 0.0 # viscosity
force = 5.0 # scale for mouse movement 
source = 100.0 # density
dvel = False # display velocity instead of density

win_x = 1024 # window width
win_y = 512 # window height

omx = 0.0 # old mouse x
omy = 0.0 # old mouse y
mx = 0.0 # mouse x
my = 0.0 # mouse y
mouse_down = [False, False, False] # mouse button callbacks

""" Start with two grids.
One that contains the density values from the previous time step and one that
will contain the new values. For each grid cell of the latter we trace the
cell's center position backwards through the velocity field. We then linearly
interpolate from the grid of previous density values and assign this value to
the current grid cell.
"""
u = zeros((size, size), float64)  # velocity
u_prev = zeros((size, size), float64)
v = zeros((size, size), float64)  # velocity
v_prev = zeros((size, size), float64)
dens = zeros((size, size), float64)  # density
dens_prev = zeros((size, size), float64)
temperature = 3400


def clear_data():
    """clear_data."""

    global u, v, u_prev, v_prev, dens, dens_prev, size

    u[0:size, 0:size] = 0.0
    v[0:size, 0:size] = 0.0
    u_prev[0:size, 0:size] = 0.0
    v_prev[0:size, 0:size] = 0.0
    dens[0:size, 0:size] = 0.0
    dens_prev[0:size, 0:size] = 0.0


def pre_display():
    """pre_display."""

    glViewport(0, 0, win_x, win_y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


def post_display():
    """post_display."""

    glutSwapBuffers()


def draw_velocity():
    """draw_velocity."""

    h = 1.0 / N

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.0)

    glBegin(GL_LINES)
    for i in range(1, N + 1):
        x = (i - 0.5) * h
        for j in range(1, N + 1):
            y = (j - 0.5) * h
            glColor3f(1, 0, 0)
            glVertex2f(x, y)
            glVertex2f(x + u[i, j], y + v[i, j])
    glEnd()


def draw_density():
    """draw_density."""

    global temperature

    h = 1.0 / N

    glBegin(GL_QUADS)
    for i in range(0, N + 1):
        x = (i - 0.5) * h
        for j in range(0, N + 1):
            y = (j - 0.5) * h
            d00 = dens[i, j]
            d01 = dens[i, j + 1]
            d10 = dens[i + 1, j]
            d11 = dens[i + 1, j + 1]

            glColor3f(d00, d00, d00)
            glVertex2f(x, y)
            glColor3f(d10, d10, d10)
            glVertex2f(x + h, y)
            glColor3f(d11, d11, d11)
            glVertex2f(x + h, y + h)
            glColor3f(d01, d01, d01)
            glVertex2f(x, y + h)
    glEnd()


def get_from_UI(d, u, v):
    """get_from_UI."""

    global omx, omy

    d[0:size, 0:size] = 0.0
    u[0:size, 0:size] = 0.0
    v[0:size, 0:size] = 0.0

    if not mouse_down[GLUT_LEFT_BUTTON] and not mouse_down[GLUT_RIGHT_BUTTON]:
        return

    i = int((mx / float(win_x)) * N + 1)
    j = int(((win_y - float(my)) / float(win_y)) * float(N) + 1.0)

    if i < 1 or i > N or j < 1 or j > N:
        return

    if mouse_down[GLUT_LEFT_BUTTON]:
        u[i, j] = force * (mx - omx)
        v[i, j] = force * (omy - my)

    if mouse_down[GLUT_RIGHT_BUTTON]:
        d[i, j] = source

    omx = mx
    omy = my


def key_func(key, x, y):
    """key_func."""

    global dvel

    if key == 'c' or key == 'C':
        clear_data()
    if key == 'v' or key == 'V':
        dvel = not dvel


def mouse_func(button, state, x, y):
    """mouse_func."""

    global omx, omy, mx, my, mouse_down

    omx = mx = x
    omy = my = y
    mouse_down[button] = (state == GLUT_DOWN)


def motion_func(x, y):
    """motion_func."""

    global mx, my

    mx = x
    my = y


def reshape_func(width, height):
    """reshape_func."""

    global win_x, win_y

    glutReshapeWindow(width, height)
    win_x = width
    win_y = height


def idle_func():
    """idle_func."""

    global dens, dens_prev, u, u_prev, v, v_prev, N, visc, dt, diff

    for i in range(20, 30):
        dens[10, i] = 1
        u[10, i] = 1


    get_from_UI(dens_prev, u_prev, v_prev)
    vel_step(N, u, v, u_prev, v_prev, visc, dt)
    dens_step(N, dens, dens_prev, u, v, diff, dt)

    glutPostRedisplay()


def display_func():
    """display_func."""

    pre_display()
    if dvel:
        draw_velocity()
    else:
        draw_density()
    post_display()


def open_glut_window():
    """open_glut_window."""

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(win_x, win_y)
    glutCreateWindow("Rocket Engine Simulation")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

    pre_display()

    glutKeyboardFunc(key_func)
    glutMouseFunc(mouse_func)
    glutMotionFunc(motion_func)
    glutReshapeFunc(reshape_func)
    glutIdleFunc(idle_func)
    glutDisplayFunc(display_func)


if __name__ == '__main__':
    glutInit(sys.argv)
    clear_data()
    open_glut_window()
    glutMainLoop()