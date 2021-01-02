#Das ist ein Script welches automatisch den Bot installiert.
sudo apt-get install -y python3-pip
sudo apt-get install -y git
pip3 install discord.py
git clone https://github.com/antonstech/simplediscordbot
cd simplediscordbot
python3 main.py
