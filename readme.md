```sh
python3 -m venv env
source ./env/bin/active
pip install -r requirements.txt

FLASK_ENV=development flask run --port=3333
FLASK_ENV=development flask run --host=0.0.0.0 --port=3333
```
