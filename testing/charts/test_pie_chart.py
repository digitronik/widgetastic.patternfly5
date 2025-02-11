from collections import namedtuple
from time import sleep

import pytest

from widgetastic_patternfly5 import DataPoint, PieChart

TESTING_PAGE_URL = "https://patternfly-react-main.surge.sh/charts/pie-chart"

Legend = namedtuple("Legend", ["label", "value"])
DATA = {"Cats": 35, "Dogs": 55, "Birds": 10}
LEGENDS = [Legend(label, value) for label, value in DATA.items()]
DATA_POINTS = [DataPoint(label, value) for label, value in DATA.items()]


@pytest.fixture(
    params=[
        {
            "id": "ws-react-c-pie-chart-multi-color-ordered-with-bottom-aligned-legend",
            "anchor": "#multi-color-ordered-with-bottom-aligned-legend",
        },
        {
            "id": "ws-react-c-pie-chart-basic-with-right-aligned-legend",
            "anchor": "#basic-with-right-aligned-legend",
        },
    ],
    ids=["bottom-aligned", "right-aligned"],
)
def chart(browser, request):
    sleep(3)  # Stabilized graph data on testing page; specially for firefox.
    # Firefox fails the test if the chart is not fully visible therefore we click here on anchor
    # in order to properly scroll down
    anchor = browser.element(f".//a[@href='{request.param['anchor']}']")
    browser.click(anchor)
    return PieChart(browser, id=request.param["id"])


def test_pie_chart(chart):
    """Test PieChart widget."""
    assert chart.is_displayed

    for leg, expected_leg in zip(chart.legends, LEGENDS):
        assert leg.label == expected_leg.label
        assert leg.value == expected_leg.value
        assert chart.data == DATA_POINTS

    assert "Birds" in chart.legend_names

    # get data point and check values
    birds_legend = chart.get_legend("Birds")
    birds_data = chart.get_data_point("Birds")

    assert birds_data.label == birds_legend.label
    assert birds_data.value == birds_legend.value
    assert birds_data.color == birds_legend.color

    # read graph
    assert chart.read() == DATA
