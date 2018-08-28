import pytest
from selenium.webdriver.common.keys import Keys

import markers
from pages.search import SearchPage

@pytest.fixture()
def search_page(driver):
    search_page = SearchPage(driver)
    search_page.goto()
    return search_page


class TestSearchPage:

    @markers.smoke_test
    @markers.core_functionality
    def test_search_results_exist(self, driver, search_page):
        search_page.search_bar.send_keys('*')
        search_page.search_bar.send_keys(Keys.ENTER)
        assert search_page.search_results
