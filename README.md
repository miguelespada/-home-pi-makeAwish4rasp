# makeAwish4rasp

# Scan ports
 nmap -sP 192.168.1.0/24

# Installation

1) Refresh System

sudo apt-get update
sudo apt-get upgrade

2) Install alsa drivers (if not installed in previous phase)
sudo apt-get install alsa-utils

3) Load driver
sudo modprobe snd_bcm2835

4) Selecting USB MobilePRE sound card as default
sudo nano /usr/share/alsa/alsa.conf

Search:
defaults.ctl.card 0
defaults.pcm.card 0

And change to:
defaults.ctl.card 1
defaults.pcm.card 1