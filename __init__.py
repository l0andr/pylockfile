"""
Project: pylockfile
Description: pylockfile it's is set of python classes implemented 'pid' and 'lock' files concepts
Copyright 2023, Andrey Loginov
"""

__author__ = "Andrey Loginov"
__copyright__ = "Copyright 2023, Andrey Loginov"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "andreyloginovmob@gmail.com"
__status__ = "Development"
import sys
if sys.version_info[:2] < (3, 6):
    raise RuntimeError("pylockfile package requres Python 3.6+")