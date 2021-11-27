How to install beanbakery ERP : https://www.odoo.com/documentation/14.0/administration/install/install.html#id7
1. Install Python 3.7 and nodejs
    - dnf install python3 python3-devel git gcc redhat-rpm-config libxslt-devel bzip2-devel openldap-devel libjpeg-devel freetype-devel curl unzip -y
    - dnf install https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox-0.12.5-1.centos8.x86_64.rpm
    -  Install nodejs and : sudo npm install -g rtlcss
2. Install PostgresSQL
    - dnf install postgresql postgresql-server postgresql-contrib -y
    - postgresql-setup initdb
    - systemctl start postgresql
    - systemctl enable postgresql
    - Create Possgres user: su - postgres -c "createuser -s beanbakery"
3. Clone source code and we need to create a new system user for our Odoo installation. Make sure the username is the same as the PostgreSQL user we created in the previous step:
    - useradd -m -U -r -d /opt/beanbakery -s /bin/bash beanbakery
    - su - beanbakery
    - git clone https://github.com/Anhjean/odoo_14.git /opt/beanbakery
4. Install python dev by Virtual Env and setup Bean Bakery ERP
    - install env lib: pip install virtualenv
    - cd /opt/beanbakery && python3 -m venv beanbakery-venv
    - source beanbakery-venv/bin/activate
    - pip3 install wheel
    - pip3 install -r ./requirements.txt
    - deactivate && exit
4. Running Bean Bakery ERP
    - $ cd /CommunityPath
    - $ odoo_setup.sh
    - sudo systemctl daemon-reload
    - sudo systemctl start beanbakery
    - sudo systemctl enable odoo14
    - sudo systemctl status odoo14

5. Install nginx
    - dnf install nginx -y
    - sudo nano /etc/nginx/conf.d/yourdomain.com.conf
    - add following code
    ''''
        #odoo server
upstream odoobean {
  server 127.0.0.1:8071;
}
upstream odoobeanchat {
  server 127.0.0.1:8073;
}

# http -> https
server {
  listen 80;
  #server_name beanbakery.vn www.beanbakery.vn nhadaubakery.com;
  #rewrite ^(.*) https://beanbakery.vn permanent;
  server_name *.beanbakery.vn beanbakery.vn;
  rewrite ^(.*) https://$host$1 permanent;
}


server {
  listen 443 ssl;
  server_name erp.beanbakery.vn beanbakery.vn;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;

# Add Headers for odoo proxy mode
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;

  # SSL parameters
  # ssl on;
  ssl_certificate /etc/ssl/beanbakery_origin_cert.pem;
  ssl_certificate_key /etc/ssl/beanbakery.key;
  ssl_session_timeout 30m;
  ssl_protocols TLSv1.2;
  ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES$
  ssl_prefer_server_ciphers off;

  # log
  access_log /var/log/nginx/odoo.access.log;
  error_log /var/log/nginx/odoo.error.log;

    #Others config
  client_max_body_size 100M;

  # Redirect longpoll requests to odoo longpolling port
  location /longpolling {
    proxy_pass http://odoobeanchat;
  }

  # Redirect requests to odoo backend server
    location / {
       proxy_redirect off;
       proxy_pass http://odoobean;
    }


    # Cache static files
    location ~* /web/static/ {
        proxy_cache_valid 200 90m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://odoobean;
    }
    
    # common gzip
    gzip_types text/css text/scss text/plain text/xml application/xml application/json application/javascript;
    gzip on;
}
    ''''
