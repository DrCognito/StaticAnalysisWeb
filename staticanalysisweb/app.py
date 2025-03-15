from itertools import zip_longest
from json import load as json_load
from pathlib import Path
from urllib.parse import unquote
from flask import Flask, abort, render_template, url_for
import staticanalysisweb.plot_routes as plot_routes


app = Flask(__name__)
app.register_blueprint(plot_routes.plot_routes)
current_dir = Path.cwd()


def get_metadata_locations(path: Path) -> dict:
    output = {}
    metadata_paths = path.glob("**/meta_data.json")
    for p in metadata_paths:
        name = p.parts[-2]
        output[name] = p

    return output


metadata_dict = {}


def update_meta_dict(index: Path = ("./index.json")):
    with open(index, "r") as f:
        global metadata_dict
        metadata_dict = json_load(f)

    return metadata_dict


data_summary_dir = Path("./static/data_summary")


def url_path(path_in: str, endpoint="static", fourohfour = True):
    if path_in is not None:
        path_in = path_in.replace("\\", "/")
        path_in = "plots/" + path_in
    elif fourohfour:
        path_in = "404.png"
    else:
        return None
    return url_for(endpoint, filename=path_in)


def get_meta_nav():
    meta_json = Path('./static/meta_plots/meta.json')
    # Categories of meta to add to navs
    categories = ["Division 1", "Division 2", "Tournaments", "Pubs", "Pub Regions"]
    navigators = {}
    if meta_json.exists():
        with open(meta_json, 'r') as f:
            meta_plots: dict = json_load(f)
            for c in categories:
                if c in meta_plots:
                    navigators[c] = []
                    for league in meta_plots[c]:
                        navigators[c] += [(league, url_for("meta", category=c, league=league))]
                    # navigators += [(None, None)]

    return navigators


def get_team_nav(team, dataset):
    """Produces name, url_for pairs for a teams sidebar.
       To be used with the sidebar templates.
    """
    navigators = {}
    navigators['top'] = [("Back", url_for("index"))]
    navigators['top'] += [(team, url_for("team", team=team, dataset=dataset))]
    # if len(metadata_dict[team]['sets']) > 1:
    #     navigators += [(None, "__dataset__")]
    # else:
    #     navigators += [(metadata_dict[team]['sets'][0], None)]
    navigators['top'] += [(None, "__dataset__")]
    navigators['top'] += [("Drafts 1st Pick", url_for("plots.draft", team=team, dataset=dataset, postfix="_first"))]
    navigators['top'] += [("Drafts 2nd Pick", url_for("plots.draft", team=team, dataset=dataset, postfix="_second"))]
    navigators['top'] += [("Drafts All", url_for("plots.draft", team=team, dataset=dataset, postfix="_all"))]
    # navigators += [("DIRE", None)]
    # Dire
    navigators['dire'] = [
        ("Drafts", url_for("plots.draft", team=team, side="dire", dataset=dataset))
    ]
    # Change plot to 'wards' for normal aggregate ward plots
    navigators['dire'] += [
        (
            "Wards",
            url_for("plots.wards_separate", team=team, side="dire", dataset=dataset),
        )
    ]
    navigators['dire'] += [
        (
            "Ward Summary",
            url_for("plots.wards", team=team, side="dire", dataset=dataset),
        )
    ]
    navigators['dire'] += [
        (
            "Pre-game Routes",
            url_for("plots.pregame_positioning", team=team,
                    side="dire", dataset=dataset),
        )
    ]
    navigators['dire'] += [
        (
            "Positioning",
            url_for("plots.positioning", team=team, side="dire", dataset=dataset),
        )
    ]
    navigators['dire'] += [
        ("Runes", url_for("plots.rune", team=team, side="dire", dataset=dataset))
    ]
    navigators['dire'] += [
        ("Smokes", url_for("plots.smoke", team=team, side="dire", dataset=dataset))
    ]
    navigators['dire'] += [
        (
            "Tormentors",
            url_for("plots.tormentor_routes", team=team,
                    side="dire", dataset=dataset),
        )
    ]
    # navigators['dire'] += [
    #     ("Scans", url_for("plots.scan", team=team, side="dire", dataset=dataset))
    # ]

    # Radiant
    navigators['radiant'] = [
        ("Drafts", url_for("plots.draft", team=team, side="radiant", dataset=dataset))
    ]
    # Change plot to 'wards' for normal aggregate ward plots
    navigators['radiant'] += [
        (
            "Wards",
            url_for("plots.wards_separate", team=team, side="radiant", dataset=dataset),
        )
    ]
    navigators['radiant'] += [
        (
            "Ward Summary",
            url_for("plots.wards", team=team, side="radiant", dataset=dataset),
        )
    ]
    navigators['radiant'] += [
        (
            "Pre-game Routes",
            url_for("plots.pregame_positioning", team=team,
                    side="radiant", dataset=dataset),
        )
    ]
    navigators['radiant'] += [
        (
            "Positioning",
            url_for("plots.positioning", team=team, side="radiant", dataset=dataset),
        )
    ]
    navigators['radiant'] += [
        ("Runes", url_for("plots.rune", team=team, side="radiant", dataset=dataset))
    ]
    navigators['radiant'] += [
        ("Smokes", url_for("plots.smoke", team=team, side="radiant", dataset=dataset))
    ]
    navigators['radiant'] += [
        (
            "Tormentors",
            url_for("plots.tormentor_routes", team=team,
                    side="radiant", dataset=dataset),
        )
    ]
    # navigators['radiant'] += [
    #     ("Scans", url_for("plots.scan", team=team, side="radiant", dataset=dataset))
    # ]

    navigators['summary'] = [("Summary", url_for("summary", team=team, dataset=dataset))]
    navigators['summary'] += [("Summary (last 5)", url_for("summary", team=team, dataset=dataset, postfix="limit5"))]
    navigators['summary'] += [("Counters", url_for("counters", team=team, dataset=dataset))]

    navigators['summary'] += [(
        "Report",
        url_for("plots.pdf_report", team=team, dataset=dataset))
    ]
    navigators['summary'] += [(
        "Mini Report",
        url_for("plots.pdf_mini_report", team=team, dataset=dataset))
    ]

    return navigators


