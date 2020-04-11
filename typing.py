# -*- coding: utf-8 -*-
import os.path
from sys import exit, argv
from re import match, sub
from random import sample

import pygame
from xlrd import open_workbook

def convert_space(pinyin):
    # スペースを見やすいように変換
    return sub(r' ', '_', pinyin)

def color_judge(ans):
    if match(r'[rfvtgbyhnujm]', ans):
        return (0, 0, 255)
    elif match(r'[ ]', ans):
        return (204, 204, 204)
    elif match(r'[edcik]', ans):
        return (255, 0, 0)
    elif match(r'[wsxol]', ans):
        return (0, 128, 0)
    else:
        return (255, 140, 0)

    return

def select_char_color(ans):
    # 文字色判別, 再帰
    return list(map(color_judge, ans))

def render_wenti(zn, jp, wenti, wenti_cnt, wenti_num):
    wenti.fill((255, 255, 255))

    font_zn = pygame.font.SysFont('simhei', 64)
    font_jp = pygame.font.SysFont('hgｺﾞｼｯｸehgpｺﾞｼｯｸehgsｺﾞｼｯｸe', 18)
    font_wn = pygame.font.SysFont(None, 28)

    sf_zn = font_zn.render(zn, True, (0, 0, 0), (255, 255, 255))
    sf_jp = font_jp.render(jp, True, (0, 0, 0), (255, 255, 255))
    sf_wn = font_wn.render(str(wenti_cnt + 1) + '/' + str(wenti_num), \
                            True, (0, 0, 0), (255, 255, 255))

    wenti.blit(sf_zn, (100, 4))
    wenti.blit(sf_jp, (sf_zn.get_rect().width + 100, 5))
    wenti.blit(sf_wn, (10, 4))

    return

def render_pinyin(pinyin, char_color, input):
    input.fill((255, 255, 255))
    font_pinyin = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 64)
    marg = 100
    len_pinyin = len(pinyin)
    for i in range(len_pinyin):
        sf_pinyin_color = font_pinyin.render(pinyin[i], True, char_color[i], (255, 255, 255))
        input.blit(sf_pinyin_color, (marg, 0))
        marg += sf_pinyin_color.get_rect().width

    return

def render_score(err, score, header):
    header.fill((200, 200, 200))
    font_score = pygame.font.SysFont(None, 28)
    sf_score = font_score.render('error:' + str(err) + '  score: ' + str(round(score, 3)),\
                                    True, (0, 0, 0), (200, 200, 200))
    header.blit(sf_score, (0, 0))

    return

def render_footer(bg):
    font_jp_foot = pygame.font.SysFont('hgｺﾞｼｯｸehgpｺﾞｼｯｸehgsｺﾞｼｯｸe', 28)
    exp1 = '右5 右4 右3 右2   左2 左3 左4 左5'

    marg = 30
    for char_exp1 in exp1:
        if char_exp1 == ' ' or char_exp1 == '右' or char_exp1 == '左':
            exp1_color = (0, 0, 0)
        elif char_exp1 == '2':
            exp1_color = (0, 0, 255)
        elif char_exp1 == '3':
            exp1_color = (255, 0, 0)
        elif char_exp1 == '4':
            exp1_color = (0, 128, 0)
        else:
            exp1_color = (255, 140, 0)

        sf_exp1_color = font_jp_foot.render(char_exp1, True, exp1_color, (200, 200, 200))
        bg.blit(sf_exp1_color, (marg, 190))
        marg += sf_exp1_color.get_rect().width

    return

def play_mp3(zn):
    file = './mp3/' +args[2] +'/'+ zn + '.wav'

    if os.path.isfile(file):
        pygame.mixer.music.load(file)  # 読み込み
        pygame.mixer.music.play()  # 再生, 引数は再生回数
    return

def make_ans(pinyin):
    ans = sub("ā|á|ǎ|à", 'a', pinyin)
    ans = sub("ē|é|ě|è", 'e', ans)
    ans = sub("ī|í|ǐ|ì", 'i', ans)
    ans = sub("ō|ó|ǒ|ò", 'o', ans)
    ans = sub("ū|ú|ǔ|ù", 'u', ans)
    ans = sub("ü|ǖ|ǘ|ǚ|ǜ", 'v', ans)
    return ans

