import pytest
from widgetastic.widget import View

from widgetastic_patternfly5 import Button

TESTING_PAGE_COMPONENT = "components/button"


@pytest.fixture
def variations_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-button-variant-examples']"
        any_button = Button()
        button1 = Button("Primary")

    return TestView(browser)


@pytest.fixture
def disabled_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-button-aria-disabled-examples']"
        button = Button("Primary aria disabled")

    return TestView(browser)


def test_button_click(variations_view):
    assert variations_view.any_button.is_displayed
    assert variations_view.button1.is_displayed


def test_disabled_button(disabled_view):
    assert disabled_view.button.is_displayed
    assert disabled_view.button.disabled
