import streamlit as st
import random

# 初始化游戏参数
GAME_SIZE = 10

# 初始化或重置游戏状态
def reset_game():
    st.session_state.player_position = [GAME_SIZE // 2, GAME_SIZE - 1]
    st.session_state.enemy_position = [GAME_SIZE // 2, 0]
    st.session_state.bullet_position = None
    st.session_state.enemy_bullet_position = None
    st.session_state.game_over = False

if 'player_position' not in st.session_state:
    reset_game()

def move_player(direction):
    if st.session_state.game_over:
        return
    pos = st.session_state.player_position
    if direction == 'left' and pos[0] > 0:
        pos[0] -= 1
    elif direction == 'right' and pos[0] < GAME_SIZE - 1:
        pos[0] += 1
    elif direction == 'up' and pos[1] > 0:
        pos[1] -= 1
    elif direction == 'down' and pos[1] < GAME_SIZE - 1:
        pos[1] += 1

def shoot():
    if not st.session_state.game_over:
        st.session_state.bullet_position = st.session_state.player_position[:]

def move_enemy():
    if st.session_state.game_over:
        return
    direction = random.choice(['left', 'right', 'none'])
    pos = st.session_state.enemy_position
    if direction == 'left' and pos[0] > 0:
        pos[0] -= 1
    elif direction == 'right' and pos[0] < GAME_SIZE - 1:
        pos[0] += 1

def enemy_shoot():
    if not st.session_state.game_over and random.random() > 0.8:
        st.session_state.enemy_bullet_position = st.session_state.enemy_position[:]

def update_game():
    if st.session_state.game_over:
        return

    # 更新子弹位置
    if st.session_state.bullet_position:
        st.session_state.bullet_position[1] -= 1
        if st.session_state.bullet_position[1] < 0:
            st.session_state.bullet_position = None
    if st.session_state.enemy_bullet_position:
        st.session_state.enemy_bullet_position[1] += 1
        if st.session_state.enemy_bullet_position[1] >= GAME_SIZE:
            st.session_state.enemy_bullet_position = None

    # 检测子弹命中
    if st.session_state.bullet_position and st.session_state.bullet_position == st.session_state.enemy_position:
        st.sidebar.success("You hit the enemy!")
        st.session_state.game_over = True
    if st.session_state.enemy_bullet_position and st.session_state.enemy_bullet_position == st.session_state.player_position:
        st.sidebar.error("You were hit by the enemy!")
        st.session_state.game_over = True

# 控制面板
st.sidebar.button("Left", on_click=move_player, args=('left',))
st.sidebar.button("Right", on_click=move_player, args=('right',))
st.sidebar.button("Up", on_click=move_player, args=('up',))
st.sidebar.button("Down", on_click=move_player, args=('down',))
st.sidebar.button("Shoot", on_click=shoot)
st.sidebar.button("Reset Game", on_click=reset_game)

# 更新游戏状态
move_enemy()
enemy_shoot()
update_game()

# 绘制游戏界面
board = [[" " for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
if not st.session_state.game_over:
    board[st.session_state.player_position[1]][st.session_state.player_position[0]] = 'P'
    board[st.session_state.enemy_position[1]][st.session_state.enemy_position[0]] = 'E'
    if st.session_state.bullet_position:
        board[st.session_state.bullet_position[1]][st.session_state.bullet_position[0]] = '*'
    if st.session_state.enemy_bullet_position:
        board[st.session_state.enemy_bullet_position[1]][st.session_state.enemy_bullet_position[0]] = '*'

st.write("\n".join("".join(row) for row in board))

if st.session_state.game_over:
    st.write("Game Over!")
