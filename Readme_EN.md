# Raspberry Pi WebCam Recorder

## Introduction

I have always been a Windows user and am not familiar with Linux-based OSs. I'm also a novice in electronics, so there might be some inaccuracies. Please keep that in mind.

## Program Overview

This program records video using a webcam connected to a Raspberry Pi. 

The webcam used is Logicool C922n PRO.

## Features

- Press the tact switch to start recording; press it again to stop
- An LED (green) is lit while the program is running
- An LED (red) is lit during recording
- Video recording uses ffmpeg
- Press Ctrl+C to stop the program

## Hardware

- Raspberry Pi 4 Model B 4GB
- Logicool C922n PRO HD Stream Webcam
- LEDs with resistors
- Tact switch
- Breadboard
- Several jumper wires

## Wiring

- GPIO20 (Pin#38) -> LED Anode (+) ... Pilot lamp
- GPIO26 (Pin#37) -> LED Anode (+) ... Recording lamp
- GND (Pin#39) -> LED Cathode (-)
- GPIO21 (Pin#40) -> Tact switch terminal 1
- 3.3V (Pin#17) -> Tact switch terminal 2

## Device Image

![screenshot](https://github.com/led-mirage/Raspi4-WebCam-Recorder/assets/139528700/8ac1fb62-a812-45c4-b1ae-10e953324fb7)

## Sample Video

https://github.com/led-mirage/Raspi4-WebCam-Recorder/assets/139528700/94cbbd7b-4c5a-493d-a9fc-9ee9ca35610c

## Execution Environment

- Raspberry Pi 4 Model B 4GB
- Raspberry Pi OS 11 (bullseye)
- Python 3.9.17
- pigpio 1.78
- ffmpeg 4.3.6

## Development Environment

- Visual Studio Code 1.76.0
- pyenv 2.3.24

## Source File Structure

- main.py … Main module
- video.py … Class for recording video
- audio_device.py … Audio device utility class

## Required Modules for Execution

The following modules are needed for execution. Install them in advance if you haven't already.

- pigpio
- ffmpeg

You will need to start the pigpio daemon before running the program. For installing pigpio and starting the daemon, refer to [here](https://github.com/led-mirage/Raspi4-LEDBlink-pigpio/blob/main/Readme.md).

To install ffmpeg, execute the following command:

```bash
$ sudo apt-get install ffmpeg
```

## Configuration

Modify the constants at the beginning of main.py according to your needs.

### GPIO

Modify the following constants to match your environment.

``` py
PILOT_LED_PIN = 26  # GPIO number for LED
VIDEO_LED_PIN = 20  # GPIO number for recording LED
SWITCH_PIN = 21     # GPIO number for tact switch
```

### Devices

Modify the following constants according to your environment:

``` py
VIDEO_DEVICE = "/dev/video0"                     # Video device name
AUDIO_CARD = "Webcam [C922 Pro Stream Webcam]"   # Audio recording device card name
OUTPUT_FILE = "./output/movie.mp4"               # Output file path
```

There's usually no need to change `VIDEO_DEVICE` and `AUDIO_CARD` if you have only one recording device connected to the Raspberry Pi (such as when only one webcam is connected). The `AUDIO_CARD` constant is set by default to an identifier for the C922, but if this identifier is not found, the first audio recording device found will be used.

You can find the name of the audio recording device with the following command:

```bash
arecord -l
```

Here's an example output. The device name (or card ID) is written next to the card number.

```
**** List of CAPTURE Hardware Devices ****
card 3: Webcam [C922 Pro Stream Webcam], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

## Running the Program

### Clone

Open the terminal on your Raspberry Pi, navigate to the directory where you want to clone the program, and execute the following command.

```bash
git clone https://github.com/led-mirage/Raspi4-WebCam-Recorder.git
```

### Execute

Run the following command to start the program.

```bash
python main.py
```

### Start and Stop Recording

Press the tact switch to start recording. Press it again to stop. The LED will illuminate while recording.

### Exiting the Program

Press "Ctrl + C" in the terminal to stop the program.

## Auto-run the Program at Raspberry Pi Startup

By creating a custom systemd service, you can set this program to automatically run when the Raspberry Pi boots. Here are the steps:

### Create Service File

Create `/etc/systemd/system/webcam-recorder.service` and save the following content.

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

Please modify the following lines according to your environment:
- /usr/bin/python ... Path to the Python executable
- /home/username/webcam/ ... Folder where the program is located
- username ... Your username

To create or modify the service file, you need administrative rights. Open the text editor as an administrator and edit as shown below.

```bash
sudo nano /etc/systemd/system/webcam-recorder.service
```

If you're not comfortable with CUI, you can edit it using Visual Studio Code. When saving, you will be prompted to save it with administrative rights. I found this method easier.

### Reload the Service

After creating the service file, execute the following command to make systemd recognize the new service.

```bash
sudo systemctl daemon-reload
```

### Enable the Service

Run the following command to set the service to start automatically.

```bash
sudo systemctl enable webcam-recorder.service
```

### Start the Service

To start the service immediately, execute the following command.

```bash
sudo systemctl start webcam-recorder.service
```

### Stop the Service

If you wish to stop the service, execute the following command.

```bash
sudo systemctl stop webcam-recorder.service
```

### Disable the Service

If you want to stop the service from running automatically, run the following command.

```bash
sudo systemctl disable webcam-recorder.service
```

## Struggles

Having no knowledge of video and being unfamiliar with ffmpeg, I struggled a lot with setting ffmpeg options. To be honest, I'm still not sure if these are the best settings. The configuration below is the result of trial and error.

```python
command = ["ffmpeg",
        "-y",                            # Overwrite existing files
        "-f", "v4l2",                    # Set input format of video device to Video4Linux2
        "-input_format", "mjpeg",        # Set format of input video to MotionJPEG
        #"-framerate", "30",             # Set frame rate of input video to 30fps
        "-thread_queue_size", "81920",   # Set queue size for input video
        "-s", "1280x720",                # Set resolution of input video to 1280x720
        #"-s", "1920x1080",              # Set resolution of input video to 1920x1080
        "-i", video,                     # Set input video device
        "-f", "alsa",                    # Set input format of audio device to ALSA
        "-thread_queue_size", "819200",  # Set queue size for input audio
        "-ac", "2",                      # Set number of input audio channels to 2
        "-i", device_text,               # Set input audio device
        "-c:v", "h264_v4l2m2m",          # Set codec of output video to h264_v4l2m2m
        "-b:v", "4M",                    # Set bitrate of output video to 4Mbps
        #"-r", "30",                     # Set frame rate of output video to 30fps
        "-c:a", "aac",                   # Set codec of output audio to AAC
        "-b:a", "128k",                  # Set bitrate of output audio to 128kbps
        "-pix_fmt", "yuv420p",           # Set pixel format of output video to yuv420p
        self.output_file]
```

One key point in this setup is the use of the hardware encoder (h264_v4l2m2m) for the output video codec and specifying mjpeg as the input video format.

Initially, I tried using h264_omx for the codec, but it didn't work well. I also tried the software encoder libx264 but wasn't satisfied with the results, so I ultimately chose h264_v4l2m2m.

As for the input video format, I experimented with yuyv422, but the FPS was only about one-third that of mjpeg. Therefore, I ultimately went with mjpeg.

Also, with this setup, recording for one hour results in a file size of around 1.8GB. If you want to reduce the file size, you can lower the bitrate from its current setting. However, this comes with the trade-off of decreased image quality. Conversely, if you wish to improve the image quality, please increase the bitrate.

In terms of resolution, while I would like to use 1980x1080, I've opted for 1280x720 due to the memory issues mentioned below. If you're only capturing short videos of around 10 minutes or are using the Raspberry Pi 8GB model, then using 1920x1080 should be fine.

## Issues (Memory Usage)

During recording, memory consumption increases over time. As a result, if you record for an extended period, you will run out of memory, causing ffmpeg to forcibly terminate. This also happens when running ffmpeg alone, so the choice of ffmpeg options might be the issue.

Recording at a resolution of 1920x1080 consumes all the memory in about 30 minutes (the Raspberry Pi I'm using has 4GB of memory). With 1280x720, the limit is about one hour. Below are the memory states before starting the recording and one hour after starting.

### Before Starting the Recording (1280x720)

```bash
$ free -m
       total        used        free      shared  buff/cache   available
Mem:    3794         264        1175          44        2354        3410
Swap:     99          99           0
```

### One Hour After Starting the Recording (1280x720)

```bash
$ free -m
       total        used        free      shared  buff/cache   available
Mem:    3794        3177          74          44         541         496
Swap:     99          84          15
```

One hour later, almost 80% of the memory is consumed. After a while, ffmpeg may throw an error and terminate

### Thoughts

Finally, I would like to list some impressions after making and actually using it.

Pros:

- The DIY aspect is fun.
- You can have fun with your existing webcam and Raspberry Pi.

Cons:

- The quality of the image is not that great.
- The background tends to be overexposed when shooting outdoors.
- The auto white balance can sometimes produce unintended color tones.

If you just look at the functionality, smartphones are far superior. However, making this gives you a new appreciation for how great smartphones are. On the other hand, this has its own merits. If you enjoy programming or appreciate the DIY aspect, you might find it fun to try making one. There are many challenges, but also many discoveries.

See you again.

## Version History

### 1.0 (2023/08/19)
- First Release

---
This document was translated into English by ChatGPT.
