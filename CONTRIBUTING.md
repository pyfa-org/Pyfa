# Contribution

## Requirements

- Python 3.7
- Git CLI installed
- Python, pip and git are all available as command-line commands (add to the path if needed)

Virtual environment will be created in *PyfaEnv* folder. Project will be cloned and run from the *PyfaDEV* folder. Separate virtual environment will be created so required libraries won't clutter the main python installation.

> Commands and screens were created on Windows 10. Please, update all the paths according to your OS.

## Setting up the project manually

Clone the repository
```
git clone <repo> PyfaDEV
```

Create the virtual environment
```
python -m venv PyfaEnv
```

Activate the virtual environment

```
For cmd.exe: PyfaEnv\scripts\activate.bat
For bash: source <venv>/Scripts/activate
```
> For other OS check [Python documentation](https://docs.python.org/3/library/venv.html)

Install requirements for the project from *requirements.txt*
```
pip install -r PyfaDEV\requirements.txt
```
> For some Linux distributions, you may need to install separate wxPython bindings, such as `python-matplotlib-wx`

Check that the libs from *requirements.txt* are installed
```
pip list
```

Build translations and database:
```
python scripts\compile_lang.py
python db_update.py
```

Test that the project is starting properly
```
python PyfaDEV\pyfa.py
```


## Setting up the project with PyCharm/IntelliJ

Install PyCharm / Other IntelliJ product with Python plugin

After launching - select *Check out from Version Control* -> *GIt*

![welcome](https://user-images.githubusercontent.com/54093496/66862580-d8edab00-ef99-11e9-94e2-e93d7043e620.png)

Login to GitHub, paste the repo URL and select the folder to which to clone the project into, press *Clone*.

![Clone](https://user-images.githubusercontent.com/54093496/66862748-38e45180-ef9a-11e9-9f68-4903baf47385.png)

After process is complete, open *File* -> *Settings* -> *Project* -> *Project Interpreter*. 

![Settings](https://user-images.githubusercontent.com/54093496/66862792-544f5c80-ef9a-11e9-9e0f-f64767f3f1b0.png)

Press on options and add new virtual environment.

![venv](https://user-images.githubusercontent.com/54093496/66862833-67622c80-ef9a-11e9-94fa-47cca0158d29.png)

Open project tree view and double-click on the *requirements.txt*. Press *Install requirements*. Install all requirements.

![Reqs](https://user-images.githubusercontent.com/54093496/66862870-7a74fc80-ef9a-11e9-9b18-e64be42c49b8.png)

Create new *Run Configuration*. Set correct *Script path* and *Python interpreter*.

![Run configuraion](https://user-images.githubusercontent.com/54093496/66862970-b4460300-ef9a-11e9-9fb4-20e24759904b.png)

Check that the project is starting properly.

## Running tests

Switch to the proper virtual environment
```
For cmd.exe: PyfaEnv\scripts\activate.bat
For bash: source <venv>/Scripts/activate
```

Install pytest 
```
pip install pytest  
```

Switch to pyfa directory.

Run tests (any will do)
```
python -m pytest
py.test
```

More information on tests can be found on appropriate [Wiki page](https://github.com/pyfa-org/Pyfa/wiki/Developers:-Writing-Tests-for-Pyfa).
