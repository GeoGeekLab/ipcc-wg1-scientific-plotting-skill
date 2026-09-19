import matplotlib.pyplot as plt

from ipcc_sciplot.fidelity import audit_figure
from ipcc_sciplot.style import publication_context
from ipcc_sciplot.tokens import scenario_style


def test_scenario_colour_audit_passes():
    with publication_context():
        fig, ax = plt.subplots()
        token = scenario_style("SSP2-4.5", profile="ar6-report")
        ax.plot([0, 1], [0, 1], label="SSP2-4.5", color=token.color)
        assert audit_figure(fig, profile="ar6-report") == []
        plt.close(fig)


def test_scenario_colour_audit_detects_default_cycle():
    with publication_context():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="SSP2-4.5")
        issues = audit_figure(fig, profile="ar6-report")
        plt.close(fig)
    assert any("expected" in issue for issue in issues)
