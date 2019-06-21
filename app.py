import sys
from itertools import zip_longest
from json import load as json_load
from os import environ
from pathlib import Path
from urllib.parse import unquote

from dotenv import load_dotenv
from flask import Flask, abort, render_template, url_for
from flask_frozen import Freezer
from config import PROJECT_ROOT

load_dotenv(dotenv_path="setup.env")
app = Flask(__name__)
app.config.from_pyfile('config.py')
freezer = Freezer(app)


def get_metadata_locations(path: Path) -> dict:
    output = {}
    metadata_paths = path.glob('**/meta_data.json')
    for p in metadata_paths:
        name = str(p.parent).split('\\')[-1]
        output[name] = p

    return output


metadata_dict = get_metadata_locations(Path(environ['PLOT_DIRECTORY']))
data_summary_dir = Path(environ['DATA_SUMMARY_DIRECTORY'])


def url_path(path_in: str, endpoint='static'):
    if path_in is not None:
        path_in = path_in.replace("\\", "/")
        path_in = "plots/" + path_in
    return url_for(endpoint, filename=path_in)


def get_team_nav(team):
    '''Produces name, url_for pairs for a teams sidebar.
       To be used with the sidebar templates.
    '''
    navigators = [("Back", url_for("index"))]
    navigators += [(team, url_for("team", team=team))]
    navigators += [("DIRE", None)]
    navigators += [("Drafts", url_for("serve_plots", team=team,
                    side="dire", plot="draft"))]
    navigators += [("Wards", url_for("serve_plots", team=team,
                    side="dire", plot="wards"))]
    navigators += [("Positioning", url_for("serve_plots", team=team,
                    side="dire", plot="positioning"))]
    navigators += [("Smokes", url_for("serve_plots", team=team,
                    side="dire", plot="smoke"))]
    navigators += [("Scans", url_for("serve_plots", team=team,
                    side="dire", plot="scan"))]

    navigators += [("RADIANT", None)]
    navigators += [("Drafts", url_for("serve_plots", team=team,
                    side="radiant", plot="draft"))]
    navigators += [("Wards", url_for("serve_plots", team=team,
                    side="radiant", plot="wards"))]
    navigators += [("Positioning", url_for("serve_plots", team=team,
                    side="radiant", plot="positioning"))]
    navigators += [("Smokes", url_for("serve_plots", team=team,
                    side="radiant", plot="smoke"))]
    navigators += [("Scans", url_for("serve_plots", team=team,
                    side="radiant", plot="scan"))]

    navigators += [(None, None)]
    navigators += [("Summary", url_for("summary", team=team))]

    return navigators


def get_nav_report():
    '''Produces navbar for reports with simple internal link.
    '''
    navigators = [(team, '#top')]
    navigators += [("DIRE", '#dire')]
    navigators += [("Drafts", '#dire_draft')]
    navigators += [("Wards", '#dire_wards')]
    navigators += [("Positioning", '#dire_pos')]
    navigators += [("Smokes", '#dire_smoke')]
    navigators += [("Scans", '#dire_scan')]

    navigators += [("RADIANT", '#radiant')]
    navigators += [("Drafts", '#radiant_draft')]
    navigators += [("Wards", '#radiant_wards')]
    navigators += [("Positioning", '#radiant_pos')]
    navigators += [("Smokes", '#radiant_smoke')]
    navigators += [("Scans", '#radiant_scan')]

    navigators += [(None, None)]
    navigators += [("Summary", '#summary')]

    return navigators


def get_team_summary(team, dataset='default') -> dict:
    '''Returns a dictionary of summary plots with url_for links'''
    with open(metadata_dict[team], 'r') as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)

        data = json_file[dataset]

        summary_dict = {}
        summary_dict['draft_summary'] = url_path(data["plot_draft_summary"])
        summary_dict['hero_picks'] = url_path(data["plot_hero_picks"])
        summary_dict['pair_picks'] = url_path(data["plot_pair_picks"])
        summary_dict['pick_context'] = url_path(data["plot_pick_context"])
        summary_dict['win_rate'] = url_path(data["plot_win_rate"])
        summary_dict['rune'] = url_path(data["plot_rune_control"])

        return summary_dict


