from staticanalysisweb.app import app
from pathlib import Path
from collections import defaultdict
import json

# print(f"Root paths {app.root_path}")
# print(f"Instance paths {app.instance_path}")
prio_list = [
    "7_38",
    "BlastSlam2",
    "FissurePG1",
    "Scrims",
    "2025",
]

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
                data_set_path = plot_dir / name / data_set
                if data_set_path.exists():
                    output[name]["sets"].append(meta_data[data_set]["name"])
                # else:
                #     print(f"Metadata for {name} has set {data_set} but no files in: {data_set_path}")
            output[name]["sets"].sort(key=str.lower)
            output[name]["sets"].sort(key=sort_prios, reverse=True)
        # Remove the team if we have no results for it!
        if len(output[name]["sets"]) == 0:
            output.pop(name)

    with open(out_path, "w") as f:
        json.dump(output, f)

    return output


if __name__ == "__main__":
    index = make_index()

    app.run(port=8000)
