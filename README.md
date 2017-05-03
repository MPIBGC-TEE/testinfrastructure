# test_infrastructure
Common test infrastructure for some of our python packages.
Unit tests usually do not do I/O but sometimes we need to check a written file.
The InDirTest class provides the infrastructure to avoid interactions between tests via 
the file system that would endanger their independence. 
 
 
