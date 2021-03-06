import json as js
import pathlib
import app


class AbstractPlot:
    def __init__(self, metadata_path: pathlib.Path, dataset: str):
        with open(metadata_path, "r") as file:
            self.metadata = js.load(file)
        self.dataset = dataset

    def plot_vars(self, side: str):
        pass


class Drafts(AbstractPlot):
    def plot_vars(self, side: str):

        data = self.metadata[self.dataset]
        plots = {}
        plots["drafts_link"] = "#{}_drafts".format(side)
        if data["plot_{}_drafts".format(side)] is not None:
            plots["plot_drafts"] = app.url_path(data["plot_{}_drafts".format(side)])

        return plots


class Wards(AbstractPlot):
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
