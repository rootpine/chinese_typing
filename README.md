# chinese typing
中国語を覚えるために作ったシンプルなタイピングゲーム。

## 実行環境
Python 3.7.6
windows 10

## 使用したライブラリ
pygame, xlrd

## 実行方法
 `$ py typing.py エクセルのパス（拡張子なし） シート名 問題数`
例)  `$ py typing.py test Sheet1 5`

## 画面
スタート画面

![start](./start.PNG)

何かキーを押すと問題へ。

![game](./mondai.PNG)

ピンインの文字色はタイピングの指を表す。（どの指でどのキーを押すか覚えていないため。笑）
\_(アンダーバー)はスペースを意味する。
音声ファイル(ファイル名は単語の列数と同じ)があれば、問題ごとに音声を流す。

全ての問題終了後、スコアを表示。

![finish](./finish.PNG)

## メモ
- 音声の再生が問題の表示と微妙にずれる（私個人で使うには気にならないけれど）。並列処理で改善されると思う。
- エクセルファイルを作るのが少し面倒。もっと自動化したい。
- スタートと終了の画面がシンプルすぎ

## 参考
1. URL: <http://hajimete-program.com/blog/2018/07/13/python初心者講座-60行でタイピングゲームを作ろう/>
2. URL: <https://qiita.com/kekeho/items/a0b93695d8a8ac6f1028>
