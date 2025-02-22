import pytest
from widgetastic.widget import Text, View

from widgetastic_patternfly5 import InputSlider, Slider

TESTING_PAGE_COMPONENT = "components/slider"
TEST_DATA = {
    "discrete": {
        "steps": [-25, -15, -5, 5, 15, 25, 35, 45, 55, 65, 75],
        "labels": [-25, 75],
        "current_value": 50,
    },
    "value": {"steps": [0, 25, 50, 75, 100], "labels": ["0%", "50%", "100%"], "current_value": 50},
}


@pytest.fixture(scope="module")
def view(browser):
    class TestView(View):
        # discrete slider
        discrete_value = Text(locator="(.//h3[contains(text(), 'Slider value is')])[4]")
        discrete = Slider(locator="(.//div[@id='ws-react-c-slider-discrete']/child::div)[4]")
        # value slider
        value = InputSlider(locator="(.//div[@id='ws-react-c-slider-value-input']/child::div)[2]")
        # disabled slider
        disabled_slider = Slider(locator=".//div[@id='ws-react-c-slider-disabled']")

    return TestView(browser)


@pytest.fixture(params=["discrete", "value"])
def slider_type(view, request):
    return request.param


@pytest.fixture
def slider(view, slider_type):
    return getattr(view, slider_type)


def test_slider_is_displayed(slider):
    assert slider.is_displayed


def test_slider_is_enabled(view):
    assert view.discrete.is_enabled
    assert not view.disabled_slider.is_enabled


def test_slider_label(slider, slider_type):
    assert slider.labels == TEST_DATA[slider_type]["labels"]


def test_slider_text(slider, slider_type):
    assert slider.text == TEST_DATA[slider_type]["current_value"]


def test_slider_steps(slider, slider_type):
    assert slider.steps() == TEST_DATA[slider_type]["steps"]


def test_slider_range(slider, slider_type):
    steps = TEST_DATA[slider_type]["steps"]
    assert slider.min == min(steps)
    assert slider.max == max(steps)
    assert slider.step == steps[1] - steps[0]


def test_slider_fill_read(slider, slider_type):
    value = slider.steps()[-2]
    slider.fill(value)
    currect_value = slider.read()
    assert currect_value == value
