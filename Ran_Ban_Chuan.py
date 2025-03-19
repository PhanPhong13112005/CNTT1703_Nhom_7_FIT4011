import pygame
import sys
import random
import heapq

# Khởi tạo pygame
pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 800, 500
CELL_SIZE = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 SNAKE GAME AI 🕹️")

# Màu sắc nền tối và neon
BACKGROUND_COLOR = (20, 20, 20)
BUTTON_COLOR = (30, 30, 30)
BUTTON_HOVER_COLOR = (50, 50, 50)
TEXT_COLOR = (0, 255, 200)
TITLE_COLOR = (100, 200, 255)
SNAKE_COLOR = (0, 200, 0)
FOOD_COLOR = (255, 50, 50)

# Load font
font_title = pygame.font.SysFont("Arial", 60, bold=True)
font_button = pygame.font.SysFont("Arial", 36, bold=True)
font_score = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()

def draw_text(text, x, y, font, color, center=False):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y) if center else (x, y))
    screen.blit(text_surface, rect)

# Thuật toán A* tìm đường đi tối ưu
class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = self.h = self.f = 0
    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)
        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current_node.position[0] + dx * CELL_SIZE, current_node.position[1] + dy * CELL_SIZE)
            if neighbor_pos in closed_set or neighbor_pos in obstacles or not (0 <= neighbor_pos[0] < WIDTH and 0 <= neighbor_pos[1] < HEIGHT):
                continue
            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_pos, goal)
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            heapq.heappush(open_list, neighbor_node)
    return None

def game_loop():
    snake = [(100, 50), (90, 50), (80, 50)]
    food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    score = 0
    running = True
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        path = a_star(snake[0], food, set(snake))
        if path and len(path) > 1:
            direction = (path[1][0] - snake[0][0], path[1][1] - snake[0][1])
        else:
            running = False
        
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head == food:
            food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
            score += 10
        else:
            snake.pop()
        
        if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            running = False
        
        snake.insert(0, new_head)
        for part in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (*part, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, FOOD_COLOR, (*food, CELL_SIZE, CELL_SIZE))
        
        draw_text(f"Score: {score}", WIDTH // 2, 20, font_score, TEXT_COLOR, center=True)
        pygame.display.flip()
        clock.tick(10)

def main_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text("SNAKE GAME AI", WIDTH // 2, HEIGHT // 10, font_title, TITLE_COLOR, center=True)
        play_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 60)
        quit_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 40, 300, 60)
        pygame.draw.rect(screen, BUTTON_COLOR, play_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_COLOR, quit_rect, border_radius=10)
        draw_text("Start", WIDTH // 2, HEIGHT // 2 - 30, font_button, TEXT_COLOR, center=True)
        draw_text("Quit", WIDTH // 2, HEIGHT // 2 + 70, font_button, TEXT_COLOR, center=True)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game_loop()
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
