import argparse
import json
import tempfile
import os

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="key name for add or search")
parser.add_argument("--value",  help="new key value")
args = parser.parse_args()
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
with open(storage_path, 'r+') as f:
    key_base = {}
    loadstr = f.readlines()
    for str in loadstr:
        key_base.update(json.loads(str))    
    if args.value:

        key_base.update({args.key: key_base[args.key] + ", " + args.value})
        f.seek(0)
        f.write(json.dumps(key_base))
    else:
        print(key_base[args.key])
