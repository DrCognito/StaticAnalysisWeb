import json as js
import pathlib
import staticanalysisweb.app as app


class AbstractPlot:
    def __init__(self, metadata_path: pathlib.Path, dataset: str):
        with open(metadata_path, "r") as file:
            self.metadata = js.load(file)
        self.dataset = dataset

    def plot_vars(self, side: str):
        pass


class Drafts(AbstractPlot):
    def plot_vars(self, key: str):

        data = self.metadata[self.dataset]
        plots = {}
        plots["drafts_link"] = f"#{key}"

        if type(drafts := data[key]) is str:
            plots["plot_drafts"] = app.url_path(drafts)
        if type(drafts) is list:
            plots["plot_drafts"] = []
            for draft in drafts:
                plots["plot_drafts"].append(app.url_path(draft))
        return plots


class Wards(AbstractPlot):
    def n_replays(self, side: str):
        data = self.metadata[self.dataset]
        replays = data.get(f"replays_{side}", [])
        if replays:
            n_replays = len(replays)
        else:
            n_replays = 0

        return n_replays

    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        plots["ward_title"] = data["plot_ward_names"]
        plots["ward_plots"] = [
            "plots/" + p.replace("\\", "/") for p in data["plot_ward_{}".format(side)]
        ]

        return plots


class WardsSeparate(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        plots["ward_plots_separate"] = {
            k: "plots/" + v.replace("\\", "/")
            for k, v in data["wards_{}".format(side)].items()
        }

        return plots


class PregamePositioning(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        try:
            plots["pregame_positioning"] = ["plots/" + p.replace("\\", "/") for p in data[f"pregame_routes_{side}"]]
        except KeyError:
            pass

        return plots


class Positioning(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        plots["pos_names"] = data["player_names"]
        plots["pos_plots"] = [
            "plots/" + p.replace("\\", "/") for p in data["plot_pos_{}".format(side)]
        ]

        return plots


class Smoke(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        if data["plot_smoke_{}".format(side)] is not None:
            plots["smoke"] = app.url_path(data["plot_smoke_{}".format(side)])

        return plots


class Scan(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        if data["plot_scan_{}".format(side)] is not None:
            plots["scan"] = app.url_path(data["plot_scan_{}".format(side)])

        return plots


class Rune(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]

        key = f"rune_routes_7m_{side}"
        plots = [app.url_path(p) for p in data.get(key, [])]

        return plots


class PDFReport(AbstractPlot):
    def plot_vars(self):
        data = self.metadata[self.dataset]
        report = data.get('pdf_report')
        if report:
            report = pathlib.Path(report)

        return report


class PDFMiniReport(AbstractPlot):
    def plot_vars(self):
        data = self.metadata[self.dataset]
        report = data.get('pdf_mini_report')
        if report:
            report = pathlib.Path(report)

        return report
