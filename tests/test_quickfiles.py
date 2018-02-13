import pytest

from api import osf_api as osf
from tests.base import SeleniumTest
from pages.dashboard import DashboardPage
from pages.quickfiles import QuickfilesPage
from pages.base import login

class TestQuickfilesPage(SeleniumTest):

    #TODO: Fix/update when redone quickfiles page comes out
    def upload_python_file(self):
        quickfile = open('/Users/laurenrevere/Code/OSF-Integration-Tests/pages/quickfiles.py')
        osf.upload_quickfile(self.session, quickfile)

    def setup_method(self, method):
        user = osf.current_user(self.session)
        self.quickfiles_page = QuickfilesPage(self.driver, False, user.id)
        self.quickfiles_page.goto()

    def test_your_quickfiles(self):
        login(self.quickfiles_page)
        self.quickfiles_page.upload_button



