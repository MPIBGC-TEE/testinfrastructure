import unittest


from testinfrastructure.InDirTest import InDirTest
import matplotlib.pyplot as plt
from pathlib import Path


class TestInDirTest(unittest.TestCase):
    def test_test_file_in_dir(self):
        # - Create an InDirTestInstance
        #   and test suite
        # - run the suite and check that
        #   it created a 'tmp' dir and a test specific
        #   subdirectory where we find the output.
        #
        # Note:
        # We could do this programmatically 
        # with the class and method name defined in a string 
        # to avoid duplication but this would look different from
        # a typical use case. 
        # Within this test method we therefore allow a
        # bit of duplication since it is easy to see 
        # the connection
        class TestWriteFile(InDirTest):
            def test_write_file(self):
                fig=plt.figure()
                fig.savefig('test.pdf')

        test_class_name = 'TestWriteFile'
        test_func_name = 'test_write_file'
        test_file_name = 'test.pdf'
        suite = unittest.TestSuite()
        test_instance=TestWriteFile(test_func_name)
        suite.addTest(test_instance)
        r = unittest.TextTestRunner()
        res = r.run(suite)
        p = Path('.')
        sub_dir_name =  __name__+ '.' + test_class_name + '.' + test_func_name
        target_path=p.joinpath('tmp', sub_dir_name, test_file_name)
        print(target_path)
        self.assertTrue(target_path.exists())

        #print(InDirTest.tmpDirPath())
        #print(test_instance.testDirPath())

