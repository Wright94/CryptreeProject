# CryptreeProject

This Repo will contain all relevant files for the Cryptree Final Year Project.


===============================================
                myFuseFS.py
===============================================

In order to execute myFuseFS.py you must first make sure that you have installed the latest
version of fusepy.

To execute the script and mount the file system to your chosen directory you must enter 
the command:

$ python myFuseFS.py /full/path/chosen/dir /full/path/mnt/pnt

Eg.

$ python myFuseFS.py /Users/Harry/Documents /Users/Harry/fsMount

fsMount will now mirror /Documents directory and allow you to execute typical file and filesystem
commands.

------------Note-------------
At the top of myFuseFS.py is the line:

sys.path.append("/Users/Harry/Library/Python/3.5/lib/python/site-packages")

This is because on my own Mac, the sys.path does not look in the right place and so does
not pick up the fusepy library. I have tried to correct this but something isnt quite right.

Please remove this line before executing the script.
