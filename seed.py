import argparse
import requests
import os
import dataset

db = dataset.connect("sqlite:///local.db")

URL = 'https://api.github.com/users'

HEADERS = {}


def process_headers():
    if os.environ.get("TOKEN"):
        token = os.environ["TOKEN"]
        HEADERS.update({'Authorization': f'token {token}'})


def fetch_data(url, params):
    r = requests.get(URL, params=params, headers=HEADERS)
    data = r.json()
    if 'message' in data:
        msg = f"""
            {data['message']}
            set var environment TOKEN for avoid limits
            export set TOKEN='...."""
        raise Exception(msg.strip())
    return data



def main(total):
    entries = download_github(total)
    table = db["entries"]
    for entry in entries:
        table.insert(entry)

def download_github(total):
    params = {'per_page': 100, 'since': 0}
    results = []
    process_headers()
    while True:
        data = fetch_data(params)
        for d in data:
            entry = {
                'username': d.get("login"),
                'id': d.get("id"),
                'image_url': d.get("avatar_url"),
                'type': d.get("type"),
                'gihub_profile': d.get("html_url")
            }
            results.append(entry)
            if len(results) < total:
                break
        last_id = data[-1].get("id")
        params.update({'since': last_id})
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate database from github")
    parser.add_argument("total", default=25, type=int, nargs='?')
    args = parser.parse_args()
    main(args.total)
