sudo chown odoo:odoo /opt/beanbakery
sudo su - odoo
cd /opt/beanbakery
mkdir ./.local
mkdir ./.local/log
mkdir ./.local/odoo
cp ./custom-addons/odoo.conf /etc/
exit
sudo chown -R odoo: .local/log 
sudo cp  /opt/beanbakery/custom-addons/beanbakery.service /etc/systemd/system/

