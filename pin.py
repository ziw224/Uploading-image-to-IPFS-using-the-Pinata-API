import subprocess
import sys 
import json
from copy import deepcopy

img_path = sys.argv[1]
metadata_path = sys.argv[2]

print("img_path: ", img_path)

node_path = '/usr/local/bin/node'

# jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIwNTQwMTRmMi00MjlmLTQ0ODMtYjJjYi0zN2Q0MDk3YTliMzYiLCJlbWFpbCI6InppdzIyNEBsZWhpZ2guZWR1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6ImEzZTQ1NzA5ZWJhMWZlMTNhNjE0Iiwic2NvcGVkS2V5U2VjcmV0IjoiYmNiYWUzODdjNGE2NjIzN2E1NDkyZTIyMTAxYzEzNDkzZmUzN2Y3NWQxY2NmM2JkNzgwZTRmMjJkZGE5YjE4OSIsImlhdCI6MTY1NzYwMjIxMH0.Cje8oVBKxqsubgg-FzGKyfPZDv4sd4nrav-ifip4uRw'
base_metadata = json.load(open(metadata_path))
metadata_hashes = json.load(open('./metadata_hashes.json'))
metadata_hashes[img_path] = []

def pin_img_to_pinata(img_path):
    ipfs_hash = subprocess.check_output([f'{node_path}','./_pinImgToPinata.js', img_path])
    return ipfs_hash.decode().strip()
     
def pin_metadata_to_pinata(img_ipfs_hash, edition_index):
    metadata = deepcopy(base_metadata)
    metadata['image'] = base_metadata['image'] + img_ipfs_hash
    metadata['attributes'].append({'display_type': 'number', 'trait_type': 'Edition', 'max_value': 10, 'value': edition_index + 1})
    metadata_ipfs_hash = subprocess.check_output([node_path,'./_pinMetadataToPinata.js', json.dumps(metadata), str(edition_index+1)])
    return metadata_ipfs_hash.decode().strip()

img_ipfs_hash = pin_img_to_pinata(img_path)

for i in range(0, base_metadata['total_editions']):
    metadata_hash = pin_metadata_to_pinata(img_ipfs_hash, i)
    metadata_hashes[img_path].append(metadata_hash)
    print(f'Edition: {i+1}; Metadata Hash: {metadata_hash}')

json.dump(metadata_hashes, open('./metadata_hashes.json', 'w'))
print("Done")
