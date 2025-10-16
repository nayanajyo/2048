from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)
SIZE = 4

def create_matrix():
    matrix = [[0]*SIZE for _ in range(SIZE)]
    add_random_tile(matrix)
    add_random_tile(matrix)
    return matrix

def add_random_tile(matrix):
    empty = [(i,j) for i in range(SIZE) for j in range(SIZE) if matrix[i][j] == 0]
    if empty:
        i,j = random.choice(empty)
        matrix[i][j] = 2 if random.random() < 0.9 else 4

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0]*(SIZE-len(new_row))
    return new_row

def merge(row):
    for i in range(SIZE-1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
    return row

def move_left(matrix):
    moved = False
    for i in range(SIZE):
        row = matrix[i]
        compressed = compress(row)
        merged = merge(compressed)
        new_row = compress(merged)
        if new_row != row:
            moved = True
        matrix[i] = new_row
    return moved

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def move_right(matrix):
    # Reverse rows, move left, then reverse back
    matrix = [row[::-1] for row in matrix]
    moved = move_left(matrix)
    matrix = [row[::-1] for row in matrix]
    return moved, matrix

def move_up(matrix):
    matrix = transpose(matrix)
    moved = move_left(matrix)
    matrix = transpose(matrix)
    return moved, matrix

def move_down(matrix):
    matrix = transpose(matrix)
    moved, matrix = move_right(matrix)
    matrix = transpose(matrix)
    return moved, matrix

# Store game state globally (in production, use sessions or DB)
game_matrix = create_matrix()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state', methods=['GET'])
def state():
    return jsonify(matrix=game_matrix)

@app.route('/move', methods=['POST'])
def move():
    global game_matrix
    direction = request.json.get('direction')
    moved = False
    if direction == 'left':
        moved = move_left(game_matrix)
    elif direction == 'right':
        moved, game_matrix = move_right(game_matrix)
    elif direction == 'up':
        moved, game_matrix = move_up(game_matrix)
    elif direction == 'down':
        moved, game_matrix = move_down(game_matrix)

    if moved:
        add_random_tile(game_matrix)

    return jsonify(matrix=game_matrix)

@app.route('/reset', methods=['POST'])
def reset():
    global game_matrix
    game_matrix = create_matrix()
    return jsonify(matrix=game_matrix)

if __name__ == '__main__':
    app.run(debug=True)