def get_nav_report():
    """Produces navbar for reports with simple internal link.
    """
    navigators = [(team, "#top")]

    navigators += [("RADIANT", "#radiant")]
    navigators += [("Drafts", "#radiant_draft")]
    navigators += [("Wards", "#radiant_wards")]
    navigators += [("Positioning", "#radiant_pos")]
    navigators += [("Smokes", "#radiant_smoke")]
    
    navigators += [("DIRE", "#dire")]
    navigators += [("Drafts", "#dire_draft")]
    navigators += [("Wards", "#dire_wards")]
    navigators += [("Positioning", "#dire_pos")]
    navigators += [("Smokes", "#dire_smoke")]
    # navigators += [("Scans", "#dire_scan")]

    # navigators += [("Scans", "#radiant_scan")]

    navigators += [(None, None)]
    navigators += [("Summary", "#summary")]

    return navigators


def get_team_summary(team, dataset="default", postfix="") -> dict:
    update_meta_dict()
    """Returns a dictionary of summary plots with url_for links"""
    with open(current_dir / metadata_dict[team]["path"], "r") as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)

        data = json_file[dataset]

        summary_dict = {}
        summary_dict["draft_summary"] = url_path(data.get(f"plot_draft_summary{postfix}"), fourohfour=False)
        summary_dict["hero_picks"] = url_path(data.get(f"plot_hero_picks{postfix}"), fourohfour=False)
        summary_dict["hero_picks_portrait"] = url_path(data.get(f"hero_picks_portrait"), fourohfour=False)
        summary_dict["hero_flex"] = url_path(data.get(f"plot_hero_flex{postfix}"), fourohfour=False)
        summary_dict["flex_pubs"] = url_path(data.get(f"plot_flex_pubs"), fourohfour=False)
        summary_dict["pair_picks"] = url_path(data.get(f"plot_pair_picks{postfix}"), fourohfour=False)
        summary_dict["pick_context"] = url_path(data.get(f"plot_pick_context{postfix}"), fourohfour=False)
        summary_dict["win_rate"] = url_path(data.get(f"plot_win_rate{postfix}"), fourohfour=False)
        summary_dict["rune"] = url_path(data.get(f"plot_rune_control{postfix}"), fourohfour=False)
        summary_dict["pick_priority"] = url_path(data.get(f"pick_priority"), fourohfour=False)
        if postfix == "":
            summary_dict["pick_table"] = url_path(data.get("plot_picktables", None), fourohfour=False)
        else:
            summary_dict["pick_table"] = None

        return summary_dict


