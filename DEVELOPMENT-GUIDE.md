
# Development Guide

This file contains a step-by-step guide to implementing changes to the coastal-dynamics python package.

## 0. Clone coastal-dynamics repository
Before starting development, we advice to have the code locally with an editable installation. A locally editable installation of the coastal-dynamics package is useful to test any changes made before pushing the changes to the online repository. For this, a local clone of the coastal-dynamics repository is required.

For instructions on cloning a git repository, see: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

The coastal-dynamics repository can be found here:
https://github.com/Coastal-Dynamics/coastal-dynamics

## 1. Re-install
Within the coastalcodebook environment, the coastal-dynamics package is installed from the pypi library. In order to test changes made to the package locally, you have to create a local ‘developer installation’. That way, whenever the package is loaded in python, the code used is pulled from the local machine instead of the installation from pypi.
- Open the command prompt
- Activate the coastalcodebook environment
mamba activate coastalcodebook
- Uninstall the pypi install of the coastal-dynamics package
pip uninstall coastal-dynamics
- Navigate to the coastal-dynamics local directory (i.e., the directory that was created during step 0).
cd …/coastal-dynamics
- Install the package in the current directory (i.e., the coastal-dynamics directory) in developer (‘editor’) mode.
    > Make sure to include the ‘.’ at the end of the command!
pip install -e .

The coastal-dynamics package is now installed in developer mode (as an editable package) in the coastalcodebook environment.

## 2. Make changes
Any changes made to the source code of the coastal-dynamics package is now directly reflected when the package is loaded in python (within the coastalcodebook environment). However, the code that is active in python is updated only when the coastal-dynamics package is imported. Therefore, whenever you make a change in the coastal-dynamics source code, re-run ‘import coastal-dynamics’ in python to use / test your changes.

## 3. Push changes to branch
•	Create a new branch using git
    o	Ensure this branch is up-to-date with main
•	Run pre-commit (with your changes, on the new branch)
    o	Remove anything pre-commit has changed in files you have not changed.
•	Commit changes to branch
•	Push commits to remote

## 4. Update version numbers
•	After your branch is up-to-date with all changes, it is almost ready to merge to main. Before merging, you have to update the version numbers in the files “pyproj.toml” and “src/__init__.py”.
    o	This update is required before pypi accepts the updated version.

## 5. Run pre-commit
We use the pre-commit package to manage and maintain pre-commit hooks. pre-commit should be installed in your coastalcodebook package. Check for it in the list by typing the following command in the prompt:
mamba list

Next, we ensure pre-commit is installed for your repoistory. Navigate to the coastal-dynamics repository in the prompt, and run
pre-commit install

Finally, run pre-commit using the command:
pre-commit run --all-files

Commit the changes made by pre-commit.

## 6. Merge to main

•	Merge to main by ensuring all the changes are pushed to the remote ('git push')
•	Create a pull request in the online repository
•	Delete your branch
