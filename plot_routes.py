from flask import Flask, abort, render_template, url_for, Blueprint
from json import load as json_load

# from .app import current_dir, update_meta_dict, metadata_dict, get_team_nav
import app
import plot_class as pc

plot_routes = Blueprint("plots", __name__)


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/draft.html")
def draft(team, dataset, side):
    app.update_meta_dict()
    draft = pc.Drafts(app.current_dir / app.metadata_dict[team]["path"], dataset)
    navigators = app.get_team_nav(team, dataset)
    try:
        plots = draft.plot_vars(side)
    except ValueError:
        abort(404)
    return render_template(
        "plots/draft.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.draft",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
    )


@plot_routes.route("/<string:team>/<string:dataset>/<string:side>/wards.html")
def wards(team, dataset, side):
    app.update_meta_dict()
    wards = pc.Wards(app.current_dir / app.metadata_dict[team]["path"], dataset)
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

    return render_template(
        "plots/warding_seperate.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.wards_separate",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
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

    return render_template(
        "plots/positioning.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.positioning",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
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

    return render_template(
        "plots/smoke.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.smoke",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
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

    return render_template(
        "plots/scan.j2",
        plots=plots,
        navigators=navigators,
        provider="plots.scan",
        dataset_list=app.metadata_dict[team]["sets"],
        side=side,
        team=team,
    )
