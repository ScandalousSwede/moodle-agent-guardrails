
# Stub module for backward compatibility
# This file imports from the new location to maintain compatibility with existing code
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.moodle_guardrails import *
