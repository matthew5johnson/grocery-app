import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/matthew5johnson/grocery-app.git'

def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'  # env.user = username for logging into the server. host = address of the server we've specified on the CL (i.e. superlists-staging.matthew5johnson.com)
	run(f'mkdir -p {site_folder}')  # run is the most common fabric command. It says to run this shell command on the server. mdkir -p makes directories all the way down the list is necessary, and just sits tight if the dir is already made
	with cd(site_folder):
		_get_latest_source()
		_update_virtualenv()
		_create_or_update_dotenv()
		_update_static_files()
		_update_database()

def _get_latest_source():
	if exists('.git'):
		run('git fetch')

	else:
		run(f'git clone {REPO_URL} .')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'git reset --hard {current_commit}')

def _update_virtualenv():
	if not exists('virtualenv/bin/pip'):
		run(f'python3.6 -m venv virtualenv')
	run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
	append('.env', 'DJANGO_DEBUG_FALSE=y')
	append('.env', f'SITENAME={env.host}')
	current_contents = run('cat .env')
	if 'DJANGO_SECRET_KEY' not in current_contents:
		new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
		append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
	run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
	run('./virtualenv/bin/python manage.py migrate --noinput')