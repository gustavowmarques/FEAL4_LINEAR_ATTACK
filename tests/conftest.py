import os, sys
# Put project root (parent of tests/) on sys.path so 'import src.*' works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
