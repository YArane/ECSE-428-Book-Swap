#Unit Tests#

Unit tests will be conducted using the [unittest](https|//docs.python.org/2/library/unittest.html#module-unittest) framework provided in python 2.1

##Test Case Reference##
Method | Checks That
------ | -----------
assertEqual(a, b)         | a == b
assertNotEqual(a, b)      | a != b
assertTrue(x)             | bool(x) is True
assertFalse(x)            | bool(x) is False
assertIs(a, b)            | a is b
assertIsNot(a, b)         | a is not b
assertIsNone(x)           | x is None
assertIsNotNone(x)        | x is not None
assertIn(a, b)            | a in b
assertNotIn(a, b)         | a not in b
assertIsInstance(a, b)    | isinstance(a, b)
assertNotIsInstance(a, b) | not isinstance(a, b)

##Test Suite Style##
```python
import unittest
from path_from_root_directory.module_to_be_tested import method_to_be_tested
    
class TestRequirement(unittest.TestCase):
    
    def setUp(self):
        # setup objects, variables
    
    def tearDown(self):
        # deallocate / dereference any unused objects
    
    def test_module(self):
        # test cases here
    
if __name__ == '__main__':
    unittest.main()
```
##Testing Conventions##

- All **story related**, **public members** must be accompanied by a *complete* testing suite
- All unit tests should be in the *unit_tests/* subdirectory

##*Todo:*##
Test runner module
    `unittest.run()`
