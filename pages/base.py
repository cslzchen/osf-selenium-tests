import settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from pages.exceptions import HttpError, PageException


class BaseElement(object):
    default_timeout = settings.TIMEOUT

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def verify_element(self):
        raise NotImplementedError

    def __getattr__(self, element):
        """
        This method is adapted from code provided on seleniumframework.com
        """
        timeout = self.default_timeout

        if element in self.locators:
            if len(self.locators[element]) == 3:
                timeout = self.locators[element][2]
            location = (self.locators[element][0], self.locators[element][1])

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} not present on page'.format(element))

            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(location)
                )
            except(TimeoutException, StaleElementReferenceException):
                raise ValueError('Element {} not visible before timeout'.format(element))

            if 'link' in element:
                try:
                    WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable(location)
                    )
                except(TimeoutException, StaleElementReferenceException):
                    raise ValueError('Element {} on page but not clickable'.format(element))

            return self.find_element(*location)
        else:
            raise ValueError('Cannot find element {}'.format(element))


class BasePage(BaseElement):
    url = None

    def goto(self):
        self.driver.get(self.url)

    def reload(self):
        self.driver.refresh()


class OSFBasePage(BasePage):
    url = settings.OSF_HOME

    def __init__(self, driver):
        super(OSFBasePage, self).__init__(driver)

        # Verify the page is what you expect it to be.
        driver.get(self.url)

        if not self._verify_page():
            url = driver.current_url

            # If we've got an error message here, grab it
            error_heading = self.driver.find_elements(
                By.CSS_SELECTOR,
                'h2#error'
            )

            if error_heading:
                h = error_heading[0]
                raise HttpError(
                    driver=self.driver,
                    code=h.get_attribute('data-http-status-code'),
                )

            raise PageException('Unexpected page structure: `{}`'.format(
                url
            ))

        self.navbar = self.Navbar(driver)

    def _verify_page(self):
        return True

    def is_logged_in(self):
        return self.navbar.is_logged_in()

    class Navbar(BaseElement):

        locators = {
            'home': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '"]'),
            'preprint': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/preprints/"]'),
            'registries': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/registries/"]'),
            'meetings': (By.XPATH, '//nav[@id="navbarScope"]/div/div[@class="navbar-header"]/div[@class="dropdown"]/ul[@role="menu"]/li/a[@href="' + settings.OSF_HOME + '/meetings/"]'),
            'my_project': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="' + settings.OSF_HOME + '/myprojects/"]'),
            'search': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="' + settings.OSF_HOME + '/search/"]'),
            'support': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="/support/"]'),
            'donate': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li/a[@href="https://cos.io/donate"]'),
            'user_dropdown': (By.CSS_SELECTOR, '#secondary-navigation > ul > li:nth-child(5) > button'),
            'user_dropdown_profile': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="/logout/"]'),
            'user_dropdown_support': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="' + settings.OSF_HOME + '/support/"]'),
            'user_dropdown_settings': (By.XPATH, '//div[@id="secondary-navigation"]/ul/li[@class="dropdown"]/ul/li/a[@href="/settings/"]'),
            'sign_up_button': (By.LINK_TEXT, 'Sign Up'),
            'sign_in_button': (By.LINK_TEXT, 'Sign In'),
            'logout_link': (By.CSS_SELECTOR, '#secondary-navigation > ul > li.dropdown.open > ul > li:nth-child(4) > a')
        }

        def _verify_element(self):
            return self.driver.find_element(
                By.CSS_SELECTOR,
                '#navbarScope > div > div > div.service-home > a > span.current-service > strong'
            ).text == 'HOME'

        def is_logged_in(self):
            try:
                if self.sign_in_button:
                    return False
            except ValueError:
                return True
