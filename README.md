# kiosk3.1
sudo apt-get update && sudo apt-get upgrade -y
Set BC reader interface to USB_COM
install git
create directory for kiosk on RaspberryPI
sudo mkdir /opt/kiosk

set ownership to pi
sudo chown pi:pi /opt/kiosk
git clone <this repositary> /opt/kiosk/
make scripts executable
cd /opt/kiosk
chmod a+x *.py /opt/kiosk/*.sh

