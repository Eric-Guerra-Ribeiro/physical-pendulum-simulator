import pygame
import math
import matplotlib.pyplot as plt
import numpy as np
from constants import *

# Physics Variables
gravity_acceleration = 9.7838163 # m/s^2
drag_b = 0.000153 # N m / (1/s)^2 
bar_mass = 0.024 # kg
bar_length = 0.31 # m
bar_width = 0.03 # m
pivot_ratio = 3.5/31.0 # from top to pivot/full length
pivot_to_cm = bar_length*math.fabs(pivot_ratio -0.5) # distance from pivot to the centre of mass (m)
bar_moment_of_inertia = bar_mass*(bar_length**2 + bar_width**2)/12 + bar_mass*pivot_to_cm**2 # steiner theorem (kg m^2)
amplitude = 0.3526803798#pi/2 #rad
theta = [amplitude, amplitude, amplitude] # theta t-1 , theta t, theta t+1 (rad)
time = 0 # s

# Arrays for Plotting
theta_history = []
angular_velocity_history = []
angular_acceleration_history = []
# Physics Functions
def get_acceleration():
    '''
    Obtains the angular acceleration of the pendulum using Newton's Second Law with the resultant momentum.

    :return: angular acceleration
    :rtype: float
    '''
    global angular_velocity_history
    global angular_acceleration_history
    angular_velocity = (theta[2] - theta[0])/(2*SAMPLE_TIME)
    drag = drag_b*angular_velocity*math.fabs(angular_velocity)
    angular_acceleration = -((bar_mass*gravity_acceleration*pivot_to_cm*math.sin(theta[1])) + (drag))/bar_moment_of_inertia
    angular_velocity_history.append(angular_velocity)
    angular_acceleration_history.append(angular_acceleration)
    return angular_acceleration


def stormer_verlet():
    '''
    Applies the Störmer-Verlet Integration.
    '''
    global theta
    global theta_history
    theta[0] = theta[1]
    theta[1] = theta[2]
    theta[2] = 2*theta[1] - theta[0] + get_acceleration()*SAMPLE_TIME**2
    theta_history.append(theta[1])


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulador Pêndulo Físico - Fis26L - Grupo 6 T1")
icon = pygame.image.load("pendulum.png") # Icons made by www.freepik.com
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

# Pygame Auxiliary Variables
pivot_coord = [WINDOW_LENGTH/2, WINDOW_HEIGHT/2]
ins_p_size = font.size("P: Plot graphs")[0]
ins_space_size = font.size("Space: Pause/Unpause")[1]
ins_esc_size = font.size("Esc: Change parameters")
ino_ud_size = font.size("Up/Down: Select another parameter")[1]
ino_lr_size = font.size("Left/Right: Change parameter value")
default_height = ins_space_size
line_spacing = round((WINDOW_HEIGHT-2*PIX_BORDER_GAP-9*default_height)/8)


def reset_simulation():
    '''
    Resets the simulations parameters.
    '''
    global theta
    global time
    global theta_history
    global angular_velocity_history
    global angular_acceleration_history
    theta = [amplitude, amplitude, amplitude]
    time = 0
    theta_history = []
    angular_velocity_history = []
    angular_acceleration_history = []


def change_parameters(option, delta):
    '''
    Changes the parameters.

    :param option: number from 0 to 6 indicating the selected parameter
    :type option: int
    :param delta: number indicating the rate of change of the parameter
    :type delta: float
    '''
    global gravity_acceleration
    global drag_b
    global bar_mass
    global bar_length
    global bar_width
    global pivot_ratio
    global amplitude
    if option == 0:
        gravity_acceleration = min(MAX_GRAVITY, max(MIN_GRAVITY, gravity_acceleration + delta))
    elif option == 1:
        drag_b = min(MAX_DRAG, max(MIN_DRAG, drag_b + delta))
    elif option == 2:
        bar_mass = min(MAX_MASS, max(MIN_MASS, bar_mass + delta))
    elif option == 3:
        bar_length = min(MAX_LENGTH, max(MIN_LENGTH, bar_length + delta))
    elif option == 4:
        bar_width = min(MAX_WIDTH, max(MIN_WIDTH, bar_width + delta))
    elif option == 5:
        pivot_ratio = min(MAX_PIVOT_RATIO, max(MIN_PIVOT_RATIO, pivot_ratio + delta))
    elif option == 6:
        amplitude = min(MAX_AMPLITUDE, max(MIN_AMPLITUDE, amplitude + delta))


