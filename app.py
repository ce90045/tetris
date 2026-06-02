import streamlit as st
import numpy as np
import random
import time

ROWS = 20
COLS = 10

SHAPES = [
    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],
]


def rotate(shape):
    return np.rot90(shape, -1).tolist()


def new_piece():
    shape = random.choice(SHAPES)
    return {
        "shape": shape,
        "row": 0,
        "col": COLS // 2 - len(shape[0]) // 2
    }


def collision(board, piece):
    shape = piece["shape"]

    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                br = piece["row"] + r
                bc = piece["col"] + c

                if (
                    br < 0
                    or br >= ROWS
                    or bc < 0
                    or bc >= COLS
                ):
                    return True

                if board[br][bc]:
                    return True

    return False


def merge(board, piece):
    shape = piece["shape"]

    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                board[piece["row"] + r][piece["col"] + c] = 1


def clear_lines(board):
    new_board = [row for row in board if not all(row)]
    cleared = ROWS - len(new_board)

    while len(new_board) < ROWS:
        new_board.insert(0, [0] * COLS)

    return new_board, cleared


def draw_board(board, piece):
    display = np.array(board)

    shape = piece["shape"]

    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                rr = piece["row"] + r
                cc = piece["col"] + c

                if 0 <= rr < ROWS and 0 <= cc < COLS:
                    display[rr][cc] = 2

    html = """
    <style>
    .cell{
        width:25px;
        height:25px;
        border:1px solid #444;
        display:inline-block;
    }
    </style>
    """

    for r in range(ROWS):
        html += "<div>"
        for c in range(COLS):

            color = "#111"

            if display[r][c] == 1:
                color = "#00AAFF"

            if display[r][c] == 2:
                color = "#FFAA00"

            html += f'<div class="cell" style="background:{color};"></div>'

        html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


if "board" not in st.session_state:
    st.session_state.board = [[0] * COLS for _ in range(ROWS)]
    st.session_state.piece = new_piece()
    st.session_state.score = 0
    st.session_state.last_drop = time.time()

st.title("🎮 Streamlit Tetris")

col1, col2, col3, col4 = st.columns(4)

if col1.button("◀"):
    p = st.session_state.piece.copy()
    p["col"] -= 1

    if not collision(st.session_state.board, p):
        st.session_state.piece = p

if col2.button("▶"):
    p = st.session_state.piece.copy()
    p["col"] += 1

    if not collision(st.session_state.board, p):
        st.session_state.piece = p

if col3.button("🔄"):
    p = st.session_state.piece.copy()
    p["shape"] = rotate(p["shape"])

    if not collision(st.session_state.board, p):
        st.session_state.piece = p

if col4.button("▼"):
    p = st.session_state.piece.copy()
    p["row"] += 1

    if not collision(st.session_state.board, p):
        st.session_state.piece = p

current = time.time()

if current - st.session_state.last_drop > 0.7:

    p = st.session_state.piece.copy()
    p["row"] += 1

    if collision(st.session_state.board, p):

        merge(
            st.session_state.board,
            st.session_state.piece
        )

        st.session_state.board, cleared = clear_lines(
            st.session_state.board
        )

        st.session_state.score += cleared * 100

        st.session_state.piece = new_piece()

        if collision(
            st.session_state.board,
            st.session_state.piece
        ):
            st.error("GAME OVER")
            st.stop()

    else:
        st.session_state.piece = p

    st.session_state.last_drop = current

st.write(f"점수: {st.session_state.score}")

draw_board(
    st.session_state.board,
    st.session_state.piece
)

time.sleep(0.1)
st.rerun()
