import pytest
from widgetastic.widget import Text

from widgetastic_patternfly5 import Button
from widgetastic_patternfly5.components.modal import Modal, ModalItemNotFound

TESTING_PAGE_COMPONENT = "components/modal"


@pytest.fixture()
def modal(browser):
    show_modal = Button(browser, "Show basic modal")
    show_modal.click()
    modal = Modal(browser)
    yield modal
    if modal.is_displayed:
        modal.close()


class CustomModal(Modal):
    """Model use as view and enhance with widgets"""

    custom_body = Text(".//div[contains(@class, '-c-modal-box__body')]")


def test_title(modal):
    assert modal.title


def test_body(modal):
    body = modal.body
    assert body.text.startswith("Lorem")


def test_close(modal):
    modal.close()
    assert not modal.is_displayed


def test_footer_items(modal):
    items = modal.footer_items
    assert len(items) == 2
    assert "Cancel" in items
    assert "Confirm" in items


def test_footer_item(modal):
    item = modal.footer_item("Confirm")
    assert item.text == "Confirm"
    item.click()
    assert not modal.is_displayed


def test_footer_item_invalid(modal):
    items = modal.footer_items
    with pytest.raises(ModalItemNotFound) as e:
        modal.footer_item("INVALID")
    assert str(e.value) == f"Item INVALID not found. Available items: {items}"


def test_modal_as_view(browser, modal):
    view = CustomModal(browser)
    assert view.is_displayed
    assert view.custom_body.text == modal.body.text
