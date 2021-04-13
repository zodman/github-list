import argparse
import requests
import os
import tqdm
import dataset

FILE_DB = "local.db"

db = dataset.connect(f"sqlite:///{FILE_DB}")

URL = 'https://api.github.com/users'

HEADERS = {}


def process_headers():
    if os.environ.get("TOKEN"):
        token = os.environ["TOKEN"]
        HEADERS.update({'Authorization': f'token {token}'})


def fetch_data(params):
    r = requests.get(URL, params=params, headers=HEADERS)
    data = r.json()
    if 'message' in data:
        msg = f"""
            {data['message']}
            set var environment TOKEN for avoid limits
            export set TOKEN='....'"""
        raise Exception(msg.strip())
    return data


def main(total):
    init()
    entries = download_github(total)
    table = db["entries"]
    for entry in tqdm.tqdm(entries, desc="inserting on sqlite"):
        table.insert(entry)


def download_github(total):
    params = {'per_page': 10, 'since': 0}
    results = []
    process_headers()
    with tqdm.tqdm(total=total, desc="fetching from GITHUB") as pbar:
        while True:
            data = fetch_data(params)
            pbar.update(params.get("per_page"))
            for d in data:
                entry = {
                    'username': d.get("login"),
                    'id': d.get("id"),
                    'image_url': d.get("avatar_url"),
                    'type': d.get("type"),
                    'github_profile': d.get("html_url")
                }
                results.append(entry)
            if len(results) >= total:
                break
            last_id = data[-1].get("id")
            params.update({'since': last_id})
    return results[:total]


def init():
    if os.path.exists(FILE_DB):
        os.remove(FILE_DB)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate database from github")
    parser.add_argument("total", default=150, type=int, nargs='?')
    args = parser.parse_args()
    main(args.total)
