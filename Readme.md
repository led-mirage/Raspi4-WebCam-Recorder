# Raspberry Pi WebCam Recorder

## はじめに

私はずっとWindowsの世界で生きてきたので、Linux系のOSには馴染みがありません。また電子回路も素人なので、間違った記載があるかもしれません。あらかじめご了承ください。

## プログラム概要

ラズパイに接続したWebカメラで動画を撮影して保存するプログラムです。 

使用するWebカメラは Logicool C922n PRO です。

## 機能

- タクトスイッチを押すと撮影を開始し、もう一度押すと撮影を終了します
- 起動中はLED（緑）が点灯します
- 録画中はLED（赤）が点灯します
- 動画撮影部分はffmpegを使用しています
- Ctrl+Cで停止します

## 機材

- Raspberry Pi 4 Model B 4GB
- Logicool C922n PRO HDストリーム ウェブカメラ
- 抵抗入りLED
- タクトスイッチ
- ブレッドボード
- ジャンプワイヤー数本

## 配線

- GPIO20 (Pin#38) -> LEDアノード(+) … パイロットランプ
- GPIO26 (Pin#37) -> LEDアノード(+) … 録画ランプ
- GND (Pin#39) -> LEDカソード(-)
- GPIO21 (Pin#40) -> タクトスイッチ端子１
- 3.3V (Pin#17) -> タクトスイッチ端子２

## 装置画像



## サンプル動画



## 実行環境

- Raspberry Pi 4 Model B 4GB
- Raspberry Pi OS 11 (bullseye)
- Python 3.9.17
- pigpio 1.78
- ffmpeg 4.3.6

## 開発環境

- Visual Studio Code 1.76.0
- pyenv 2.3.24

## ソースファイル構成

- main.py … メインモジュール
- video.py … 録画用クラス
- audio_device.py … オーディオデバイス・ユーティリティクラス

## 実行に必要なモジュール

実行には以下のモジュールが必要です。インストールされていない場合はあらかじめインストールしておいてください。

- pigpio
- ffmpeg

プログラムを実行する前にpigpioのデーモンを起動しておく必要があります。pigpioのインストールとデーモンの起動については[ここ](https://github.com/led-mirage/Raspi4-LEDBlink-pigpio/blob/main/Readme.md)を参照してください。

ffmepgのインストールは次のようにします。

```bash
$ sudo apt-get install ffmpeg
```

## 設定

main.pyの先頭部分にある定数を必要に応じて書き換えてください。

### GPIO

利用している環境に合わせて以下の定数を書き換えます。

``` py
PILOT_LED_PIN = 26  # LEDのGPIO番号
VIDEO_LED_PIN = 20  # 録画LEDのPIN番号
SWITCH_PIN = 21     # タクトスイッチのGPIO番号
```

### デバイス

利用している環境に合わせて以下の定数を書き換えます。

``` py
VIDEO_DEVICE = "/dev/video0"                     # ビデオデバイス名
AUDIO_CARD = "Webcam [C922 Pro Stream Webcam]"   # 録音デバイスのカード名
OUTPUT_FILE = "./output/movie.mp4"               # 出力ファイルパス
```

VIDEO_DEVICEとAUDIO_CARDは、ラズパイに接続している録画録音デバイスが１つの場合は特に変更する必要はないと思います（Webカメラ１台だけが繋がっているような場合）。録音デバイスを表すAUDIO_CARD定数には既定でC922用の識別子が書かれていますが、この識別子が見つからなかった場合は、サーチして最初に見つかった録音デバイスを使用します。

録音デバイスの名前は以下のコマンドで調べることができます。

```bash
$ arecord -l
```

実行例は以下の通りです。カード番号の次に書かれているのがデバイス名（カードID）です。

```
**** ハードウェアデバイス CAPTURE のリスト ****
カード 3: Webcam [C922 Pro Stream Webcam], デバイス 0: USB Audio [USB Audio]
  サブデバイス: 1/1
  サブデバイス #0: subdevice #0
```

## プログラムの実行

### クローン

ラズパイのターミナルを開き、プログラムをクローンしたいディレクトリに移動し、次のコマンドを実行します。

```bash
git clone https://github.com/led-mirage/Raspi4-WebCam-Recorder.git
```

### 実行

以下のコマンドを実行するとプログラムが開始します。

```bash
python main.py
```

### 録画の開始と停止

タクトスイッチを押すと録画が始まり、もう一度押すと録画が停止します。録画中はLEDが点灯します。

### プログラム終了

ターミナルで「Ctrl + C」を押すとプログラムが停止します。

## ラズパイ起動時にプログラムを自動実行するには

独自のsystemdサービスを作成することで、このプログラムをラズパイが起動したときに自動実行させることができます。以下に手順を示します。

### サービスファイルの作成

/etc/systemd/system/webcam-recorder.serviceを作成して、以下の内容を保存します。

```
[Unit]
Description=WebCam Recorder

[Service]
ExecStart=/usr/bin/python /home/username/webcam/main.py
WorkingDirectory=/home/username/webcam/
Restart=always
User=username

[Install]
WantedBy=multi-user.target
```

ファイル中の以下の個所はご自身の環境に合わせて書き換えてください。
- /usr/bin/python … Pythonの実行ファイルへのパス
- /home/username/webcam/ … プログラムを配置したフォルダ
- username … ご自身のユーザー名

サービスファイルを作成・変更するには管理者権限が必要です。下記例のように管理者権限でテキストエディタを起動し編集してください。

```bash
$ sudo nano /etc/systemd/system/webcam-recorder.service
```

CUIが苦手な方は、Visual Studio Codeでも編集できます。サービスファイルをVS Codeで開くと、保存時に管理者権限で保存するかを尋ねられます。私はこの方法の方が楽だと感じました。

### サービスのリロード

サービスファイルを作成したら、systemdに新しいサービスファイルを認識させるために、次のコマンドを実行します。

```bash
$ sudo systemctl daemon-reload
```

### サービスの有効化

次のコマンドでサービスを自動起動するように設定します。

```bash
$ sudo systemctl enable webcam-recorder.service
```

### サービスの実行

サービスをすぐに開始するには、以下のコマンドを実行します。

```bash
$ sudo systemctl start webcam-recorder.service
```

### サービスの停止

もしサービスを停止したい場合は、以下のコマンドを実行します。

```bash
$ sudo systemctl stop webcam-recorder.service
```

### サービスの無効化

もしサービスの自動実行をやめたい場合は、以下のコマンドを実行します。

```bash
$ sudo systemctl disable webcam-recorder.service
```

## 苦労した点

動画の知識もなく、ffmpegにも詳しくないので、ffmpegのオプション構成にとても苦労しました。正直、今でもこれでいいのかもわかりません。試行錯誤の果てにたどり着いたのが、下の現状のオプション構成です。

```py
        command = ["ffmpeg",
                "-y",                            # ファイル上書き
                "-f", "v4l2",                    # ビデオデバイスの入力形式をVideo4Linux2に設定
                "-input_format", "mjpeg",        # 入力ビデオのフォーマットをMotionJPEGに設定
                #"-framerate", "30",             # 入力ビデオのフレームレートを30fpsに設定
                "-thread_queue_size", "81920",   # 入力ビデオのキューのサイズを設定
                "-s", "1280x720",                # 入力ビデオの解像度を1280x720に設定
                #"-s", "1920x1080",              # 入力ビデオの解像度を1920x1080に設定
                "-i", video,                     # 入力ビデオのデバイスを設定
                "-f", "alsa",                    # オーディオデバイスの入力形式をALSAに設定
                "-thread_queue_size", "819200",  # 入力オーディオのキューのサイズを設定
                "-ac", "2",                      # 入力オーディオのチャンネル数を2に設定
                "-i", device_text,               # 入力オーディオのデバイスを設定
                "-c:v", "h264_v4l2m2m",          # 出力ビデオのコーデックをh264_v4l2m2mに設定
                "-b:v", "4M",                    # 出力ビデオのビットレートを4Mbpsに設定
                #"-r", "30",                     # 出力ビデオのフレームレートを30fpsに設定
                "-c:a", "aac",                   # 出力オーディオのコーデックをAACに設定
                "-b:a", "128k",                  # 出力オーディオのビットレートを128kbpsに設定
                "-pix_fmt", "yuv420p",           # 出力ビデオのピクセルフォーマットをyuv420pに設定
                self.output_file]
```

この中でポイントなるのは、出力動画のコーデックにハードウェアエンコーダー（h264_v4l2m2m）と、入力ビデオフォーマットに mjpeg を指定した点でしょうか。

最初、コーデックに h264_omx を使おうとしたのですがうまくいかず、続いてソフトウェアエンコーダーの libx264 も試したのですが満足いく結果が得られなかったので h264_v4l2m2m を採用しました。

入力ビデオフォーマットに関しては、yuyv422 も試したのですが FPS が mjpeg の３分の１程度しか出ないので、最終的には mjpeg を採用しました。

また、この設定で１時間録画するとファイルサイズは1.8GB程度になります。ファイルサイズを押さえたい場合は、ビットレートを現状より低く設定すればOKです。ただし、トレードオフとして画質が落ちます。反対に画質を上げたい場合はビットレートを高く設定してください。

解像度に関しては1980x1080を使いたいところではあるのですが、下記に挙げるメモリの問題があるので、ここでは 1280x720 を採用しています。10分程度の短い動画しかとらないか、ラズパイの8GBモデルを使用しているのであれば 1920x1080 を採用してもいいと思います。

## 問題点（メモリ使用量）

録画中は時間の経過とともにメモリの消費量が増えていきます。そのため、長時間録画するとメモリ不足になってffmpegが強制終了します。ffmpeg単体で動かしても同じ現象が発生するため、ffmpegのオプションの選び方が悪いのかもしれません。

解像度を1920x1080で録画すると30分程度でメモリがなくなります（使用しているラズパイのメモリは4GB）。1280x720でも1時間くらいが限界かなと思います。録画開始前と、録画開始１時間後のメモリの状態を以下に示します。

### 録画開始前（1280x720）

```bash
$ free -m
       total        used        free      shared  buff/cache   available
Mem:    3794         264        1175          44        2354        3410
Swap:     99          99           0
```

### 録画開始１時間後（1280x720）

```bash
$ free -m
       total        used        free      shared  buff/cache   available
Mem:    3794        3177          74          44         541         496
Swap:     99          84          15
```

１時間経過するとほとんどメモリが80%ほど消費されています。

## バージョン履歴

### 1.0 (2023/08/19)
- ファーストリリース
