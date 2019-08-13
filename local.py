from app import app
from pathlib import Path
from collections import defaultdict
import json

prio_list = ["TIQuals2019", "Ti2019Main"]


def sort_prios(x: str) -> int:
    # The comparison key works more naturally with reversed list.
    for i, d_set in enumerate(prio_list[::-1]):
        if d_set == x:
            return i + 1

    return 0


def make_index(out_path: Path = Path('./index.json'),
               plot_dir: Path = Path('./static/plots')):
    output = defaultdict(dict)
    metadata_paths = plot_dir.glob('**/meta_data.json')
    for p in metadata_paths:
        name = p.parts[-2]
        path = str(p).replace("\\", "/")
        output[name]['path'] = path
        output[name]['sets'] = list()
        with open(p, 'r') as f:
            meta_data = json.load(f)
            for data_set in meta_data:
                output[name]['sets'].append(meta_data[data_set]['name'])
            output[name]['sets'].sort(key=str.lower)
            output[name]['sets'].sort(key=sort_prios, reverse=True)
            print(output[name]['sets'])

    with open(out_path, 'w') as f:
        json.dump(output, f)

    return output


if __name__ == '__main__':
    index = make_index()

    app.run(port=8000)
