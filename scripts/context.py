# These are the imports we're going to use in all scripts.
import sys
import os
import matplotlib.pyplot as plt
# Use relative paths so this works on any computer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utility
# Use relative paths so this works on any computer
import platform
if platform.processor() == 'arm':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ext/gpytoolbox/build-arm')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ext/gpytoolbox/build')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ext/gpytoolbox/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ext/gpytoolbox/build-linux')))
import gpytoolbox as gpy
import numpy as np
import polyscope as ps
import argparse

def dir_path(string):
    if os.path.exists(string):
        return string
    else:
        return None