def render_plot_template(team, side, plot, dataset='default'):
    if side not in ['dire', 'radiant']:
        abort(404)
    if plot not in ['draft', 'wards', 'positioning', 'smoke', 'scan']:
        abort(404)

    with open(metadata_dict[team], 'r') as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)

        data = json_file[dataset]
        navigators = get_team_nav(team)
        plots = {}
        if plot == 'draft':
            plots["drafts_link"] = "#{}_drafts".format(side)
            if data["plot_{}_drafts".format(side)] is not None:
                plots["plot_drafts"] = url_path(data["plot_{}_drafts".format(side)])

            return render_template('plots/draft.j2',
                                   plots=plots,
                                   navigators=navigators,
                                   team=team)

        if plot == 'wards':
            plots["ward_title"] = data['plot_ward_names']
            plots["ward_plots"] = ['plots/' + p.replace("\\", "/") for p in
                                   data['plot_ward_{}'.format(side)]]

            return render_template('plots/warding.j2',
                                   plots=plots,
                                   navigators=navigators,
                                   team=team)

        if plot == 'positioning':
            plots['pos_names'] = data['player_names']
            plots['pos_plots'] = ['plots/' + p.replace("\\", "/") for p in
                                  data['plot_pos_{}'.format(side)]]
            return render_template('plots/positioning.j2',
                                   plots=plots,
                                   navigators=navigators,
                                   team=team)

        if plot == 'smoke':
            if data["plot_smoke_{}".format(side)] is not None:
                plots["smoke"] = url_path(data["plot_smoke_{}".format(side)])
            return render_template('plots/smoke.j2',
                                   plots=plots,
                                   navigators=navigators,
                                   team=team)

        if plot == 'scan':
            if data["plot_scan_{}".format(side)] is not None:
                plots["scan"] = url_path(data["plot_scan_{}".format(side)])
            return render_template('plots/scan.j2',
                                   plots=plots,
                                   navigators=navigators,
                                   team=team)


@app.route("/")
def index():
    navigators = []
    for team in metadata_dict:
        url = url_for("team", team=team)
        navigators.append((team, url))
    navigators.append((None, None))
    navigators.append(("Summaries", url_for("data_summary")))
    return render_template('index.j2',
                           navigators=navigators)


@app.route("/<string:team>/")
def team(team, dataset='default'):
    team = unquote(team)
    if team not in metadata_dict:
        abort(404)
    with open(metadata_dict[team], 'r') as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)

        data = json_file[dataset]
        navigators = get_team_nav(team)
        dire = data['replays_dire']
        dire.sort(reverse=True)
        radiant = data['replays_radiant']
        radiant.sort(reverse=True)
        replay_list = list(zip_longest(dire, radiant))
        return render_template('replays.j2',
                               navigators=navigators,
                               replays=replay_list,
                               team=team,
                               winrates=data['stat_win_rate'])


@app.route("/<string:team>/summary/")
def summary(team):
    team = unquote(team)
    if team not in metadata_dict:
        abort(404)
    navigators = get_team_nav(team)
    summary = get_team_summary(team)
    return render_template('plots/summary.j2',
                           navigators=navigators,
                           summary=summary,
                           team=team)


@app.route("/data_summary.html")
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

    return render_template('plots/data_summary.j2',
                           navigators=navigators,
                           plots=plots)


@app.route("/<string:team>/<string:side>/<string:plot>.html")
def serve_plots(team, side, plot):
    team = unquote(team)
    if team not in metadata_dict:
        abort(404)
    return render_plot_template(team, side, plot)


@app.route("/<string:team>/report/")
def report(team, dataset='default'):
    team = unquote(team)
    if team not in metadata_dict:
        abort(404)

    navigators = get_nav_report()
    dire = {}
    radiant = {}
    with open(metadata_dict[team], 'r') as file:
        json_file = json_load(file)

        if dataset not in json_file:
            abort(404)
        data = json_file[dataset]

        # replays
        dire_replays = data['replays_dire']
        dire_replays.sort(reverse=True)
        radiant_replays = data['replays_radiant']
        radiant_replays.sort(reverse=True)
        replay_list = list(zip_longest(dire_replays, radiant_replays))
        # win rates
        winrates = data['stat_win_rate']

        # drafts
        dire["drafts_link"] = "#dire_drafts"
        if data["plot_dire_drafts"] is not None:
            dire["plot_drafts"] = url_path(data["plot_dire_drafts"])
        radiant["drafts_link"] = "#radiant_drafts"
        if data["plot_radiant_drafts"] is not None:
            radiant["plot_drafts"] = url_path(data["plot_radiant_drafts"])

        # wards
        dire["ward_title"] = data['plot_ward_names']
        dire["ward_plots"] = ['plots/' + p.replace("\\", "/") for p in
                              data['plot_ward_dire']]
        radiant["ward_title"] = data['plot_ward_names']
        radiant["ward_plots"] = ['plots/' + p.replace("\\", "/") for p in
                                 data['plot_ward_radiant']]

        # positioning
        dire['pos_names'] = data['player_names']
        dire['pos_plots'] = ['plots/' + p.replace("\\", "/") for p in
                             data['plot_pos_dire']]
        radiant['pos_names'] = data['player_names']
        radiant['pos_plots'] = ['plots/' + p.replace("\\", "/") for p in
                                data['plot_pos_radiant']]

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

    return render_template('plots/report.j2',
                           navigators=navigators,
                           replays=replay_list,
                           winrates=winrates,
                           dire=dire,
                           radiant=radiant,
                           summary=summary,
                           team=team)

@freezer.register_generator
def team():
    for p in metadata_dict.keys():
        yield {'team': p}

@freezer.register_generator
def report():
    for p in metadata_dict.keys():
        yield {'team': p}



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        print("Exporting to {}".format(PROJECT_ROOT))
        freezer.freeze()
        print("Exporting to {}".format(PROJECT_ROOT))
    app.run(port=8000)
