# kiosk3.1 installation
sudo apt-get update && sudo apt-get upgrade -y
Set BC reader interface to USB_COM
i nstall git
create directory for kiosk on RaspberryPI
sudo mkdir /opt/kiosk

set ownership to pi
sudo chown pi:pi /opt/kiosk
git clone <this repositary> /opt/kiosk/
make scripts executable
cd /opt/kiosk
chmod a+x *.py *.sh *.ini
kiosk.ini should have execute permission!!!

Launch configuration script. This will install required libraries and configure system. Check with sudo raspi_config
sudo ./preppi.sh
