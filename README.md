# family-robot

## main
workflow.py --the overall workflow

hardware.py --all the hardware

qrgenerate.py --transfer an audio into a qr code



## Setup


Raspberry Pi OS --> SD card with Raspberry Pi Imager
```
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

```
sudo apt install python3-opencv python3-pyzbar

cd ~/
python3 -m venv venv
source ./venv/bin/activate

pip install rpi_ws281x
# if cannot pip：https://blog.csdn.net/qq_25439417/article/details/139485697

# To install robot hat related hardware:
sudo apt install git python3-pip python3-setuptools python3-smbus
cd ~/
git clone -b v2.0 https://github.com/sunfounder/robot-hat.git
cd robot-hat
python setup.py install
cd ~/robot-hat
sudo bash i2samp.sh
# you will be prompted to reboot
```


```
# /boot/firmware/config.txt
core_freq=500
core_freq_min=500
```


### LED Connection
- 3.3V, GND, MO



```
git clone git@github.com:hxn111/family-robot.git
source ./venv/bin/activate

cd family-robot

```