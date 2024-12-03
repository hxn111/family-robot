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

### Add these to config file
```
# /boot/firmware/config.txt
core_freq=500
core_freq_min=500
```


### LED Connection
- 3.3V, GND, MO


### Installing Redis
```
# install redis
sudo apt-get install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis

sudo systemctl enable redis-server
sudo systemctl start redis-server
```


### Installing robot code and dependencies
```
git clone git@github.com:hxn111/family-robot.git
source ./venv/bin/activate
cd family-robot
pip install -r requirements.txt
```

## Configuration
In `family-robot/config.py`, you'll need to modify some paths, and the MIC device code. 