# Coordinates Managment
def get_top_coordinates():
    '''
    Obtains the coordinates of the top  of the bar, when it rotates theta[1] from the pivot point.

    :return: the (x, y) coordinates of the top of the bar 
    :rtype: float list
    '''
    aux_length = bar_length*pivot_ratio*M2PIX
    return [pivot_coord[0] + aux_length*math.sin(theta[1]), pivot_coord[1] - aux_length*math.cos(theta[1])]


def get_bottom_coordinates():
    '''
    Obtains the coordinates of bottom top  of the bar, when it rotates theta[1] from the pivot point.
    
    :return: the (x, y) coordinates of the bottom of the bar 
    :rtype: float list
    '''
    aux_length = bar_length*(1.0 - pivot_ratio)*M2PIX
    return [pivot_coord[0] - aux_length*math.sin(theta[1]), pivot_coord[1] + aux_length*math.cos(theta[1])]


def get_rectangle_points():
    '''
    Obtains the coordinates of the four corners of the bar (a rectangle), when it rotates theta[1] from the pivot point.

    :return: a list with the (x, y) coordinates of each of the points
    :rtype: float tuples list
    '''
    top = get_top_coordinates()
    bottom = get_bottom_coordinates()
    length = M2PIX*bar_width/2
    len_cos = length*math.cos(theta[1])
    len_sin = length*math.sin(theta[1])
    return [(top[0]-len_cos, top[1]-len_sin), (top[0]+len_cos, top[1]+len_sin),
    (bottom[0]+len_cos, bottom[1]+len_sin), (bottom[0]-len_cos, bottom[1]-len_sin)]


# Drawing and Printing
def draw_bar():
    '''
    Draws the bar at an angle of theta[1], the pivot and a red dot on its extremity.
    '''
    pygame.draw.polygon(screen, LIGHT_GRAY, get_rectangle_points())
    pygame.draw.circle(screen, DARK_GRAY, pivot_coord, M2PIX*bar_width/8)
    pygame.draw.circle(screen, RED, get_bottom_coordinates(), M2PIX*bar_width/10)


def print_instructions_simulator():
    '''
    Prints what each hotkey does in the simulador.
    '''
    ins_r = font.render("R: Reset simulation", True, LIGHT_GRAY)
    ins_p = font.render("P: Plot graphs", True, LIGHT_GRAY)
    ins_space = font.render("Space: Pause/Unpause", True, LIGHT_GRAY)
    ins_esc = font.render("Esc: Change parameters", True, LIGHT_GRAY)
    screen.blit(ins_r, (10, 10))
    screen.blit(ins_p, (WINDOW_LENGTH-10-ins_p_size,10))
    screen.blit(ins_space, (10, WINDOW_HEIGHT-10-ins_space_size))
    screen.blit(ins_esc, (WINDOW_LENGTH-10-ins_esc_size[0], WINDOW_HEIGHT-10-ins_esc_size[1]))


def print_instructions_options():
    '''
    Prints what each hotkey does in the options menu.
    '''
    ino_ud = font.render("Up/Down: Select another parameter", True, LIGHT_GRAY)
    ino_lr = font.render("Left/Right: Change parameter value", True, LIGHT_GRAY)
    ino_esc = font.render("Esc: Simulator", True, LIGHT_GRAY)
    screen.blit(ino_ud, (PIX_BORDER_GAP, WINDOW_HEIGHT-PIX_BORDER_GAP-ino_ud_size))
    screen.blit(ino_lr, (WINDOW_LENGTH-PIX_BORDER_GAP-ino_lr_size[0], WINDOW_HEIGHT-PIX_BORDER_GAP-ino_lr_size[1]))
    screen.blit(ino_esc, (PIX_BORDER_GAP, PIX_BORDER_GAP))


