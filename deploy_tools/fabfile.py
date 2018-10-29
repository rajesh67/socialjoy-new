import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/rajesh67/socialjoy.git'  

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  
    run(f'mkdir -p {site_folder}')  
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
        new_secret = ''.join(random.SystemRandom().choices(  
            '1*b84qe7z%4v)(_ji01k^_xx2tkhs062zpsza9gpzl3rxdfhfv', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')


#cat ./deploy_tools/nginx.template.conf | sed "s/DOMAIN/yogdaan.org.in/g" | sudo tee /etc/nginx/sites-available/yogdaan.org.in
#sudo ln -s /etc/nginx/sites-available/yogdaan.org.in /etc/nginx/sites-enabled/yogdaan.org.in
#cat ./deploy_tools/gunicorn-systemd.template.service | sed "s/DOMAIN/yogdaan.org.in/g" | sudo tee /etc/systemd/system/gunicorn-yogdaan.org.in.service

#sudo systemctl daemon-reload
#elspeth@server:$ sudo systemctl reload nginx
#elspeth@server:$ sudo systemctl enable gunicorn-yogdaan.org.in
#elspeth@server:$ sudo systemctl start gunicorn-yogdaan.org.in
