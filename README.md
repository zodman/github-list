# Fetch github

* Install
```bash
yarn install
yarn run build
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
# optional
# export set TOKEN='<github_token>' to avoid limits
python seed.py 
flask run

```
