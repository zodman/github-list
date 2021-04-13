# Fetch github

[![Coverage Status](https://coveralls.io/repos/github/zodman/github-list/badge.svg)](https://coveralls.io/github/zodman/github-list)

[![CI](https://github.com/zodman/github-list/actions/workflows/ci.yml/badge.svg)](https://github.com/zodman/github-list/actions/workflows/ci.yml)



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
* Testing
```bash
source .env/bin/activate
fab test
python -m http.server  --directory htmlcov/
```

![](https://i.imgur.com/rr5fYwJ.png)


Timelapse:

6pm-8pm build the seed.py
10pm-11pm unittest of seed.py
11-1am flask app and unittest
1am-2am deploy on ci

total:  ~7hrs
