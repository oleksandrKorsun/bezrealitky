import os

class Utils:

    def __init__(self, app):
        self.app = app
        self.step = self.app.step
        self.wd = self.app.wd

    BASEDIR = os.path.join(os.path.abspath(os.pardir), "screenshots")

    def takeScreenshot(self):
        self.wd.save_screenshot(self.BASEDIR + "test.png")

    def deleteAllScreenshots(self):
        import shutil
        shutil.rmtree(self.BASEDIR)
        os.makedirs(self.BASEDIR)

    def getPathToScreenshot(self):
        return self.BASEDIR + "test.png"
