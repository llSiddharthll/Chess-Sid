echo "BUILD START"
pip install --upgrade pip
pip3 install -r requirements.txt
python3.9 manage.py makemigrations
python3.9 manage.py migrate
echo "BUILD DONE"