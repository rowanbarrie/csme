from typer.testing import CliRunner

from csme.cli import app

runner = CliRunner()


def test_render(mocker):
    fake_output_filename = "build/foo.png"
    mocker.patch('csme.cli.service.render', return_value=fake_output_filename)

    result = runner.invoke(app, ["render", "data/arabic_1.json"])
    assert result.exit_code == 0

    assert f"Output filepath: {fake_output_filename}" in result.stdout


def test_render_no_states(mocker):
    fake_output_filename = "build/foo.png"
    mocker.patch('csme.cli.service.render_no_states', return_value=fake_output_filename)

    result = runner.invoke(app, ["render-no-states", "data/arabic_1.json"])
    assert result.exit_code == 0

    assert f"Output filepath: {fake_output_filename}" in result.stdout
