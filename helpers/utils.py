import os
import shutil

class Utils:

    def __init__(self, app):
        self.app = app
        self.step = self.app.step
        self.wd = self.app.wd

    BASEDIR = os.path.join(os.getcwd(), "screenshots/")

    def takeScreenshot(self):
        shutil.rmtree(self.BASEDIR)
        os.makedirs(self.BASEDIR)
        self.wd.save_screenshot(self.BASEDIR + "test.png")

    def deleteAllScreenshots(self):
        shutil.rmtree(self.BASEDIR)
        os.makedirs(self.BASEDIR)

    def getPathToScreenshot(self):
        return self.BASEDIR + "test.png"
