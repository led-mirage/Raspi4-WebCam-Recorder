"""
Raspberry Pi WebCam Recorder
動画撮影クラス

Copylight (c) 2023 led-mirage
"""

import os
import signal
import subprocess
from audio_device import AudioDevice


# 動画撮影クラス
class Video:
    # コンストラクタ
    def __init__(self):
        self.output_file = ""
        self.ffmpeg_process = None
        self.is_recording = False


    # 録画を開始します
    def start_recording(self, filename = "movie.mp4", video = "/dev/video0", audio = ""):
        if self.is_recording:
            print("Video: 既に録画中なので、録画を開始できません")
            return False

        self.output_file = self.get_unique_filename(filename)

        device = AudioDevice.search_recording_device(audio)
        if device == None:
            devices = AudioDevice.get_recording_devices()
            if len(devices) > 0:
                device = devices[0]
            else:
                print("Video: 録音デバイスが見つからないので、録画を開始できません")
                return False
        
        device_text = f"hw:{device.card_id},{device.device_id}"
            
        command = ["ffmpeg",
                "-y",							# ファイル上書き
                "-f", "v4l2",					# ビデオデバイスの入力形式をVideo4Linux2に設定
                "-input_format", "mjpeg",		# 入力ビデオのフォーマットをMotionJPEGに設定
                #"-framerate", "30",			# 入力ビデオのフレームレートを30fpsに設定
                "-thread_queue_size", "81920",	# 入力ビデオのキューのサイズを設定
                "-s", "1280x720",				# 入力ビデオの解像度を1280x720に設定
                #"-s", "1920x1080",				# 入力ビデオの解像度を1920x1080に設定
                "-i", video,					# 入力ビデオのデバイスを設定
                "-f", "alsa",					# オーディオデバイスの入力形式をALSAに設定
                "-thread_queue_size", "819200",	# 入力オーディオのキューのサイズを設定
                "-ac", "2",						# 入力オーディオのチャンネル数を2に設定
                "-i", device_text,				# 入力オーディオのデバイスを設定
                "-c:v", "h264_v4l2m2m",			# 出力ビデオのコーデックをh264_v4l2m2mに設定
                "-b:v", "4M",					# 出力ビデオのビットレートを4Mbpsに設定
                #"-r", "30",					# 出力ビデオのフレームレートを30fpsに設定
                "-c:a", "aac",					# 出力オーディオのコーデックをAACに設定
                "-b:a", "128k",					# 出力オーディオのビットレートを128kbpsに設定
                "-pix_fmt", "yuv420p",			# 出力ビデオのピクセルフォーマットをyuv420pに設定
                self.output_file]
        
        command_text = " ".join(command)
        with open("ffmpeg_cmd.log", "w") as file:
            file.write(command_text)
        
        self.ffmpeg_process = subprocess.Popen(command)
        self.is_recording = True
        return True


    # 録画を停止します
    def stop_recording(self):
        if self.is_recording:
            os.kill(self.ffmpeg_process.pid, signal.SIGTERM)
            self.is_recording = False


    # 指定されたファイル名に基づいて、一意のファイル名を生成します
    # param filename: 基本となるファイル名（例："movie.mp4"）
    # return: 一意のファイル名（例："movie_0001.mp4"）
    def get_unique_filename(self, filename):
        counter = 1
        name, extension = os.path.splitext(filename)
        new_filename = f"{name}_{counter:04}{extension}"

        while os.path.exists(new_filename):
            counter += 1
            new_filename = f"{name}_{counter:04}{extension}"

        return new_filename