def run_game(screen, wenti_num, wb, sheet):
    # ゲーム実行
    # 変数の初期化
    wenti_cnt, type_num, err, score = 0, 0, 0, 0

    zn = sheet.col_values(0)
    pinyin = sheet.col_values(1)
    ans = list(map(make_ans, pinyin))
    jp = sheet.col_values(3)

    # pinyinのスペースを_に置換
    pinyin = list(map(convert_space,pinyin))

    k = len(zn) # エクセル表の行数
    if wenti_num > k:
        print('問題数は表の単語数を超えることができません。')
        exit()

    num_list = sample(list(range(k)), wenti_num)  #rondom word num
    word_num = num_list[wenti_cnt]
    char_color = list(map(select_char_color, ans))

    # Fill background
    bg = pygame.Surface(screen.get_size())
    bg.fill((200, 200, 200))
    wenti = pygame.Surface((720, 68))
    header = pygame.Surface((200, 24))
    input = pygame.Surface((720, 90))

    # Blit
    play_mp3(zn[word_num])
    render_footer(bg)
    render_wenti(zn[word_num], jp[word_num], wenti, wenti_cnt, wenti_num)
    render_pinyin(pinyin[word_num], char_color[word_num], input)
    render_score(err, score, header)

    screen.blit(bg, (0, 0))
    screen.blit(wenti, (0, 24))
    screen.blit(input, (0, 88))
    screen.blit(header, (300, 0))

    while True:
        pygame.display.update()

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                type_num += 1
                if chr(event.key) == ans[word_num][0]:
                    pinyin[word_num] = pinyin[word_num][1:]
                    ans[word_num] = ans[word_num][1:]
                    char_color[word_num] = char_color[word_num][1:]

                    if not ans[word_num]:
                        wenti_cnt += 1
                        if wenti_cnt == wenti_num:
                            key = 1
                            start_quit(key, wenti_num, wb, sheet, score, err)
                            break
                        word_num = num_list[wenti_cnt]
                        play_mp3(zn[word_num])
                        render_wenti(zn[word_num], jp[word_num], wenti, wenti_cnt, wenti_num)
                        screen.blit(wenti, (0, 24))
                else:
                    err += 1
                score = ((type_num-err) / type_num) * 100

                render_pinyin(pinyin[word_num], char_color[word_num], input)
                screen.blit(input, (0, 88))
                render_score(err, score, header)
                screen.blit(header, (300, 0))

    return

#起動時とリスタート時の画面表示
def start_quit(key, wenti_num, wb, sheet, score, err):
    if key == 0:
        # initialization
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.pre_init(16000, -16, 2, 2048) # setup mixer to avoid sound lag, play speed
        pygame.mixer.init() # mp3
        pygame.display.set_caption('Chinese Typing!')

    screen = pygame.display.set_mode((540, 230))

    #フォントとテキストの設定
    font = pygame.font.SysFont(None, 40)
    screen.fill((0, 0, 0))

    if key == 0 :
        text1 = font.render('Type Chinese Words (^^)v', True, (255, 255, 255), (0, 0, 0))
        text2 = font.render('** _: type space **', True, (255, 255, 255), (0, 0, 0))
        text_press = font.render('Press Any Key to start', True, (255, 255, 255), (0, 0, 0))
    else:
        text1 = font.render('your score: ' + str(round(score, 3)), True, (255, 255, 255), (0, 0, 0))
        text2 = font.render('Error: ' + str(err), True, (255, 255, 255), (0, 0, 0))
        text_press = font.render('Press Any Key to Re-start', True, (255, 255, 255), (0, 0, 0))

    screen.blit(text1, (20, 10))
    screen.blit(text2, (20, 60))
    screen.blit(text_press, (20, 160))

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                #何かしらキーが押されたらゲームを再開
                run_game(screen, wenti_num, wb, sheet)
                break
    return

# command line: e.g. "py typing.py test Sheet1 5"
key = 0 # key: start or quit
args = argv
if len(args) > 3:
    wb = open_workbook(args[1] + '.xlsx') # './HSK5.xlsx'
    sheet = wb.sheet_by_name(args[2]) # 'Sheet0'
    wenti_num = int(args[3])
else:
    print('引数が正しくありません、確認してください。')
    exit()

start_quit(key, wenti_num, wb, sheet, 0, 0)
