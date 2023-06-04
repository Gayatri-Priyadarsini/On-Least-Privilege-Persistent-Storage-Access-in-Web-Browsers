# Sites taken from here:
# https://surfshark.com/whos-tracking-you

from marionette_driver import Wait
from marionette_driver.keys import Keys
from marionette_harness import (
        MarionetteTestCase,
        WindowManagerMixin,
        )

from tqdm import tqdm

urls = ['http://youtube.com','http://google.com']
#with open("curr_url.txt") as f:
#    urls = f.readlines()
#    urls = [i.strip() for i in urls]


class BaseNavigationTestCase(WindowManagerMixin, MarionetteTestCase):
    def setUp(self):
        super(BaseNavigationTestCase, self).setUp()

        if self.marionette.session_capabilities["platformName"] == "mac":
            self.mod_key = Keys.META
        else:
            self.mod_key = Keys.CONTROL

        # Always use a blank new tab for an empty history
        self.new_tab = self.open_tab()
        self.marionette.switch_to_window(self.new_tab)
        Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
            lambda _: self.history_length == 1,
            message="The newly opened tab doesn't have a browser history length of 1",
        )

    def tearDown(self):
        self.marionette.timeout.reset()

        self.close_all_tabs()

        super(BaseNavigationTestCase, self).tearDown()

    @property
    def history_length(self):
        return self.marionette.execute_script("return window.history.length;")

    @property
    def is_remote_tab(self):
        with self.marionette.using_context("chrome"):
            # TODO: DO NOT USE MOST RECENT WINDOW BUT CURRENT ONE
            return self.marionette.execute_script(
                """
              Components.utils.import("resource://gre/modules/AppConstants.jsm");

              let win = null;

              if (AppConstants.MOZ_APP_NAME == "fennec") {
                Components.utils.import("resource://gre/modules/Services.jsm");
                win = Services.wm.getMostRecentWindow("navigator:browser");
              } else {
                Components.utils.import("resource:///modules/BrowserWindowTracker.jsm");
                win = BrowserWindowTracker.getTopWindow();
              }

              let tabBrowser = null;

              // Fennec
              if (win.BrowserApp) {
                tabBrowser = win.BrowserApp.selectedBrowser;

              // Firefox
              } else if (win.gBrowser) {
                tabBrowser = win.gBrowser.selectedBrowser;

              } else {
                return null;
              }

              return tabBrowser.isRemoteBrowser;
            """
            )

    @property
    def ready_state(self):
        return self.marionette.execute_script(
            "return window.document.readyState;", sandbox=None
        )


class TestNavigate(BaseNavigationTestCase):
    def setUp(self):
        super(BaseNavigationTestCase, self).setUp()
        self.new_tab = self.open_tab()
        self.marionette.switch_to_window(self.new_tab)
        Wait(self.marionette, timeout=self.marionette.timeout.page_load).until(
            lambda _: self.history_length == 1,
            message="The newly opened tab doesn't have a browser history length of 1",
        )

    def test_get_current_url(self):
        self.marionette.timeout.page_load = 10
        pbar = tqdm(urls)
        for url in pbar:
            pbar.set_description(url)
            try:
                self.marionette.navigate(url)
            except Exception:
                continue
        self.marionette.timeout.reset()
        # self.assertEqual(self.test_page_remote, self.marionette.get_url())
