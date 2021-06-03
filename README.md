# autobase_web
Website to control [twitter_autobase](https://github.com/fakhrirofi/twitter_autobase) database and trigger data updates.


## TODO (Developer)
- Add tests
- Update default_config (follow twitter_autobase)
- Complete form design using default_config
- Integrate with twitter_autobase
    * bridge between database and Autobase object
    * save twitter_autobase ngrok url to database
    * send trigger with requests.post to ngrok url
    * Re-code twitter_autobase starter (follow main.py)


## Requirements
- Python 3.8.x
- [git](#), [heroku](#), and [pip](#)
- Heroku Account (optional)


## Installation & Configuration
### Clone this repo
```bash
git clone https://github.com/fakhrirofi/autobase_web.git
# or download from release page
cd autobase_web
```
### Create virtual environment & install python package
Note: Delete `gunicorn` and `psycopg2` from requirements.txt if you are using windows.
```bash
python3 -m venv venv
source venv/bin/activate # linux
# venv\Scripts\Activate # windows
pip3 install -r requirements.txt
```
### Make .env file
Rename `.env.example` to `.env`, then edit its contents. <br>
Or (if using Heroku) add `.env` config vars on heroku app settings.
### Initialize the database
```bash
flask db init
flask db migrate -m initial
flask db upgrade
```
### Run the website locally
```bash
python3 start_gevent.py
```
Open 127.0.0.1:8000 on your web browser <br>
for debugging: (set the `FLASK_DEBUG` to 1 in `.flaskenv` file)
```bash
flask run
```

## Deploy to Heroku
Delete `gevent==21.1.2` and add `gunicorn==20.1.0` & `psycopg2==2.8.6` in requirements.txt <br>
**Set heroku app configuration**
```bash
heroku git:remote -a your-autobase-web-app-name
heroku addons:add heroku-postgresql:hobby-dev
```
Attach autobase_web database to [twitter_autobase](https://github.com/fakhrirofi/twitter_autobase) database
```bash
heroku addons
heroku addons:attach your-db-addon-name -a your-twitter-autobase-app-name
```
**Deploy the application**
```bash
git add .
git commit -m 'initial commit'
git push heroku main
```
### Heroku (free-tier) limitations
- 550 dyno hours, you can upgrade to 1000 dyno hours by adding credit card (it's free for free-tier)
- 4 hours downtime for Postgres per month
<!-- - After 30 minutes of inactivity, the app automatically turned off
### no-request handling
I don't know whether it's illegal or not to keep your free heroku app alive :D <br>
Here are the steps:
1. Sign up and login at https://cron-job.org
2. Create cronjob at https://cron-job.org/en/members/jobs/add/
3. Fill the address with your heroku app address, example: `https://example.herokuapp.com/`
4. Set the schedule for every 25 minutes (or under 30 minutes)
5. Submit the form -->


## Reference
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
