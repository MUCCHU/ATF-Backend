#!./env/bin/python
import os
x= os.system("export FLASK_ENV=development")
print(x)
os.system("echo Hello World!")
print("Environment set to development, Debugger ON")