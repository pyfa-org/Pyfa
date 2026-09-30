# Contribution

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- Git CLI installed


> Commands and screens were created on Windows 10. Please, update all the paths according to your OS.

## Setting up the project manually

Clone the repository
```
git clone <repo> pyfa
```

Install the locked dependencies. This creates `.venv` and downloads interpreter and necessary packages.
```
cd pyfa
uv sync
```

Check what was installed
```
uv pip list
```

### wxPython on linux

On Windows and macOS wxPython installs binary package. On linux there is no binary package in pypi, which leads us to two options:

- build from source (needs extra dependencies, slow)
- install wheels from github release page (fast, but high chance they are linked to libraries which do not exist on your system)

First is executed with regular `uv sync` command. The second needs `uv sync --no-default-groups --group dev --group wx-binary`; 
it grabs binary package built for Ubuntu 22.04. If you need wxPython for different Ubuntu version, you will have to edit `pyproject.toml`.

Build translations and database:
```
uv run python scripts/compile_lang.py
uv run python db_update.py
```

Test that the project is starting properly
```
uv run python pyfa.py
```

`uv run` syncs the environment before each command, so there is no virtualenv to
activate manually. If you prefer an activated shell, the venv is at `.venv`.

## Setting up the project with PyCharm/IntelliJ

Install PyCharm / Other IntelliJ product with Python plugin

After launching - select *Check out from Version Control* -> *GIt*

![welcome](https://user-images.githubusercontent.com/54093496/66862580-d8edab00-ef99-11e9-94e2-e93d7043e620.png)

Login to GitHub, paste the repo URL and select the folder to which to clone the project into, press *Clone*.

![Clone](https://user-images.githubusercontent.com/54093496/66862748-38e45180-ef9a-11e9-9f68-4903baf47385.png)

After the process is complete, run `uv sync` in a terminal at the project root to
create `.venv`.

Then open `File` -> `Settings` -> `Project` -> `Project Interpreter`.

![Settings](https://user-images.githubusercontent.com/54093496/66862792-544f5c80-ef9a-11e9-9e0f-f64767f3f1b0.png)

Press on options and add an existing virtual environment, pointing it at the
`.venv` folder uv created.

![venv](https://user-images.githubusercontent.com/54093496/66862833-67622c80-ef9a-11e9-94fa-47cca0158d29.png)

Create new *Run Configuration*. Set correct *Script path* and *Python interpreter*.

![Run configuraion](https://user-images.githubusercontent.com/54093496/66862970-b4460300-ef9a-11e9-9fb4-20e24759904b.png)

Check that the project is starting properly.

## Running tests

pytest is not a project dependency, so pull it in for the run:
```
uv run --with pytest python -m pytest
```

More information on tests can be found on appropriate [Wiki page](https://github.com/pyfa-org/Pyfa/wiki/Developers:-Writing-Tests-for-Pyfa).
