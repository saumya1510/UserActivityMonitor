The chrome extension tracks user activity on stack overflow, such as clicks, scrolls, question tags, etc. The python server logs these events on an MLab database (MongoDB). The details on the activities can be seen on the [website](saumya-cse591.herokuapp.com). 

Download the required libraries using `pip install -r requirements.txt`
Change the MLab authentication and location in application.py

To run the files locally:

1. Load the unpacked extension:
	chrome://extensions -> Load unpacked extension -> Select "Local Extension" Folder
	[The differences between the two are in manifest->permissions and content.js->url]
2. Make sure you have python 3.4 or above, and pip.
3. Go to command line, and type "pip install -r requirements.txt"
4. Run the application by "python application.py"
5. Look for the URL in the command line, given as  "Running on http://[localhost]:[port]". Usually it is "http://127.0.0.1:5000". 
6. If the URL is not "http://127.0.0.1:5000", you'll have to go to Local Extension -> content.js and change the URL in "passToServer()" function to the one given by the command line.
7. Type the url in the chrome browser and login using username as "aaa" or "bbb" or "ccc" and password "123"



