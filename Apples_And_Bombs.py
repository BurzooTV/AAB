#Apples And Bombs.

import os
import re
import random
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts.dialogs import input_dialog
from prompt_toolkit.shortcuts.dialogs import message_dialog
from prompt_toolkit.shortcuts.dialogs import radiolist_dialog
from prompt_toolkit.key_binding.bindings.basic import load_basic_bindings


clear = lambda: os.system('clear')
bindings = load_basic_bindings()
board = [' . ' for _ in range(50)]


dialog_style = Style.from_dict({
    'dialog': 'bg:#ffffff',
    'dialog frame.label': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#ffffff #000000',
    'dialog shadow': 'bg:#000000',})


def check_score_board_file() -> None:
    if not os.path.exists('AAMSB.txt'):
        with open('AAMSB.txt', 'w+') as _: ...


def get_high_score() -> int:
    if os.path.exists('AAMSB.txt'):
        with open('AAMSB.txt', 'r') as score_board_file:
            high_score = re.findall('[0-9]+', score_board_file.read())
            int_hight_score = map(lambda x: int(x), high_score)
            try:
                return max(int_hight_score)
            except:
                return 0
    else:
        return 0


def draw_board() -> None:
    clear()
    print('\n')
    print(f'Score: {score}               High Score: {str(get_high_score())}')
    #print('\n')
    for dot in board[0:10]:
        print(dot, end=' ')
    print('\n')
    for dot in board[10:20]:
        print(dot, end=' ')
    print('\n')
    for dot in board[20:30]:
        print(dot, end=' ')
    print('\n')
    for dot in board[30:40]:
        print(dot, end=' ')
    print('\n')
    for dot in board[40:50]:
        print(dot, end=' ')
    print('\n')


@bindings.add('up')
def _(event):
    event.current_buffer.insert_text('-10')
    event.app.exit(result=event.app.current_buffer.text)


@bindings.add('down')
def _(event):
    event.current_buffer.insert_text('+10')
    event.app.exit(result=event.app.current_buffer.text)

@bindings.add('left')
def _(event):
    event.current_buffer.insert_text('-1')
    event.app.exit(result=event.app.current_buffer.text)

@bindings.add('right')
def _(event):
    event.current_buffer.insert_text('+1')
    event.app.exit(result=event.app.current_buffer.text)


def main():
    check_score_board_file()
    session = PromptSession()

    global current_snake
    last_snake, current_snake = 25, 25

    board.pop(last_snake)
    board.insert(current_snake, ' \033[92m#\033[0m ')

    ups = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    downs = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    lefts = [0, 10, 20, 30, 40]
    rights = [9, 19, 29, 39, 49]
    
    global apple
    apple = random.randint(0, 49)
    board.pop(apple)
    board.insert(apple, ' \033[34m@\033[0m ')

    global score
    score = 0

    bomb = random.randint(0, 49)

    while True:
        clear()
        main_menu = radiolist_dialog(title='Apples And Bombs!',
                                    text='Main Menu:',
                                    values=[('new_game', 'New Game'),
                                            ('score_board', 'ScoreBoard'),
                                            ('help', 'Help'),
                                            ('exit', 'Exit')], style=dialog_style).run()

        if main_menu == 'new_game':

            while True:
                draw_board()
                prompt = session.prompt(key_bindings=bindings)

                if board.count(' \033[91m$\033[0m ') > 0:
                    board.remove(' \033[91m$\033[0m ')
                    board.insert(bomb, ' . ')

                bomb = random.randint(0, 49)
                board.pop(bomb)
                board.insert(bomb, ' \033[91m$\033[0m ')

                if current_snake in ups and prompt == '-10':
                    board.remove(' \033[92m#\033[0m ')
                    board.insert(last_snake, ' . ')
                    current_snake += + 40
                    last_snake = current_snake
                    board.pop(current_snake)
                    board.insert(current_snake, ' \033[92m#\033[0m ')

                elif current_snake in downs and prompt == '+10':
                    board.remove(' \033[92m#\033[0m ')
                    board.insert(last_snake, ' . ')
                    current_snake += -40
                    last_snake = current_snake
                    board.pop(current_snake)
                    board.insert(current_snake, '\033[92m#\033[0m ')

                elif current_snake in lefts and prompt == '-1':
                    board.remove(' \033[92m#\033[0m ')
                    board.insert(last_snake, ' . ')
                    current_snake += +9
                    last_snake = current_snake
                    board.pop(current_snake)
                    board.insert(current_snake, ' \033[92m#\033[0m ')

                elif current_snake in rights and prompt == '+1':
                    board.remove(' \033[92m#\033[0m ')
                    board.insert(last_snake, ' . ')
                    current_snake += -9
                    last_snake = current_snake
                    board.pop(current_snake)
                    board.insert(current_snake, ' \033[92m#\033[0m ')

                else:
                    
                    if board.count(' \033[92m#\033[0m ') > 0:
                        board.remove(' \033[92m#\033[0m ')
                        board.insert(last_snake, ' . ')

                    current_snake += int(prompt)
                    last_snake = current_snake
                    board.pop(current_snake)
                    board.insert(current_snake, ' \033[92m#\033[0m ')

                if current_snake == apple:
                    score += 10
                    apple = random.randint(0, 49)
                    board.pop(apple)
                    board.insert(apple, ' \033[34m@\033[0m ')

                if bomb == apple:
                    board.pop(apple)
                    board.insert(apple, ' \033[34m@\033[0m ')
                    bomb = 50

                if current_snake == bomb:
                    break

            
            clear()
            end_dialog = input_dialog(title='Game Over!',
                                       text=f'Your Score is {score}!\nEnter Your Name To Submit Your Score!', style=dialog_style).run()

            if end_dialog == None:
                score = 0
                continue
            else:
                with open('AAMSB.txt', 'a+') as score_board_file:
                    score_board_file.write(end_dialog + ' ' + str(score) + '\n')
                score = 0
                continue


        elif main_menu == 'score_board':
            with open('AAMSB.txt', 'r') as score_board_file:
                _ = message_dialog(title='ScoreBoard',
                text='\n'.join(score_board_file.readlines()),
                style=dialog_style).run()


        elif main_menu == 'help':
            _ = message_dialog(title='Help',
            text='''            You must achieve the goals,
            while being lucky and not be killed by mines.
            GoodLuck!''', style=dialog_style).run()


        elif main_menu == 'exit':
            break


        elif main_menu == None:
            continue


if __name__ == "__main__":
    main()