from math import pi
# pygame Constants
FREQUENCY = 60
SAMPLE_TIME = 1/FREQUENCY
WINDOW_HEIGHT = 720
WINDOW_LENGTH = 1280
M2PIX = 1000
BLACK = 0, 0, 0
DARK_GRAY = 96, 96, 96
LIGHT_GRAY = 216, 216, 216
RED = 255, 0, 0
PIX_BORDER_GAP = 10
PIX_TAB_GAP = round(WINDOW_LENGTH*0.2)
# Unit Conversion
KILO2GRAM = 1000.0
METRE2CENTI = 100.0
DRAG_B_SI2CGS = 10000000.0
RADIAN2DEGREES = 180.0/pi
# Physics Limits and Deltas
MAX_GRAVITY = 15 # m/s^2
MIN_GRAVITY = 0 # m/s^2
MAX_DRAG = 0.001 # N m / (1/s)^2
MIN_DRAG = 0.0 # N m / (1/s)^2
MAX_MASS = 0.100 # kg
MIN_MASS = 0.001 # kg
MAX_LENGTH = 0.50 # m
MIN_LENGTH = 0.01 # m
MAX_WIDTH = 0.50 # m
MIN_WIDTH = 0.001 #m
MAX_PIVOT_RATIO = 0.50
MIN_PIVOT_RATIO = 0.00
MAX_AMPLITUDE = pi # rad
MIN_AMPLITUDE = -pi # rad
DELTA = [0.05, 0.000001, 0.0005, 0.005, 0.0005, 0.005, 1.0/RADIAN2DEGREES] # gravity, drag, mass, length, width, pivot, amplitude