def get_counters(team, dataset):
    update_meta_dict()
    with open(current_dir / metadata_dict[team]["path"], "r") as file:
        json_file = json_load(file)

    if dataset not in json_file:
        abort(404)

    data = json_file[dataset]

    counters = {}
    for hero, path in data["counter_picks"].items():
        counters[hero] = url_path(path)

    return counters


def render_plot_template(team, side, plot, dataset="default", postfix=""):
    if side not in ["dire", "radiant"]:
        abort(404)
    if plot not in ["draft", "wards", "positioning", "smoke", "scan",
                    "wards_seperate", "pregame_positioning"]:
        abort(404)

    with open(current_dir / metadata_dict[team]["path"], "r") as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)

        data = json_file[dataset]
        navigators = get_team_nav(team, dataset)
        plots = {}
        if plot == "draft":
            plots["drafts_link"] = "#{}_drafts".format(side)
            if data["plot_{}_drafts".format(side)] is not None:
                plots["plot_drafts"] = url_path(data["plot_{}_drafts".format(side)])

            return render_template(
                "plots/draft.j2", plots=plots, navigators=navigators, team=team
            )

        if plot == "wards":
            plots["ward_title"] = data["plot_ward_names"]
            plots["ward_plots"] = [
                "plots/" + p.replace("\\", "/")
                for p in data["plot_ward_{}".format(side)]
            ]
            n_replays = len(data.get(f"replays_{side}", default = []))

            return render_template(
                "plots/warding.j2", plots=plots, navigators=navigators, team=team, replays=n_replays
            )
        if plot == "wards_seperate":

            # plots["ward_plots_separate"] = data['plot_ward_names']
            plots["ward_plots_separate"] = {
                k: "plots/" + v.replace("\\", "/")
                for k, v in data["wards_{}".format(side)].items()
            }

            return render_template(
                "plots/warding_seperate.j2",
                plots=plots,
                navigators=navigators,
                team=team,
            )

        if plot == "positioning":
            plots["pos_names"] = data["player_names"]
            plots["pos_plots"] = [
                "plots/" + p.replace("\\", "/")
                for p in data["plot_pos_{}".format(side)]
            ]
            return render_template(
                "plots/positioning.j2", plots=plots, navigators=navigators, team=team
            )

        if plot == "smoke":
            if data["plot_smoke_{}".format(side)] is not None:
                plots["smoke"] = url_path(data["plot_smoke_{}".format(side)])
            if data[f"table_smoke_{side}"] is not None:
                plots["smoke_table"] = data[f"table_smoke_{side}"]
            else:
                plots["smoke_table"] = None
            return render_template(
                "plots/smoke.j2", plots=plots, navigators=navigators, team=team
            )

        if plot == "scan":
            if data["plot_scan_{}".format(side)] is not None:
                plots["scan"] = url_path(data["plot_scan_{}".format(side)])
            return render_template(
                "plots/scan.j2", plots=plots, navigators=navigators, team=team
            )

        if plot == "pregame_positioning":
            try:
                if data[f"pregame_routes_{side}"] is not None:
                    plots["pregame_positioning"] = url_path(data[f"pregame_routes_{side}"])
            except KeyError:
                abort(404)
            return render_template(
                "plots/pregame_positioning.j2", plots=plots,
                navigators=navigators, team=team
            )


@app.route("/")
def index():
    # Update our team index and datasets
    update_meta_dict()
    teams = list(metadata_dict.keys())
    teams.sort(key=str.lower)
    navigators = []
    for team in teams:
        try:
            dataset = metadata_dict[team]["sets"][0]
        except (KeyError, IndexError):
            print(f"Missing data for {team}")
        url = url_for("team", team=team, dataset=dataset)
        navigators.append((team, url))
    # navigators.append((None, None))
    # navigators.append(("Summaries", url_for("data_summary")))
    return render_template("index.j2", navigators=navigators)


