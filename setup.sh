#Das ist ein Script welches automatisch den Bot installiert.
echo "This Script only works on Linux Based Systems"
echo "For all other Systems there is a Tutorial on github"
sudo apt-get install -y python3-pip
pip3 install --upgrade --force-reinstall -r requirements.txt
python3 start.py