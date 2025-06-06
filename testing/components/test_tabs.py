import pytest
from widgetastic.widget import Text, View

from widgetastic_patternfly5 import Tab

TESTING_PAGE_COMPONENT = "components/tabs"


class TabsTestView(View):
    @View.nested
    class primary(View):
        ROOT = ".//div[@id='ws-react-c-tabs-default-tabs']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Users"
            content = Text(".")

        @View.nested
        class tab2(Tab):
            TAB_NAME = "Containers"
            content = Text(".")

    @View.nested
    class secondary(View):
        ROOT = ".//div[@id='ws-react-c-tabs-secondary-tabs']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Users"

            @View.nested
            class secondary1(Tab):
                TAB_NAME = "Secondary tab item 1"
                content = Text(".")

            @View.nested
            class secondary2(Tab):
                TAB_NAME = "Secondary tab item 2"
                content = Text(".")

    @View.nested
    class separate(View):
        ROOT = ".//div[@id='ws-react-c-tabs-with-separate-content']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Tab item 1"
            content = Text(".")

        @View.nested
        class tab2(Tab):
            TAB_NAME = "Tab item 2"
            content = Text(".")

        @View.nested
        class tab3(Tab):
            TAB_NAME = "Tab item 3"
            content = Text(".")

    @View.nested
    class sub(View):
        ROOT = ".//div[@id='ws-react-c-tabs-subtabs']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Users"

            @View.nested
            class sub1(Tab):
                TAB_NAME = "Subtab item 1"
                content = Text(".")

            @View.nested
            class sub2(Tab):
                TAB_NAME = "Subtab item 2"
                content = Text(".")


def test_primary_tabs(browser):
    view = TabsTestView(browser)
    assert view.primary.tab1.is_displayed
    view.primary.tab1.select()
    assert view.primary.tab1.tab_name == view.primary.tab1.TAB_NAME
    assert view.primary.tab2.is_displayed
    assert view.primary.tab1.is_active()

    view.primary.tab2.select()
    view.primary.tab1.child_widget_accessed(view.primary.tab1)
    assert view.primary.tab1.is_active()

    assert not view.primary.tab2.is_active()
    assert view.primary.tab1.content.text == "Users"
    view.primary.tab2.select()

    assert not view.primary.tab1.is_active()
    assert view.primary.tab2.is_active()
    assert view.primary.tab2.content.text == "Containers"


@pytest.mark.skip_if_pf6
def test_secondary_tabs(browser):
    """In PF6, the secondary tab widget does not exactly match the PF5 demo widget.
    Therefore, we will be skipping this test for PF6.
    """
    view = TabsTestView(browser)
    assert view.secondary.tab1.is_displayed
    view.primary.tab1.select()
    assert view.secondary.tab1.is_active()
    assert view.secondary.tab1.secondary1.is_displayed
    assert view.secondary.tab1.secondary2.is_displayed
    assert not view.secondary.tab1.secondary1.is_active()
    assert not view.secondary.tab1.secondary2.is_active()
    assert view.secondary.tab1.secondary1.content.text == "Secondary tab item 1 item section"
    view.secondary.tab1.secondary2.select()
    assert not view.secondary.tab1.secondary1.is_active()
    assert view.secondary.tab1.secondary2.is_active()
    assert view.secondary.tab1.secondary2.content.text == "Secondary tab item 2 section"


@pytest.mark.skip_if_pf5
def test_sub_tabs(browser):
    """In PF5, the sub tab widget does not exactly match the PF6 demo widget.
    Therefore, we will be skipping this test for PF5.
    """
    view = TabsTestView(browser)
    assert view.sub.tab1.is_displayed
    view.primary.tab1.select()
    assert view.sub.tab1.is_active()
    assert view.sub.tab1.sub1.is_displayed
    assert view.sub.tab1.sub2.is_displayed
    assert not view.sub.tab1.sub1.is_active()
    assert not view.sub.tab1.sub2.is_active()
    assert view.sub.tab1.sub1.content.text == "Subtab item 1 item section"
    view.sub.tab1.sub2.select()
    assert not view.sub.tab1.sub1.is_active()
    assert view.sub.tab1.sub2.is_active()
    assert view.sub.tab1.sub2.content.text == "Subtab item 2 section"


def test_auto_selected(browser):
    view = TabsTestView(browser)
    view.primary.tab1.select()
    assert not view.primary.tab2.is_active()
    view.primary.tab2.content.read()
    assert view.primary.tab2.is_active()


def test_separate_content_tabs(browser):
    view = TabsTestView(browser)
    view.separate.tab1.select()
    assert view.separate.tab2.is_displayed
    assert view.separate.tab1.is_active()
    assert not view.separate.tab2.is_active()
    assert view.separate.tab1.content.text == "Tab 1 section"
    view.separate.tab2.select()
    assert not view.separate.tab1.is_active()
    assert view.separate.tab2.is_active()
    assert view.separate.tab2.content.text == "Tab 2 section"