def print_parameters():
    '''
    Prints the current values of the parameters and its limits and units.
    '''
    text_gravity = font.render("Gravity Acceleration (m/s^2): {:.2f} ({:.2f}<g<{:.2f}) "
    .format(gravity_acceleration, MIN_GRAVITY, MAX_GRAVITY), True, LIGHT_GRAY)
    text_drag = font.render("Drag Factor (dyn cm s^2): {:.0f} ({:.0f}<b<{:.0f})"
    .format(DRAG_B_SI2CGS*drag_b, DRAG_B_SI2CGS*MIN_DRAG, DRAG_B_SI2CGS*MAX_DRAG), True, LIGHT_GRAY)
    text_mass = font.render("Bar Mass (g): {:.1f} ({:.1f}<m<{:.1f})"
    .format(KILO2GRAM*bar_mass, KILO2GRAM*MIN_MASS, KILO2GRAM*MAX_MASS), True, LIGHT_GRAY)
    text_length = font.render("Bar Length (cm): {:.1f} ({:.1f}<l<{:.1f})"
    .format(METRE2CENTI*bar_length, METRE2CENTI*MIN_LENGTH, METRE2CENTI*MAX_LENGTH), True, LIGHT_GRAY)
    text_width = font.render("Bar Width (cm): {:.2f} ({:.2f}<w<{:.2f})"
    .format(METRE2CENTI*bar_width, METRE2CENTI*MIN_WIDTH, METRE2CENTI*MAX_WIDTH), True, LIGHT_GRAY)
    text_pivot = font.render("Distance to Pivot (cm): {:.1f} ({:.1f}<p<{:.1f})"
    .format(METRE2CENTI*bar_length*pivot_ratio, METRE2CENTI*bar_length*MIN_PIVOT_RATIO, METRE2CENTI*bar_length*MAX_PIVOT_RATIO), True, LIGHT_GRAY)
    text_amplitude= font.render("Initial Amplitude (º): {:.0f} ({:.0f}<A<{:.0f})"
    .format(RADIAN2DEGREES*amplitude, RADIAN2DEGREES*MIN_AMPLITUDE, RADIAN2DEGREES*MAX_AMPLITUDE), True, LIGHT_GRAY)
    base = PIX_BORDER_GAP+default_height+line_spacing
    screen.blit(text_gravity, (PIX_TAB_GAP, base))
    screen.blit(text_drag, (PIX_TAB_GAP, base+(default_height+line_spacing)))
    screen.blit(text_mass, (PIX_TAB_GAP, base+2*(default_height+line_spacing)))
    screen.blit(text_length, (PIX_TAB_GAP, base+3*(default_height+line_spacing)))
    screen.blit(text_width, (PIX_TAB_GAP, base+4*(default_height+line_spacing)))
    screen.blit(text_pivot, (PIX_TAB_GAP, base+5*(default_height+line_spacing)))
    screen.blit(text_amplitude, (PIX_TAB_GAP, base+6*(default_height+line_spacing)))


def show_chosen(option):
    '''
    Draws a red circle next to the selected option.

    :param option: number from 0 to 6 indicating the selected option
    :type option: int
    '''
    radius = default_height/4
    base = PIX_BORDER_GAP+default_height+line_spacing
    pygame.draw.circle(screen, RED, (PIX_TAB_GAP - 2*radius, base + option*(default_height+line_spacing) + 0.5*default_height), radius)


# Options Menu
def options_menu():
    '''
    Brings an option menu to change the parameters.

    :return: if the user clicked quit while in the options menu
    :rtype: bool
    '''
    option = 0
    delta = 0
    running = True
    while running:
        clock.tick(FREQUENCY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    option = (option+6)%7
                elif event.key == pygame.K_DOWN:
                    option = (option+1)%7
                elif event.key == pygame.K_RIGHT:
                    delta = DELTA[option]
                elif event.key == pygame.K_LEFT:
                    delta = - DELTA[option]
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    delta = 0
        screen.fill(BLACK)
        print_instructions_options()
        print_parameters()
        show_chosen(option)
        change_parameters(option, delta)
        pygame.display.flip()
    return False


# Plot Graphs
def plot():
    '''
    Plots the graphs for angle, angular velocity and angular acceleration
    '''
    number_points = len(theta_history)
    time_history = np.linspace(0, time, number_points)
    with open("theta.txt", 'w' ,encoding = 'utf-8') as file:
        for i in theta_history:
            file.write("{}\n".format(i*180/pi))
    with open("time.txt", 'w' ,encoding = 'utf-8') as file:
        for i in time_history:
            file.write("{}\n".format(i))
    plt.figure()
    plt.plot(time_history, theta_history)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.title('Angle versus Time')
    plt.grid()
    plt.figure()
    plt.plot(time_history, angular_velocity_history)
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.title('Angular Velocity versus Time')
    plt.grid()
    plt.figure()
    plt.plot(time_history, angular_acceleration_history)
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Acceleration (rad/s^2)')
    plt.title('Angular Acceleration Time')
    plt.grid()
    plt.show()


# Simulation Loop
paused = True
running = True
while running:
    clock.tick(FREQUENCY)
    screen.fill(BLACK)
    draw_bar()
    print_instructions_simulator()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                reset_simulation()
                paused = True
            elif event.key == pygame.K_ESCAPE:
                running = not options_menu()
                reset_simulation()
                paused = True
            elif event.key == pygame.K_p:
                plot()
                paused = True
    if not paused:
        stormer_verlet()
        time += SAMPLE_TIME

pygame.quit()