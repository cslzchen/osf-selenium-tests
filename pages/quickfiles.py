import urllib
import settings


from selenium.webdriver.common.by import By
from pages.base import (
    OSFBasePage,
    Locator,
    GroupLocator
)

class QuickfilesPage(OSFBasePage):

    # Locators
    quickfiles_heading = Locator(By.CSS_SELECTOR, '.active.NavbarList__item__title--active.ember-view')
    upload_button = Locator(By.CSS_SELECTOR, '.btn.text-success.dz-upload-button.dz-clickable')
    download_button = Locator(By.LINK_TEXT, 'Download as zip')
    identity = quickfiles_heading

    def __init__(self, driver, verify=False, user_id=''):
        super(self.__class__, self).__init__(driver, verify)
        quickfiles_url = '{}/quickfiles/'.format(user_id)
        self.user_id = user_id
        self.url = urllib.parse.urljoin(settings.OSF_HOME, quickfiles_url)
