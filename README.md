# ntn-backend

###To run the project

1. Install Python 3 if you haven’t done so already
2. Create a virtual environment:
   • Choose a location in which to create the virtual environment. I call it “venv” and don’t put it
   in my repo, but if you put it anywhere in your repo, be sure to put the name of the virtual
   environment directory into your .gitignore. (Our default .gitignore contains venv.)
   cd <location for your virtual environment folder>
   python3 -m venv venv
3. Activate your virtual environment using the appropriate command for your shell:
   • MAC zsh: source venv/bin/activate
   • MS cmd.exe: venv\Scripts\activate.bat
   • Linux csh: source venv/bin/activate.csh
   (See https://docs.python.org/3/library/venv.html for other shells)
4. Install Django
   • Upgrade pip to the most current version:
   python3 -m pip install --upgrade pip
   • Then install Django
   python3 -m pip install django
5. python3 -m pip install djangorestframework
6. python3 manage.py migrate
   python3 manage.py runserver
