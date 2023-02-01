# kiosk3.1
Set BC reader interface to USB_COM
install git
create directory for kiosk on RaspberryPI
sudo mkdir /opt/kiosk

set ownership to pi
sudo chown pi:pi /opt/kiosk

make scripts executable: chmod a+x /opt/kiosk/*.py /opt/kiosk/*.sh
git clone <this repositary.
