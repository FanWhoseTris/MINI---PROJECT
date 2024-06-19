import sys

def inboard(board):
    for i in range(3):
        for j in range(3):
            if board[i*3+j] == -1:
                print('O',end=' ')
            elif board[i*3+j] == 1:
                print('X',end=' ')
            else:
                print('-',end=' ')
        print()
def premove(board):
    def check(board):
        for i in range(3):
            r = board[i*3 : i*3+3]
            c = board[i :: 3]
            if all(cell == 1 for cell in r):
                return 10
            if all(cell == -1 for cell in r):
                return -10
            if all(cell == 1 for cell in c):
                return 10
            if all(cell == -1 for cell in c):
                return -10
        dcheo1 = board[0] == board[4] == board[8]
        dcheo2 = board[2] == board[4] == board[6]
        if dcheo1 and board[0] != 0:
            return 10 if board[0] == 1 else -10
        if dcheo2 and board[2] != 0:
            return 10 if board[2] == 1 else -10
        if 0 not in board:
            return 00
        return None

    def minimax(board, depth, alpha, beta, maximizing):
        score = check(board)
        if score is not None:
            return score
        if maximizing:
            best_score = -sys.maxsize
            for i, cell in enumerate(board):
                if cell == 0:
                    board[i] = 1
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[i] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
            return best_score
        else:
            best_score = sys.maxsize
            for i, cell in enumerate(board):
                if cell == 0:
                    board[i] = -1
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[i] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
            return best_score
    #Main của hàm đoán nước đi
    bestmove = None
    bestscore = -sys.maxsize
    for i,cell in enumerate(board):
        if cell == 0:
            board[i] = 1
            score = minimax(board, 0, -sys.maxsize, sys.maxsize, False)
            board[i] = 0
            if score > bestscore:
                bestscore = score
                bestmove = i
    return bestmove + 1
#Main cua truong trinh
if __name__ == '__main__':
    board = list(map(int,input().split()))
    #inboard(board)
    ans = premove(board)
    print(ans)
