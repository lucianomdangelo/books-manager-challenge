# FOR TES

# TO START
docker build . -t books-manager
docker run --name books-manager-container -p 8000:8000/tcp books-manager

or run ./run_dockerfile.sh

## TO RUN WITH PYTHON ENVIRONMENT

# install virtualenv if it's not installed already
pip install virtualenv 

# create the environment
python3 -m venv books-manager-challenge

# activate
source books-manager-challenge/bin/activate

# install dependencies
pip3 install fastapi pydantic requests sqlalchemy

# run the app
uvicorn app.main:app --reload