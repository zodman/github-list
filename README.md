# Fetch github

[![Coverage Status](https://coveralls.io/repos/github/zodman/github-list/badge.svg)](https://coveralls.io/github/zodman/github-list)


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
