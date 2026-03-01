# makby-test

This is my solution to the software engineering exercises for Makby's software engineering role.

## Setting up the environment:

**TL;DR <br/>1. Set project Python version to 3.12.12.<br/> 2. Create virtual environment with Python's `python3 -m venv .venv`.<br/> 3.Activate virtual environment with `source .venv/bin/activate`.<br/> 4. Install dependencies via `pip install -r requirements.txt`<br> 5. Run the solution files for exercises 1 or 2 with `python3 -m src.exerciseN.solution`, just replace exerciseN with exercise1 or exercise2.<br/> 6. _(Optional)_ Launch the web viewer with `python3 webviewer/app.py` and open [http://localhost:5000](http://localhost:5000) to browse all exercise results interactively.**

> [!NOTE]
> Before setting up the dependencies for the project please make sure you have the following base dependencies installed: <br/>
> [pip - A python package manager](https://pypi.org/project/pip/) <br/>
> [pyenv - A python version manager](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) <br/>
> [make - a UNIX program compilation utility](https://www.gnu.org/software/make/manual/make.html) **this one is optional** <br/>
> [Brew - a package manager for MacOS](https://brew.sh/) **Optional and only for MacOS users** <br/>

**Additionally, please note that the guide assumes that the user is in a Linux/UNIX environment like any Linux distribution such as Ubuntu, Fedora, and ArchLinux, or MacOS. If the user is using Windows, the structure of the commands below will change, and certain dependencies, like pyenv, [will require different installations](https://github.com/pyenv/pyenv?tab=readme-ov-file#windows).**

### Using `make`:

The repository includes a [`Makefile`](/makby-test/Makefile) which can easily install the necessary dependencies and setup the development environment to run the project. [MacOS users will need to install make through brew or XCode](https://formulae.brew.sh/formula/make). Once `make` is installed, run the following command:

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

That should create a [`.python-version` file](/makby-test/.python-version), check it an ensure it registered the correct version. You can also run:

```sh
python3 --version
```

To check that the correct version was set.

#### Setting up a virtual environment:

Virtual environments are used in Python to avoid global package installations and version collisions. To create a virtual environment, run the following command:

```sh
python3 -m venv .venv
```

This will create a virtual environment folder called `.venv` at the root of the repository. Now we need to activate the virtual environment:

```sh
source .venv/bin/activate
```

#### Installing dependencies:

Now that the virtual environment has been created, we can install the project dependencies with one simple command:

```sh
pip install -r requirements.txt
```

#### Running solution files:

To run the solution files for [exercise 1](/makby-test/src/exercise1/solution.py) or [exercise 2](/makby-test/src/exercise2/solution.py) run the following command:

```sh
python3 -m src.exercise1.solution # for exercise 1

python3 -m src.exercise2.solution # for exercise 2
```

## Viewing Results (Web Viewer):

The repository includes a small Flask-based web viewer that renders the results of all three exercises in a local browser. No separate display server needed!

### What it shows:

- **Exercise 1** — Interactive plot of the fill-pattern regions + a collapsible G-code viewer with a download button.
- **Exercise 2** — Plot of the flat template, 2D ring, and 3D cylinder mappings.
- **Exercise 3** — Rendered Markdown document with an option to open a print-friendly view and save it as a PDF.

All plots support click-to-fullscreen (or the dedicated **⛶ Full screen** button) and can be opened in a new tab for native zoom/pan.

### Running the web viewer:

#### With `make`:

```make
make webviewer
```

#### Without `make`:

Make sure the virtual environment is activated, then run:

```sh
python3 webviewer/app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser. Press `Ctrl+C` in the terminal to stop the server.

> [!NOTE]
> The first load of an exercise plot may take a few seconds as it is generated on demand. Subsequent loads are fast because the browser caches the image.

## Sources:

### For understanding GCode commands/generation:

1. https://www.klipper3d.org/G-Codes.html
2. https://sourceforge.net/p/easycnc/wiki/G-Code/
3. https://linuxcnc.org/docs/html/gcode/g-code.html

## Usage of AI:

The [`utils/` folder](/src/utils/README.md), the [webviewer](/webviewer/README.md), and the [solution document](/src/exercise3/solution.md) for the 3rd exercise all contain notes on the usage of AI throughout the project, as per the guidelines.
