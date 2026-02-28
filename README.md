# makby-test

This is my solution to the software engineering exercises for Makby's software engineering role.

## Setting up the environment:

> [!NOTE]
> Before setting up the dependencies for the project please make sure you have the following base dependencies installed:
> [pip - A python package manager](https://pypi.org/project/pip/)

> [pyenv - A python version manager](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

> [make - a UNIX program compilation utility](https://www.gnu.org/software/make/manual/make.html) **this one is optional**

> [Brew - a package manager for MacOS](https://brew.sh/) **Optional and only for MacOS users**

**Additionally, please note that the guide assumes that the user is in a Linux/UNIX enviornment like any Linux distribution such as Ubuntu, Fedora, and ArchLinux, or MacOS. If the user is using Windows, the structure of the commands below will change, and certain dependencies, like pyenv, [will require different installations](https://github.com/pyenv/pyenv?tab=readme-ov-file#windows).**

### Using `make`:

The repository includes a [`Makefile`](/makby-test/Makefile) which can easily install the necessary dependencies and setup the development enviornment to run the project. [MacOS users will need to install make through brew or XCode](https://formulae.brew.sh/formula/make). Once `make` is installed, run the following command:

```make
make help # lists all available commands
```

or

```make
make dependencies # will bootsrtap all project dependecies assuming the user has python, pip, pyenv
```

Afterwards, the solution files for [exercise 1](/makby-test/src/exercise1/solution.py) or [exercise 2](/makby-test/src/exercise2/solution.py) can be executed by running the following command:

```make
make exerciseN
```

just replace `N` with 1 or 2 depending on which exercise solution file you wish to run.

### Without `make`:

#### Setting python version via pyenv:

Python scientific libraries like `numpy`, `pyclipper`, and `matplotlib` often run behind the latest Python version, so to ensure the usage of a stable but not too old Python version we can use `pyenv`. Run this command to set the local version of Python:

```sh
pyenv local 3.12.12
```

That should create a [`.python-version` file](/makby-test/.python-version), check it an ensure it rtegistered the correct version. You can also run:

```sh
python3 --version
```

To check that the correct version was set.

#### Setting up a virtual enviornment:

Virtual environments are used in Python to avoid global package installations and version collisions. To create a vritual envrionment, run the following command:

```sh
python3 -m venv .venv
```

This will create a virtual environment folder called `.venv` at the root of the repository. Now we need to activate the virtual environment:

```sh
source .venv/bin/activate
```

#### Installing dependencies:

Now that the virtual enviornment has been created, we can install the project dependencies with one simple command:

```sh
pip install -r requirements.txt
```

#### Running solution files:

To run the solution files for [exercise 1](/makby-test/src/exercise1/solution.py) or [exercise 2](/makby-test/src/exercise2/solution.py) run the following command:

```sh
python3 -m src.exercise1.solution # for exercise 1

python3 -m src.exercise2.solution # for exercise 2
```

## Sources:

### For understanding GCode commands/generation:

1. https://www.klipper3d.org/G-Codes.html
2. https://sourceforge.net/p/easycnc/wiki/G-Code/
3. https://linuxcnc.org/docs/html/gcode/g-code.html

## Stuff to work on (besides the exercises):

1. Generating good pydocs / readmes for each function and file/folders
2. Makefile to setup and get the project running.
3. Basic html website to visualize stuff (idk if i will need streamlit)
4. Tests (?)
