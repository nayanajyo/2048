from flask import Flask, jsonify, request, render_template
import random
import os

app = Flask(__name__)

SIZE = int(os.environ.get("BOARD_SIZE", 4)) 

def new_game_matrix():
    matrix = [[0]*SIZE for _ in range(SIZE)]
    matrix = add_random_tile(matrix)
    matrix = add_random_tile(matrix)
    return matrix

def add_random_tile(matrix):
    empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if matrix[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        matrix[i][j] = 2 if random.random() < 0.9 else 4
    return matrix

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (SIZE - len(new_row))
    return new_row

def merge(row):
    score = 0
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return row, score

def move_left(matrix):
    moved = False
    total_score = 0
    new_matrix = []
    for i in range(SIZE):
        row = compress(matrix[i])
        row, score = merge(row)
        row = compress(row)
        if row != matrix[i]:
            moved = True
        total_score += score
        new_matrix.append(row)
    return moved, new_matrix, total_score

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def reverse(matrix):
    return [row[::-1] for row in matrix]

def move_right(matrix):
    matrix = reverse(matrix)
    moved, matrix, score = move_left(matrix)
    matrix = reverse(matrix)
    return moved, matrix, score

def move_up(matrix):
    matrix = transpose(matrix)
    moved, matrix, score = move_left(matrix)
    matrix = transpose(matrix)
    return moved, matrix, score

def move_down(matrix):
    matrix = transpose(matrix)
    moved, matrix, score = move_right(matrix)
    matrix = transpose(matrix)
    return moved, matrix, score

def check_win(matrix):
    return any(cell == 2048 for row in matrix for cell in row)

def moves_available(matrix):
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == 0:
                return True
            if j < SIZE - 1 and matrix[i][j] == matrix[i][j + 1]:
                return True
            if i < SIZE - 1 and matrix[i][j] == matrix[i + 1][j]:
                return True
    return False

game_state = {
    "matrix": new_game_matrix(),
    "score": 0,
    "won": False,
    "over": False
}

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/state', methods=['GET'])
def state():
    return jsonify(game_state)

@app.route('/move', methods=['POST'])
def move():
    global game_state
    direction = request.json.get('direction')
    matrix = game_state['matrix']
    score = game_state['score']
    moved = False
    add_score = 0

    if direction == 'left':
        moved, matrix, add_score = move_left(matrix)
    elif direction == 'right':
        moved, matrix, add_score = move_right(matrix)
    elif direction == 'up':
        moved, matrix, add_score = move_up(matrix)
    elif direction == 'down':
        moved, matrix, add_score = move_down(matrix)

    if moved:
        matrix = add_random_tile(matrix)
        score += add_score

    won = check_win(matrix)
    over = not moves_available(matrix) and not won

    game_state = {
        "matrix": matrix,
        "score": score,
        "won": won,
        "over": over
    }
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset():
    global game_state
    game_state = {
        "matrix": new_game_matrix(),
        "score": 0,
        "won": False,
        "over": False
    }
    return jsonify(game_state)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
