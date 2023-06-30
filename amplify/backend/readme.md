## These steps are required to properly setup pipenv packages to make Amplify work 
- go to local function folder eg. `cd /Users/josereyes/Dev/cevo-shopping-demo/amplify/backend/function/getProducts`
- `pipenv --rm` to remove the virtual environment
- `pipenv install --python 3.9` to create a new virtual environment ==> JO Change all to use 3.9 as that is the maximum that Amplify supports
- `pipenv shell` to enter the virtual environment
- `python`, then `import sys`, then `sys.executable` to deterimine the path to the python executable
- `quit()` to exit python
- `exit` to exit the virtual environment
- `amplify push -y` to push the function to the cloud