@app.route("/<string:team>/<string:dataset>/")
def team(team, dataset):
    # Update our team index and datasets
    update_meta_dict()
    team = unquote(team)
    dataset = unquote(dataset)
    if team not in metadata_dict:
        abort(404)
    if dataset not in metadata_dict[team]["sets"]:
        abort(404)
    with open(current_dir / metadata_dict[team]["path"], "r") as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)

        data = json_file[dataset]
        general_stats = json_file.get("general_stats")
        navigators = get_team_nav(team, dataset)
        dire = data["replays_dire"]
        radiant = data["replays_radiant"]
        if dire:
            dire.sort(reverse=True)
        else:
            dire = []
        if radiant:
            radiant.sort(reverse=True)
        else:
            radiant = []
        replay_list = list(zip_longest(dire, radiant))

        dire_drafts = data.get('drafts_only_dire')
        radiant_drafts = data.get('drafts_only_radiant')
        time_string = data.get('time_string')
        drafts_only = None
        if dire_drafts:
            dire_drafts = [x for x in dire_drafts if x not in dire]
            dire_drafts.sort(reverse=True)
        if radiant_drafts:
            radiant_drafts = [x for x in radiant_drafts if x not in radiant]
            radiant_drafts.sort(reverse=True)
        if dire_drafts or radiant_drafts:
            drafts_only = list(zip_longest(dire_drafts, radiant_drafts))
        return render_template(
            "replays.j2",
            navigators=navigators,
            replays=replay_list,
            drafts_only=drafts_only,
            team=team,
            dataset_list=metadata_dict[team]["sets"],
            winrates=data["stat_win_rate"],
            time_string=time_string,
            general_stats=general_stats
        )


@app.route("/<string:team>/<string:dataset>/summary/")
@app.route("/<string:team>/<string:dataset>/summary<string:postfix>/")
def summary(team, dataset="default", postfix=""):
    update_meta_dict()
    team = unquote(team)
    dataset = unquote(dataset)
    if team not in metadata_dict:
        abort(404)
    navigators = get_team_nav(team, dataset)

    summary = get_team_summary(team, dataset, postfix=postfix)
    return render_template(
        "plots/summary.j2",
        navigators=navigators,
        summary=summary,
        team=team,
        dataset_list=metadata_dict[team]["sets"],
        provider="summary",
    )


@app.route("/<string:team>/<string:dataset>/counters/<string:hero>.html")
@app.route("/<string:team>/<string:dataset>/counters/")
def counters(team, dataset, hero=None):
    update_meta_dict()
    team = unquote(team)
    dataset = unquote(dataset)
    if team not in metadata_dict:
        abort(404)
    navigators = get_team_nav(team, dataset)
    summary = get_team_summary(team, dataset)
    return render_template(
        "plots/counters.j2",
        navigators=navigators,
        summary=summary,
        team=team,
        set=dataset,
        dataset_list=metadata_dict[team]["sets"],
        counter_picks=get_counters(team, dataset),
        hero=hero,
    )


# @app.route("/data_summary.html")
def data_summary():
    navigators = []
    for team in metadata_dict:
        url = url_for("team", team=team)
        navigators.append((team, url))
    navigators.append((None, None))
    navigators.append(("Summaries", url_for("data_summary")))
    # Wards
    plots = {}
    dire_wards = data_summary_dir / "wards_dire.png"
    radiant_wards = data_summary_dir / "wards_radiant.png"

    if dire_wards.is_file():
        plots["wards_dire"] = "data_summary/wards_dire.png"
    if radiant_wards.is_file():
        plots["wards_radiant"] = "data_summary/wards_radiant.png"

    return render_template("plots/data_summary.j2", navigators=navigators, plots=plots)


@app.route("/<string:team>/<string:dataset>/<string:side>/<string:plot>.html")
def serve_plots(team, dataset, side, plot):
    team = unquote(team)
    update_meta_dict()
    if team not in metadata_dict:
        abort(404)
    return render_plot_template(team, side, plot, dataset=dataset)


