#Das ist ein Script welches automatisch den Bot installiert.
echo "Dieses Script Funtkioniert NUR auf Debian basierten Linux Betriebssystemen"
echo "Für alle anderen Betriebssysteme gibt es auch ein Tutorial auf Github"
sudo apt-get install -y python3-pip
pip3 install --upgrade --force-reinstall -r requirements.txt
python3 start.py