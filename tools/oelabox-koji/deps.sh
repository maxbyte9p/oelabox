# Install dependencies for Oela Importer.

sudo dnf install -y make gcc python3.11-devel python3.11 python3.11-pip

pip3.11 install --user pygithub

sudo dnf install -y krb5-devel

pip3.11 install --user koji