@app.route("/<string:team>/report/")
def report(team, dataset="default"):
    team = unquote(team)
    if team not in metadata_dict:
        abort(404)

    navigators = get_nav_report()
    dire = {}
    radiant = {}
    with open(metadata_dict[team], "r") as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)
        data = json_file[dataset]

        # replays
        dire_replays = data["replays_dire"]
        dire_replays.sort(reverse=True)
        radiant_replays = data["replays_radiant"]
        radiant_replays.sort(reverse=True)
        replay_list = list(zip_longest(dire_replays, radiant_replays))
        # win rates
        winrates = data["stat_win_rate"]

        # drafts
        dire["drafts_link"] = "#dire_drafts"
        if data["plot_dire_drafts"] is not None:
            dire["plot_drafts"] = url_path(data["plot_dire_drafts"])
        radiant["drafts_link"] = "#radiant_drafts"
        if data["plot_radiant_drafts"] is not None:
            radiant["plot_drafts"] = url_path(data["plot_radiant_drafts"])

        # wards
        dire["ward_title"] = data["plot_ward_names"]
        dire["ward_plots"] = [
            "plots/" + p.replace("\\", "/") for p in data["plot_ward_dire"]
        ]
        radiant["ward_title"] = data["plot_ward_names"]
        radiant["ward_plots"] = [
            "plots/" + p.replace("\\", "/") for p in data["plot_ward_radiant"]
        ]

        # positioning
        dire["pos_names"] = data["player_names"]
        dire["pos_plots"] = [
            "plots/" + p.replace("\\", "/") for p in data["plot_pos_dire"]
        ]
        radiant["pos_names"] = data["player_names"]
        radiant["pos_plots"] = [
            "plots/" + p.replace("\\", "/") for p in data["plot_pos_radiant"]
        ]

        # smoke
        if data["plot_smoke_dire"] is not None:
            dire["smoke"] = url_path(data["plot_smoke_dire"])
        if data["plot_smoke_radiant"] is not None:
            radiant["smoke"] = url_path(data["plot_smoke_radiant"])

        # scans
        if data["plot_scan_dire"] is not None:
            dire["scan"] = url_path(data["plot_scan_dire"])
        if data["plot_scan_radiant"] is not None:
            radiant["scan"] = url_path(data["plot_scan_radiant"])

    summary = get_team_summary(team)

    return render_template(
        "plots/report.j2",
        navigators=navigators,
        replays=replay_list,
        winrates=winrates,
        dire=dire,
        radiant=radiant,
        summary=summary,
        team=team,
    )

@app.route("/meta/")
@app.route("/meta/<string:category>/<string:league>.html")
def meta(league=None, category=None):
    plot = None
    if league is not None and category is not None:
        meta_json = Path('./static/meta_plots/meta.json')
        if meta_json.exists():
            with open(meta_json, 'r') as f:
                meta_plots: dict = json_load(f)
                plot = {}
                try:
                    plots = meta_plots[category][league]
                    if isinstance(plots, dict):
                        for type, p in meta_plots[category][league].items():
                            plot[type] = f"meta_plots/{p}"
                    if isinstance(plots, str):
                        plot['basic'] = f"meta_plots/{plots}"
                except KeyError:
                    abort(404)
    # if league is None and category is not None:
    #     meta_json = Path('./static/meta_plots/meta.json')
    #     if meta_json.exists():
    #         with open(meta_json, 'r') as f:
    #             meta_plots: dict = json_load(f)
    #             plot = {}
    #             try:
    #                 plots = meta_plots[category][league]
                    
    #                 for type, p in .items():
    #                     plot["all"] = f"meta_plots/{p}"
    #             except KeyError:
    #                 abort(404)
    navigators = get_meta_nav()
    return render_template("meta.j2", navigators=navigators,
                           league=league, plot=plot, category=category)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.j2"), 404


def team():
    for p in metadata_dict.keys():
        yield {"team": p}


def report():
    for p in metadata_dict.keys():
        yield {"team": p}
