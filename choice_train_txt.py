####

import cv2
import re
import numpy as np

train_txt_file = 'train.txt'
remove_txt = 'face-data/'
save_file_name = 'train3.txt'
num = ''

with open(train_txt_file) as f:
    num = f.read().count('jpg')
print('number of images:', num)

# 説明文の表示
def text_window():
    text_window_img = np.full((100, 260, 3), 128, dtype=np.uint8)
    cv2.putText(text_window_img, 'F: ADD', (34, 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'J: THROUGH', (38, 45),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'B: BACK(DELETE)', (32, 70),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.putText(text_window_img, 'ESC: END', (0, 95),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA)
    cv2.imshow('Description', text_window_img)
    cv2.moveWindow('Description', 1580, 25)


def generator():
    temp_paths = []

    # 配列に読み込ませる
    with open(train_txt_file) as f:
        for i in range(num):
            temp_paths.append(f.readline().strip())

    # 一旦読み込んだ配列からそれぞれ取り出して,画像を表示しながら判定する
    img_paths = []  # 出力する配列
    end_flag = False  # 途中終了フラグ
    i = 0  # 表示する配列の番号
    while i < num:
        # 両端の空白や改行を除去して1行ずつ読み込む
        img_path = temp_paths[i].strip()

        # 画像を読み込み 画像を表示(大きい画像は一旦リサイズ)
        im = cv2.imread(re.sub(remove_txt, '', img_path))
        if im.shape[0] >= 950 or im.shape[1] >= 1800:
            im = cv2.resize(im, (int(im.shape[1] * 0.5), int(im.shape[0] * 0.5)))
        cv2.imshow('now image', im)
        cv2.moveWindow('now image', 50, 25)

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
            elif key == 27:  # escの入力で途中終了
                end_flag = True
                break
            else:
                print('キー入力が正しくありません')
        if end_flag:
            print('途中で終了します.途中までの結果は保存されます')
            break
    # 画像パス一覧を出力
    cv2.destroyAllWindows()
    return img_paths

text_window()
img_paths = generator()

# trainファイル作成
train_list = img_paths[:num]
train_str = '\n'.join(train_list)
with open(save_file_name, 'w') as f:
    f.write(train_str)
