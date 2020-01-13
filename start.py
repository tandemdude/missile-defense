#! usr/bin/python3
import os

platform = os.name

if os.name == "nt":
	os.system("py -m source")
else:
	os.system("python3 -m source")