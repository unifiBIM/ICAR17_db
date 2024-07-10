# SQL-Workflow
This script has been made as an **exercise** to populate a PostgreSQL database with data coming from a series of CSV files regarding the management of courses in a public university.

PostgreSQL is available for download as ready-to-use packages or installers for various platforms and you can download it from [here](https://www.postgresql.org/download/). Installation file includes also the GUI (pgAdmin)[https://www.pgadmin.org/), usefull for beginners. If you are interested in a deeper explanation of how PostgreSQL works you can find the official documentation [here][https://www.postgresql.org/docs/16/index.html).

In order to work with the database from Python you need an IDE (eg. [Spyder](https://www.spyder-ide.org/) or [PyCharm](https://www.jetbrains.com/pycharm/)) and you have to install some additional libraries: pandas, psycopg and SQLAlchemy.

## Check Python installation
Check which `python` version is currently used by your machine. This tutorial is prepared using Python 3.9.0 but you can use also a higher version.

```import sys
print( "You are using python version: ")
sys.version
```
## Create Virtual Environment
If you are working locally, then it is recommended to work with a local [virtual environment](https://docs.python.org/3/library/venv.html).

A virtual environment in Python is an isolated environment that allows you to manage and install packages independently of your system-wide Python installation. This isolation helps to avoid conflicts between dependencies and ensures that your projects have access to the specific versions of packages they need. Here are some key points about virtual environments:

### Key Features and Benefits:

1. **Isolation**: Each virtual environment has its own set of installed packages and dependencies, separate from other environments and the system Python installation.

2. **Dependency Management**: You can install and manage project-specific dependencies without affecting other projects or the global Python installation.

3. **Reproducibility**: Ensures that a project can be replicated on another system with the same set of dependencies, making it easier to share projects with others or deploy them on different machines.

4. **Version Control**: Allows you to test projects with different versions of packages without interfering with other projects.

### How to Create and Use a Virtual Environment:

1. **Creating a Virtual Environment**:
   - Using `venv` (included in Python 3.3 and above):
     ```sh
     python -m venv myenv
     ```
   - Using `virtualenv` (requires installation):
     ```sh
     pip install virtualenv
     virtualenv myenv
     ```

2. **Activating the Virtual Environment**:
   - On Windows:
     ```sh
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source myenv/bin/activate
     ```

3. **Installing Packages**:
   - Once the virtual environment is activated, you can install packages using `pip`:
     ```sh
     pip install package_name
     ```

4. **Deactivating the Virtual Environment**:
   - To deactivate the virtual environment and return to the global Python environment:
     ```sh
     deactivate
     ```

5. **Deleting the Virtual Environment**:
   - To remove a virtual environment, simply delete the directory:
     ```sh
     rm -rf myenv
     ```

### Example Workflow:

1. Create a new virtual environment for your project:
   ```sh
   python -m venv myprojectenv
   ```

2. Activate the virtual environment:
   ```sh
   source myprojectenv/bin/activate  # macOS/Linux
   myprojectenv\Scripts\activate     # Windows
   ```

3. Install required packages:
   ```sh
   pip install requests numpy
   ```

4. Work on your project, knowing the dependencies are isolated.

5. Deactivate the environment when done:
   ```sh
   deactivate
   ```

Using virtual environments is a best practice for Python development, especially when managing multiple projects or working in a team.

## Required packages
For this tutorial, the following packages are needed:
- [pandas](https://pandas.pydata.org/)
- [psycopg](https://www.psycopg.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

If you are working locally, then install them preferably in your active virtual environment. If you are working in Google Colab, then install them in that Google Colab environment. As a third option, you can install them in your local machine.

Check if your current python environment has the required packages for this tutorial installed:

```import pandas
import psycopg
import sqlalchemy
```

If there is a **ModuleNotFoundError**, then install the missing modules, using `pip install`:

```pip install pandas
pip install "psycopg[binary]"
pip install SQLAlchemy
```
