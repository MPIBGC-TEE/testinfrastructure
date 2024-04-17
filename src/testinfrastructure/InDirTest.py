# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import pathlib
import inspect
import shutil
import os


class InDirTest(unittest.TestCase):
    #def __init__(self, args):
    #    st = inspect.stack()
    #    # self.caller_dir_path = pathlib.Path(
    #    #     os.path.dirname(os.path.abspath(inspect.getfile(st[-1].frame)))
    #    # )
    #    super().__init__(args)

    def myDirPath():
        return pathlib.Path.cwd()

    def tmpDirPath():
        return __class__.myDirPath().joinpath("tmp")

    def run(self, *args):
        #testDirPath = __class__.tmpDirPath().joinpath(self.id())
        cls=self.__class__
        testDirPath = cls.tmpDirPath().joinpath(f"{cls.__module__}.{cls.__name__}.{self._testMethodName}")
        testDirName = testDirPath.as_posix()

        self.oldDirName = os.getcwd()
        __class__.rootDir = pathlib.Path(self.oldDirName).parent.parent
        if testDirPath.exists():
            shutil.rmtree(testDirPath)
        testDirPath.mkdir(parents=True)
        print("self.id()",self.id())
        print("testDirName",testDirName)

        os.chdir(testDirName)

        try:
            super().run(*args)
        finally:
            os.chdir(self.oldDirName)
