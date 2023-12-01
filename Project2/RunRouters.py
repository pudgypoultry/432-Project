import socket
import sys
import traceback
from NetworkingHelpers import *
from threading import Thread

def execute_python_file(file_path):
   try:
      with open(file_path, 'r') as file:
         python_code = file.read()
         exec(python_code, locals())
   except FileNotFoundError:
      print(f"Error: The file '{file_path}' does not exist.")

thread1 = Thread(target = execute_python_file, args = ["router1.py"])
thread2 = Thread(target = execute_python_file, args = ["router2.py"])
thread3 = Thread(target = execute_python_file, args = ["router3.py"])
thread4 = Thread(target = execute_python_file, args = ["router4.py"])
thread5 = Thread(target = execute_python_file, args = ["router5.py"])
thread6 = Thread(target = execute_python_file, args = ["router6.py"])

thread1.start()
thread4.start()
thread6.start()
thread5.start()
thread3.start()

thread2.start()





"""
execute_python_file("router6.py")
execute_python_file("router5.py")
execute_python_file("router3.py")
execute_python_file("router4.py")
execute_python_file("router2.py")
execute_python_file("router1.py")
"""