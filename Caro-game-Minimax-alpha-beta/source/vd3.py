import math

index1 = None
board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def is_full():
    for i in range(9):
        if board[i] != 'X':
            if board[i] != 'O':
                return 0
    return 1


def user_won():
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == 'O':
            return 1
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == 'O':
            return 1
    if board[0] == board[4] == board[8] == 'O':
        return 1
    if board[2] == board[4] == board[6] == 'O':
        return 1
    return 0


def cpu_won():
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == 'X':
            return 1
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == 'X':
            return 1
    if board[0] == board[4] == board[8] == 'X':
        return 1
    if board[2] == board[4] == board[6] == 'X':
        return 1
    return 0


def draw_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("---------")
    print(board[3], "|", board[4], "|", board[5])
    print("---------")
    print(board[6], "|", board[7], "|", board[8])


def minimax(flag):
    global index1
    max_val = -math.inf
    min_val = math.inf
    value = 1
    if cpu_won() == 1:
        return 10
    elif user_won() == 1:
        return -10
    elif is_full() == 1:
        return 0
    score = [1] * 9

    for i in range(9):
        if board[i] != 'O' and board[i] != 'X':
            if min_val > max_val:
                if flag:
                    board[i] = 'X'
                    value = minimax(False)
                else:
                    board[i] = 'O'
                    value = minimax(True)
                board[i] = i+1
                score[i] = value

    if flag:
        max_val = -math.inf
        for j in range(9):
            if score[j] > max_val and score[j] != 1:
                max_val = score[j]
                index1 = j
        return max_val
    if not flag:
        min_val = math.inf
        for j in range(9):
            if score[j] < min_val and score[j] != 1:
                min_val = score[j]
                index1 = j
        return min_val


if __name__ == '__main__':
    move = None
    choice = int(input("--------------------------Chao Mung Ban Den Voi Game Tictactoe--------------------------------------------------\n"
                   "Chọn người đánh trước (1-người (O) ||| 2-CPU (X) ):"))
    if choice == 1:
        draw_board()
        while True:
            move = int(input("Mời nhập ô:"))
            if board[move - 1] != 'O' and board[move - 1] != 'X':
                board[move - 1] = 'O'
                draw_board()
                break
            else:
                print("Ô này không hợp lệ")

    while True:
        print("Đợi em tí....")
        minimax(True)
        board[index1] = 'X'
        draw_board()
        if cpu_won() == 1:
            print("Non ơi là non")
            break
        if is_full() == 1:
            print("Tuổi Ngang Tao thoai.")
            break
        while True:
            move = int(input("Mời Nhập Ô:"))
            if board[move - 1] != 'O' and board[move - 1] != 'X':
                board[move - 1] = 'O'
                draw_board()
                break
            else:
                print("Ô sai roài, chọn ô khác đi nhóc...")
        if user_won() == 1:
            print("Bạn thắng rồi, hên thoai.")
            break
        if is_full() == 1:
            print("Hòa rồi, hên đó....")
            break