# choice_train_txt
yoloの補助的に作ったツール．<br>
YOLOのtrain.txtを読み込み，その画像を表示しながら，キー入力によって追加するものやしないものを選択し，新しいtrain.txtを生成する．

## 書き換える必要のある変数の説明
`train_txt_file` 元のtrain.txtファイルの場所．<br>
`remove_txt` train.txtは毎行読み込み，darknet.exeの位置からのアドレスなのでいらない部分を削除するために使う．<br>
`save_file_name` 保存するファイルの名前．<br>
`num` 値を初期化してるだけ．<br>

## 操作説明
* F: 現在の画像を新しいtrain.txtに追加する．
* J: 現在の画像を新しいtrain.txtに追加しない．
* B: 前の画像に戻る．(追加していた場合取り消される)
* ESC: ツールを途中で終了する
