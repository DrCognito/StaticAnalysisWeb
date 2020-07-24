from app import app
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from os import environ as environment
import json

prio_list = ["Ti2019Group", "Ti2019Main", "TIQuals2019", "Epi2019"]
load_dotenv(dotenv_path="setup.env")
PLOT_PATH = Path(environment['PLOT_DIRECTORY'])


def sort_prios(x: str) -> int:
    # The comparison key works more naturally with reversed list.
    for i, d_set in enumerate(prio_list[::-1]):
        if d_set == x:
            return i + 1

    return 0


def make_index(
    out_path: Path = Path("./index.json"), plot_dir: Path = Path("./static/plots")
):
    output = defaultdict(dict)
    metadata_paths = plot_dir.glob("**/meta_data.json")
    for p in metadata_paths:
        name = p.parts[-2]
        path = str(p).replace("\\", "/")
        output[name]["path"] = path
        output[name]["sets"] = list()
        with open(p, "r") as f:
            meta_data = json.load(f)
            for data_set in meta_data:
                output[name]["sets"].append(meta_data[data_set]["name"])
            output[name]["sets"].sort(key=str.lower)
            output[name]["sets"].sort(key=sort_prios, reverse=True)

    with open(out_path, "w") as f:
        json.dump(output, f)

    return output


if __name__ == "__main__":
    index = make_index(plot_dir=PLOT_PATH)

    app.run(port=8000)
