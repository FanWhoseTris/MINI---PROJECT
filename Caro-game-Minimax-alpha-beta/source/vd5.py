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
def evaluate(board):
    # Kiểm tra các hàng
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == 'X':
                return 1  # Máy thắng
            elif board[row][0] == 'O':
                return -1  # Người thắng

    # Kiểm tra các cột
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 'X':
                return 1  # Máy thắng
            elif board[0][col] == 'O':
                return -1  # Người thắng

    # Kiểm tra đường chéo chính
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return 1  # Máy thắng
        elif board[0][0] == 'O':
            return -1  # Người thắng

    # Kiểm tra đường chéo phụ
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'X':
            return 1  # Máy thắng
        elif board[0][2] == 'O':
            return -1  # Người thắng

    # Trạng thái hòa
    return 0
def minimax(board, depth, maximizing_player):
    # Đánh giá và trả về điểm tương ứng cho bàn cờ hiện tại
    score = evaluate(board)

    if score != 0:
        return score

    if is_full(board):
        return 0

    if maximizing_player:
        max_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = '-'
                    max_score = max(score, max_score)
        return max_score

    else:
        min_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = '-'
                    min_score = min(score, min_score)
        return min_score

def find_best_move(board):
    best_score = -math.inf
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = 'X'
                score = minimax(board, 0, False)
                board[i][j] = '-'
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move
def cpu_won(board):
    # Kiểm tra các hàng
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == 'O':
            return True

    # Kiểm tra các cột
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == 'O':
            return True

    # Kiểm tra đường chéo chính
    if board[0][0] == board[1][1] == board[2][2] == 'O':
        return True

    # Kiểm tra đường chéo phụ
    if board[0][2] == board[1][1] == board[2][0] == 'O':
        return True

    return False
def user_won(board):
    # Kiểm tra các hàng
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == 'X':
            return True

    # Kiểm tra các cột
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == 'X':
            return True

    # Kiểm tra đường chéo chính
    if board[0][0] == board[1][1] == board[2][2] == 'X':
        return True

    # Kiểm tra đường chéo phụ
    if board[0][2] == board[1][1] == board[2][0] == 'X':
        return True

    return False
def is_full(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == '-':
                return False
    return True
def main():
    board = [
        ['-','-','-'],
        ['-','-','-'],
        ['-','-','-']
    ]
    for event in pygame.event.get():
        if pygame.event.get() == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse_pos(pos)
            if board[row][col] != 'X' and board[row][col] != 'O':
                draw_X(col * 133, row * 133)
                board[row][col] = 'X'
        player = 'X'
        while True:
                best_move = find_best_move(board)
                best_row, best_col = best_move
                board[best_row][best_col] = 'O'
                draw_O(best_row*133, best_col*133)
                if cpu_won(board):
                    pygame.time.wait(2000)
                    pygame.quit()
                    break
                if is_full(board):
                    pygame.time.wait(2000)
                    pygame.quit()
                    break
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse_pos(pos)
                        if board[row][col] != 'X' and board[row][col] != 'O':
                            draw_X(col * 133, row * 133)
                            board[row][col] = player
                            break
                if user_won(board):
                    pygame.time.wait(2000)
                    pygame.quit()
                    break
                if is_full(board):
                    pygame.time.wait(2000)
                    pygame.quit()
                    break
                draw_grid()
                pygame.display.flip()

if __name__ == '__main__':
    main()

