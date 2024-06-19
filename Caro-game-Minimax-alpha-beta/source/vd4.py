import pygame
import math

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Tic Tac Toe")
def draw_grid():
    line_width = 10
    pygame.draw.line(screen, (255, 255, 255), (133, 0), (133, 400), line_width)
    pygame.draw.line(screen, (255, 255, 255), (266, 0), (266, 400), line_width)
    pygame.draw.line(screen, (255, 255, 255), (0, 133), (400, 133), line_width)
    pygame.draw.line(screen, (255, 255, 255), (0, 266), (400, 266), line_width)
def draw_X(x, y):
    line_width = 10
    padding = 20
    pygame.draw.line(screen, (255, 0, 0), (x+padding, y+padding), (x+133-padding, y+133-padding), line_width)
    pygame.draw.line(screen, (255, 0, 0), (x+133-padding, y+padding), (x+padding, y+133-padding), line_width)

def draw_O(x, y):
    line_width = 10
    padding = 20
    pygame.draw.circle(screen, (0, 0, 255), (x+67, y+67), 50, line_width)
def get_row_col_from_mouse_pos(pos):
    x, y = pos
    if x < 133:
        col = 0
    elif x < 266:
        col = 1
    else:
        col = 2
    if y < 133:
        row = 0
    elif y < 266:
        row = 1
    else:
        row = 2
    return row, col

board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
player = 'X'
opponent = 'O'
def handle_click(board, row, col, player):
    if board[row*3+col] == ' ':
        board[row*3+col] = player
        return True
    return False
# Hàm để kiểm tra trạng thái hiện tại của bàn cờ
def is_full():
    for i in range(9):
        if board[i] == ' ':
            return False
    return True

# Hàm để kiểm tra xem có người chiến thắng hay không
def check_win(board, player):
    if (
        (board[0] == player and board[1] == player and board[2] == player) or
        (board[3] == player and board[4] == player and board[5] == player) or
        (board[6] == player and board[7] == player and board[8] == player) or
        (board[0] == player and board[3] == player and board[6] == player) or
        (board[1] == player and board[4] == player and board[7] == player) or
        (board[2] == player and board[5] == player and board[8] == player) or
        (board[0] == player and board[4] == player and board[8] == player) or
        (board[2] == player and board[4] == player and board[6] == player)
    ):
        return True
    return False

# Hàm để tính điểm của nước đi
def evaluate(board):
    if check_win(board, player):
        return 10
    elif check_win(board, opponent):
        return -10
    else:
        return 0

# Hàm minimax
def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if is_full():
        return 0
    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = opponent
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Hàm để thực hiện nước đi tốt nhất
def get_best_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move
# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse_pos(pos)
            if handle_click(board, row, col, player):
                if player == 'X':
                    player = 'O'
                else:
                    player = 'X'
                if not check_win(board, player) and not is_full():
                    best_move = get_best_move(board)
                    row = best_move // 3
                    col = best_move % 3
                    handle_click(board, row, col, player)
                    if player == 'X':
                        player = 'O'
                    else:
                        player = 'X'
    draw_grid()


