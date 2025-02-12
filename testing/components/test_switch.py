import pytest
from widgetastic.widget import View

from widgetastic_patternfly5 import Switch, SwitchDisabled

TESTING_PAGE_URL = "https://patternfly-react-main.surge.sh/components/switch"


@pytest.fixture
def view(browser):
    class TestView(View):
        switch = Switch(locator='.//label[@for="simple-switch"]')
        no_label_switch = Switch(locator='.//label[@for="no-label-switch-on"]')
        disabled_switch_on = Switch(locator='.//label[@for="disabled-switch-on"]')
        disabled_switch_off = Switch(locator='.//label[@for="disabled-switch-off"]')
        disabled_no_label_switch_on = Switch(locator='.//label[@for="disabled-no-label-switch-on"]')
        disabled_no_label_switch_off = Switch(
            locator='.//label[@for="disabled-no-label-switch-off"]'
        )

    return TestView(browser)


def test_switch_is_displayed(view):
    assert view.switch.is_displayed
    assert view.no_label_switch.is_displayed
    assert view.disabled_switch_on.is_displayed
    assert view.disabled_switch_off.is_displayed
    assert view.disabled_no_label_switch_on.is_displayed
    assert view.disabled_no_label_switch_off.is_displayed


def test_switch_is_enabled(view):
    assert view.switch.is_enabled
    assert view.no_label_switch.is_enabled
    assert not view.disabled_switch_on.is_enabled
    assert not view.disabled_switch_off.is_enabled
    assert not view.disabled_no_label_switch_on.is_enabled
    assert not view.disabled_no_label_switch_off.is_enabled


def test_switch_label(view):
    assert view.switch.label == "Message when on"
    assert view.no_label_switch.label is None
    assert view.disabled_switch_on.label == "Message when on"
    assert view.disabled_switch_off.label == "Message when off"
    assert view.disabled_no_label_switch_on.label is None
    assert view.disabled_no_label_switch_off.label is None


def test_switch_selected(view):
    assert view.switch.read()
    assert view.no_label_switch.read()
    assert view.disabled_switch_on.read()
    assert not view.disabled_switch_off.read()
    assert view.disabled_no_label_switch_on.read()
    assert not view.disabled_no_label_switch_off.read()


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_switch_fill(view):
    view.browser.refresh()
    assert view.switch.selected
    assert view.switch.label == "Message when on"
    assert not view.switch.fill(True)
    assert view.switch.selected
    assert view.switch.label == "Message when on"
    assert view.switch.fill(False)
    assert not view.switch.selected
    assert view.switch.label == "Message when off"
    assert view.switch.fill(True)
    assert view.switch.selected
    assert view.switch.label == "Message when on"


def test_switch_fill_disabled(view):
    for disabled_switch in (
        view.disabled_switch_on,
        view.disabled_switch_off,
        view.disabled_no_label_switch_on,
        view.disabled_no_label_switch_off,
    ):
        with pytest.raises(SwitchDisabled):
            disabled_switch.fill(True)
