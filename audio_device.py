"""
Raspberry Pi WebCam Recorder
オーディオデバイス・ユーティリティークラス

Copylight (c) 2023 led-mirage
"""

import subprocess


# オーディオデバイスクラス
class AudioDevice:
    # コンストラクタ
    def __init__(self, card_id, card_name, device_id, device_name):
        self.card_id = card_id
        self.card_name = card_name
        self.device_id = device_id
        self.device_name = device_name


    # 「arecord -l」を使って録音デバイスのリストを取得します
    @classmethod
    def get_recording_devices(cls):
        env = {"LANG": "en_US.UTF-8"} # 英語のロケールを設定
        result = subprocess.run(["arecord", "-l"], env=env, stdout=subprocess.PIPE, text=True)
        devices = result.stdout.split("\n")
        
        audio_devices = []

        for device in devices:
            if "card" in device:
                parts = device.split(",")
                card_parts = parts[0].split()
                card_id = card_parts[1].strip(":")
                card_name = " ".join(card_parts[2:])
                device_parts = parts[1].split()
                device_id = device_parts[1].strip(":")
                device_name = " ".join(device_parts[2:])
                audio_devices.append(AudioDevice(card_id, card_name, device_id, device_name))

        return audio_devices


    # 録音デバイスの中から、特定のカード名を持つデバイスを取得します
    @classmethod
    def search_recording_device(cls, card_name):
        devices = cls.get_recording_devices()
        for device in devices:
            if device.card_name == card_name:
                return device
        return None
