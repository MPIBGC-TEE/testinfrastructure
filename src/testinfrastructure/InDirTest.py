# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import pathlib
import inspect
import shutil
import os

class InDirTest(unittest.TestCase):
    
    def myDirPath():
        return pathlib.Path.cwd()

    def tmpDirPath():
        return __class__.myDirPath().joinpath("tmp")

    def get_testDirPath(self):
        cls=self.__class__
        return cls.tmpDirPath().joinpath(f"{cls.__module__}.{cls.__name__}.{self._testMethodName}")

    def run(self, *args):
        cls=self.__class__
        testDirPath=self.get_testDirPath()
        testDirName = testDirPath.as_posix()
        print("testDirName",testDirName)

        self.oldDirName = os.getcwd()
        __class__.rootDir = pathlib.Path(self.oldDirName).parent.parent
        if testDirPath.exists():
            shutil.rmtree(testDirPath)
        testDirPath.mkdir(parents=True)

        os.chdir(testDirName)

        try:
            super().run(*args)
        finally:
            os.chdir(self.oldDirName)
