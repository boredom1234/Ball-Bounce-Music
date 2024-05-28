import pygame
import sys
import math
import mido
import pygame.midi


pygame.init()
pygame.midi.init()


screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing_Balls_Midi")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIME = (0, 255, 0)
TEAL = (0, 128, 128)
PINK = (255, 192, 203)
LAVENDER = (230, 230, 250)
MAROON = (128, 0, 0)
NAVY = (0, 0, 128)
OLIVE = (128, 128, 0)
INDIGO = (75, 0, 130)
TURQUOISE = (64, 224, 208)
SLATE = (112, 128, 144)
SALMON = (250, 128, 114)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
SKY_BLUE = (135, 206, 235)
FOREST_GREEN = (34, 139, 34)


circle_center = (screen_width // 2, screen_height // 2)
circle_radius = 100


ball_radius = 5
ball_pos = [circle_center[0], circle_center[1] - circle_radius + ball_radius]
ball_velocity = [2, 2]


midi_file = mido.MidiFile(
    'your_midi_file_path_here')
midi_notes = [msg for msg in midi_file if msg.type == 'note_on']
note_index = 0


midi_out = pygame.midi.Output(pygame.midi.get_default_output_id())


def check_collision_and_bounce(ball_pos, ball_velocity, circle_center, circle_radius, ball_radius):
    global note_index
    distance = math.sqrt(
        (ball_pos[0] - circle_center[0]) ** 2 + (ball_pos[1] - circle_center[1]) ** 2)
    if distance + ball_radius > circle_radius:

        nx = (ball_pos[0] - circle_center[0]) / distance
        ny = (ball_pos[1] - circle_center[1]) / distance
        dot_product = ball_velocity[0] * nx + ball_velocity[1] * ny
        ball_velocity[0] -= 2 * dot_product * nx
        ball_velocity[1] -= 2 * dot_product * ny

        overlap = (distance + ball_radius) - circle_radius
        ball_pos[0] -= overlap * nx
        ball_pos[1] -= overlap * ny

        if note_index < len(midi_notes):
            note = midi_notes[note_index]
            midi_out.note_on(note.note, note.velocity)
            note_index += 1

        return True
    return False


def check_explosion(ball_radius, circle_radius):
    if ball_radius > circle_radius:
        return True
    return False


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    if check_collision_and_bounce(ball_pos, ball_velocity, circle_center, circle_radius, ball_radius):
        ball_radius += 0

    if check_explosion(ball_radius, circle_radius):
        running = False

    screen.fill(BLACK)

    pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 2)

    pygame.draw.circle(
        screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
