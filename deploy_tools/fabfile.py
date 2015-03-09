from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import time
import sys
import os

REPO_URL = 'https://github.com/kflavin/testdrivendevelopment.git'

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _install_packages(source_folder)
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    # Don't think we need this?
    #_install_gunicorn(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _configure_nginx(source_folder, env.host)
    _configure_gunicorn(source_folder, env.host)
    _start_services(env.host)

def _install_packages(source_folder):
    run('sudo apt-get install -y nginx python-virtualenv git')

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))

    print "your current folder", os.getcwd()
    current_commit = local("git log -n 1 --format=%H", capture=True)
    print "I found current commit to be", current_commit
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _install_gunicorn(source_folder):
    run('cd %s && ../virtualenv/bin/pip install gunicorn==18' % (source_folder))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/tdd/tdd/settings/production.py'
    sed(settings_path, "DEBUG=True", "DEBUG=False")
    sed(settings_path, 
        'ALLOWED_HOSTS=.+$',
        'ALLOWED_HOSTS=["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/tdd/tdd/settings/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements/production.txt' % ( virtualenv_folder, source_folder))

def _update_static_files(source_folder):
    run('cd %s/tdd && DJANGO_SETTINGS_MODULE=tdd.settings.production ../../virtualenv/bin/python manage.py collectstatic --noinput' % (source_folder,))

def _update_database(source_folder):
    run('cd %s/tdd && DJANGO_SETTINGS_MODULE=tdd.settings.production ../../virtualenv/bin/python manage.py migrate --noinput' % (source_folder,))

def _configure_nginx(source_folder, site_name):
    run('cd %s/deploy_tools && sed "s/SITENAME/%s/g" nginx.template.conf | sudo tee /etc/nginx/sites-available/%s' % (source_folder, site_name, site_name))
    run('test -L /etc/nginx/sites-enabled/%s || sudo ln -s ../sites-available/%s /etc/nginx/sites-enabled/%s' % (site_name, site_name, site_name))
    run('sudo sed -i "s/# server_names_hash_bucket_size 64;/server_names_hash_bucket_size 256;/" /etc/nginx/nginx.conf')

def _configure_gunicorn(source_folder, site_name):
    run('cd %s/deploy_tools && sed "s/SITENAME/%s/g" gunicorn-upstart.template.conf | sudo tee /etc/init/gunicorn-%s.conf' % (source_folder, site_name, site_name))
    run('test -L /etc/nginx/sites-enabled/%s || sudo ln -s ../sites-available/%s /etc/nginx/sites-enabled/%s' % (site_name, site_name, site_name))
    run('sudo sed -i "s/# server_names_hash_bucket_size 64;/server_names_hash_bucket_size 256;/" /etc/nginx/nginx.conf')

def _start_services(site_name):
    run('sudo service nginx reload')
    run('sudo start gunicorn-%s' % site_name)
