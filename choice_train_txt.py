# -*- coding: utf-8 -*-

import cv2
import re
import numpy as np
import time


train_txt_file = 'train.txt'
remove_txt = 'face-data/'
save_file_name = 'train3.txt'


# 説明用のテキスト画面の生成と表示
def text_window():
    text_window_img = np.full((125, 260, 3), 128, dtype=np.uint8)
    cv2.putText(text_window_img, 'F: ADD', (34, 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'J: THROUGH', (37, 45),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'B: BACK(DELETE)', (32, 70),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'Q: END(NO SAVE)', (32, 95),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'ESC: END', (0, 120),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.imshow('Description', text_window_img)
    cv2.moveWindow('Description', 0, 25)


def generator():
    temp_paths = []
    num = 0

    # 配列に読み込ませる
    print('テキストを読み込んでいます。しばらく待ってください')
    with open(train_txt_file) as f:
        for line in f:
            temp_paths.append(line)
            num += 1
    print("画像の数:" + str(num))

    # 最初に画像用の画面を作って,ウィンドウの位置を調整しておく(ループ内でウィンドウの移動を何回もさせないため)
    temp_img = np.full((100, 260, 3), 128, dtype=np.uint8)
    cv2.imshow('now image', temp_img)
    cv2.moveWindow('now image', 340, 25)

    # 一旦読み込んだ配列からそれぞれ取り出して,画像を表示しながら判定する
    img_paths = []  # 出力する配列
    end_flag = False  # 途中終了フラグ
    save_flag = True
    i = 0  # 表示する配列の番号
    while i < num:  # 全部の行を読み込ませる
        # 両端の空白や改行を除去して1行ずつ読み込む
        img_path = temp_paths[i].strip()

        # 画像を読み込み 画像を表示(大きい画像は一旦リサイズ)
        im = cv2.imread(re.sub(remove_txt, '', img_path))
        if im.shape[0] >= 950 or im.shape[1] >= 1700:
            im = cv2.resize(im, (int(im.shape[1] * 0.5), int(im.shape[0] * 0.5)))
        cv2.putText(im, str(i+1), (0, 12), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)  # 画像番号を出力
        cv2.imshow('now image', im)
        time.sleep(0.2)  # 長押しで暴発しないため

        # 入力を待つ
        while 1:
            key = cv2.waitKey(0)
            if key == ord('f'):  # fの入力で保存する
                print('追加しました:' + img_path)
                img_paths.append(img_path)
                i += 1
                break
            elif key == ord('j'):  # jの入力で保存しない
                i += 1
                break
            elif key == ord('b') and i > 0:  # 表示する画像を一つ戻る
                if img_paths[-1] == temp_paths[i - 1].strip():
                    print('削除しました:' + img_paths[-1])
                    img_paths.pop()
                i -= 1
                break
            elif key == ord('q'):  # 保存をセずに終了
                end_flag = True
                save_flag = False
                break
            elif key == 27:  # escの入力で途中終了
                end_flag = True
                break
            else:
                print('キー入力が正しくありません')
        if end_flag:
            if save_flag:
                print('途中で終了します.途中までの結果は保存しました.')
            else:
                print('途中で終了します.途中までの結果は保存しませんでした.')
            break
    # 画像パス一覧を出力
    cv2.destroyAllWindows()
    return img_paths, save_flag, num


text_window()
img_paths, save_flag, num = generator()

# trainファイル作成
if save_flag:
    train_str = '\n'.join(img_paths)
    with open(save_file_name, 'w') as f:
        f.write(train_str)
    print('train.txtに追加した数:' + str(len(img_paths)))
