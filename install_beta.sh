#!/bin/bash
sudo -H pip3 install -r requirements.txt
npm install 
sudo npm install pm2@latest -g
python3 createdb.py
cd node_modules
git clone https://github.com/PersonaIam/persona-js
cd persona-js
npm install
