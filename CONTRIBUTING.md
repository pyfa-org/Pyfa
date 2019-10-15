# Contribution

## Requirements

- Python 3.6
- Git CLI installed
- Python, pip and git are available as commands (add to path if needed)

## Setting up the project manually

Virtual environment will be created in *PyfaEnv* folder. Project will be cloned and run from the *PyfaDEV* folder. Separate virtual environment will be created so required libraries won't clutter the main python installation.

Clone the repo 
`git clone <repo> PyfaDEV`

Create virtual environment
`python -m venv PyfaEnv`

Activate virtual environment

```
For cmd.exe: PyfaEnv\scripts\activate.bat
For bash: source <venv>/bin/activate
```
> For other OSes check [Python documentation](https://docs.python.org/3/library/venv.html)

Install requirements for the project from *requirements.txt*
`pip install -r PyfaDEV\requirements.txt`

Check that libs from *requirements.txt* are installed
`pip list`

Test that the project is starting properly
`python PyfaDEV\pyfa.py`



## Setting up the project with PyCharm/IntelliJ
