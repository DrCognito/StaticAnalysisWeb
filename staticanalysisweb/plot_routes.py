from flask import Flask, abort, render_template, url_for, Blueprint, send_file
from json import load as json_load

# from .app import current_dir, update_meta_dict, metadata_dict, get_team_nav
import staticanalysisweb.app as app
import staticanalysisweb.plot_class as pc

plot_routes = Blueprint("plots", __name__)


@plot_routes.route("/<string:team>/<string:dataset>/drafts<string:postfix>.html")
@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/draft.html")
def draft(team, dataset, side=None, postfix=None):
    app.update_meta_dict()
    draft = pc.Drafts(app.current_dir / app.metadata_dict[team]["path"], dataset)

    key = "plot"
    if side is not None:
        key += f"_{side}"
    key += "_drafts"
    if postfix is not None:
        key += postfix

    navigators = app.get_team_nav(team, dataset)
    try:
        plots = draft.plot_vars(key)
    except (ValueError, KeyError):
        message = f"No data for {team} on {side} with data {dataset}+{postfix}"
        return render_template("plots/plot_404.j2",
                                navigators=navigators,
                                team=team,
                                plot_type="No Drafts",
                                message=message)
        # abort(404)
    return render_template(
        "plots/draft.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.draft",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        postfix=postfix,
        active=side
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/wards.html")
def wards(team, dataset, side):
    app.update_meta_dict()
    wards = pc.Wards(app.current_dir / app.metadata_dict[team]["path"], dataset)
    n_replays = wards.n_replays(side)
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = wards.plot_vars(side)
    except ValueError:
        abort(404)

    return render_template(
        "plots/warding.j2",
        plots=plots,
        navigators=navigators,
        dataset_list=app.metadata_dict[team]["sets"],
        provider="plots.wards",
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/wards_separate.html")
def wards_separate(team, dataset, side):
    app.update_meta_dict()
    wards_separate = pc.WardsSeparate(
        app.current_dir / app.metadata_dict[team]["path"], dataset
    )
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = wards_separate.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = wards_separate.n_replays(side)
    return render_template(
        "plots/warding_seperate.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.wards_separate",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/pregame_positioning.html")
def pregame_positioning(team, dataset, side):
    app.update_meta_dict()
    pregame_positioning = pc.PregamePositioning(
        app.current_dir / app.metadata_dict[team]["path"], dataset
    )
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = pregame_positioning.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = pregame_positioning.n_replays(side)
    return render_template(
        "plots/pregame_positioning.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.pregame_positioning",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/tormentor_routes.html")
def tormentor_routes(team, dataset, side):
    app.update_meta_dict()
    tormentor_routes = pc.TormentorPositioning(
        app.current_dir / app.metadata_dict[team]["path"], dataset
    )
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = tormentor_routes.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = tormentor_routes.n_replays(side)
    return render_template(
        "plots/tormentors.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.tormentor_routes",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/stacks.html")
def stacks_plot(team, dataset, side):
    app.update_meta_dict()
    stacks = pc.Stacks(
        app.current_dir / app.metadata_dict[team]["path"], dataset
    )
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = stacks.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = stacks.n_replays(side)
    return render_template(
        "plots/stacks.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.stacks_plot",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/positioning.html")
def positioning(team, dataset, side):
    app.update_meta_dict()
    positioning = pc.Positioning(
        app.current_dir / app.metadata_dict[team]["path"], dataset
    )
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = positioning.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = positioning.n_replays(side)
    return render_template(
        "plots/positioning.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.positioning",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/smoke.html")
def smoke(team, dataset, side):
    app.update_meta_dict()
    smoke = pc.Smoke(app.current_dir / app.metadata_dict[team]["path"], dataset)
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = smoke.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = smoke.n_replays(side)
    return render_template(
        "plots/smoke.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.smoke",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/scan.html")
def scan(team, dataset, side):
    app.update_meta_dict()
    scan = pc.Scan(app.current_dir / app.metadata_dict[team]["path"], dataset)
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = scan.plot_vars(side)
    except ValueError:
        abort(404)
    n_replays = scan.n_replays(side)
    return render_template(
        "plots/scan.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.scan",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/runes.html")
def rune(team, dataset, side):
    app.update_meta_dict()
    rune = pc.Rune(app.current_dir / app.metadata_dict[team]["path"], dataset)
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = rune.plot_vars(side)
    except ValueError:
        return render_template("404.j2")
    n_replays = rune.n_replays(side)
    return render_template(
        "plots/rune.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.rune",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
        active=side,
        replays=n_replays
    )


@plot_routes.route("/<string:team>/<string:dataset>/report.pdf")
def pdf_report(team, dataset):
    app.update_meta_dict()

    route = pc.PDFReport(app.current_dir / app.metadata_dict[team]["path"], dataset)
    report = route.plot_vars()
    if not report:
        return render_template("404.j2")
    if not report.exists():
        return render_template("404.j2")

    return send_file(
        report,
        download_name=report.name,
        mimetype='application/pdf')


@plot_routes.route("/<string:team>/<string:dataset>/mini_report.pdf")
def pdf_mini_report(team, dataset):
    app.update_meta_dict()

    route = pc.PDFMiniReport(app.current_dir / app.metadata_dict[team]["path"], dataset)
    report = route.plot_vars()
    if not report:
        return render_template("404.j2")
    if not report.exists():
        return render_template("404.j2")

    return send_file(
        report,
        download_name=report.name,
        mimetype='application/pdf')