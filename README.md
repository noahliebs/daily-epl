Runnning Redis
brew install redis

brew services start redis
brew services stop redis


Running Flask App
export FLASK_APP=app.py
export FLASK_ENV=development
python -m flask run