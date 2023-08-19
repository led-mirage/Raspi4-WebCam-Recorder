"""
Raspberry Pi WebCam Recorder
メインモジュール

Copylight (c) 2023 led-mirage
"""

import pigpio
import signal
import time
from video import Video


PILOT_LED_PIN = 26  # LEDのGPIO番号
VIDEO_LED_PIN = 20  # 録画LEDのPIN番号
SWITCH_PIN = 21	    # タクトスイッチのGPIO番号

VIDEO_DEVICE = "/dev/video0"                    # ビデオデバイス名
AUDIO_CARD = "Webcam [C922 Pro Stream Webcam]"  # 録音デバイスのカード名
OUTPUT_FILE = "./output/movie.mp4"


pi = pigpio.pi()
pi.set_mode(PILOT_LED_PIN, pigpio.OUTPUT)
pi.set_mode(VIDEO_LED_PIN, pigpio.OUTPUT)
pi.set_mode(SWITCH_PIN, pigpio.INPUT)
pi.set_pull_up_down(SWITCH_PIN, pigpio.PUD_DOWN)


video = Video()


# メイン
def main():
    print("Raspberry Pi WebCam Recorder ver 1.0.0")

    set_led_status(PILOT_LED_PIN, True)

    while True:
        # タクトスイッチが押されたか確認
        if pi.read(SWITCH_PIN) == 1:
            if not video.is_recording:
                video.start_recording(OUTPUT_FILE, VIDEO_DEVICE, AUDIO_CARD)
            else:
                video.stop_recording()
                time.sleep(1)
                print(f"{video.output_file}を書き込みました")
                
            set_led_status(VIDEO_LED_PIN, video.is_recording)
                
            time.sleep(0.5)  # 押下時のチャタリング対策
        time.sleep(0.01)  # CPU使用率を下げるための待機


# LEDを点灯／消灯する
def set_led_status(pin, is_on):
    duty = 10 # 0-255
    if is_on:
        pi.set_PWM_dutycycle(pin, duty)
    else:
        pi.set_PWM_dutycycle(pin, 0)


# 終了処理
def cleanup():
    video.stop_recording()
    set_led_status(PILOT_LED_PIN, False)
    set_led_status(VIDEO_LED_PIN, False)
    pi.stop()


# 終了ハンドラ
def handle_exit(signum, frame):
    cleanup()
    exit(0)


signal.signal(signal.SIGINT, handle_exit)   # Ctrl + C
signal.signal(signal.SIGHUP, handle_exit)   # Close Terminal
signal.signal(signal.SIGTERM, handle_exit)  # killed


try:
    main()
except Exception as e:
    print(e)
    pass
else:
    cleanup()
