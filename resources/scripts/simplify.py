import argparse
import requests
from muss.simplify import ALLOWED_MODEL_NAMES
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='File containing the source sentences, one sentence per line.')
    parser.add_argument(
        '--model-name',
        type=str,
        default=ALLOWED_MODEL_NAMES[0],
        choices=ALLOWED_MODEL_NAMES,
        help=f'Model name to generate from. Models selected with the highest validation SARI score.',
    )
    args = parser.parse_args()
    session = requests.Session()
    url =  f'http://localhost:8000/muss/{args.filepath}/{args.model_name}'
    headers = {
            "accept": "application/json", 
            "content-type": "application/json",
          }
    response = session.get(url, headers=headers, verify=False)
    print("\n".join(str(x) for x in json.loads(response.text)))
