import unittest

from testinfrastructure.InDirTest import InDirTest
import matplotlib.pyplot as plt
from pathlib import Path


class TestInDirTest(unittest.TestCase):
    def test_file_in_dir(self):
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
        self.assertTrue(target_path.exists())

    def test_files_in_subtest_dirs(self):
        class TestWriteSubTestFiles(InDirTest):
            def test_write_subtest_files(self):
                names = ["1","2"]
                for name in names:
                    with self.subTest(name=name):
                        fig=plt.figure()
                        print("name: ", name)
                        fig.savefig(f'test{name}.pdf')

        test_class_name = 'TestWriteSubTestFiles'
        test_func_name = 'test_write_subtest_files'
        names = ["1","2"]
        test_file_names = [f'test{name}.pdf' for name in names]
        suite = unittest.TestSuite()
        test_instance=TestWriteSubTestFiles(test_func_name)
        suite.addTest(test_instance)
        r = unittest.TextTestRunner()
        res = r.run(suite)
        p = Path('.')
        sub_dir_name =  __name__+ '.' + test_class_name + '.' + test_func_name
        
        for test_file_name in test_file_names:
            tp= p.joinpath('tmp', sub_dir_name, test_file_name)
            print("tp ",tp)
            self.assertTrue(tp.exists())



