from fabric.api import *
from fabric.contrib.files import exists

test_server = 'admin@61.174.8.251'
test_server_bj = 'admin@120.132.49.11'
p1 = 'admin@122.226.44.71'
foxconn = ['admin@210.83.232.53']
env.passwords = {test_server: 'luhu#2014!'}
base_root = '/usr/hiwifi/lib'
proj_name = 'luhu_sharper'
bj = 'admin@120.132.69.41'


@hosts(test_server)
def deploy_release():
    root = base_root + '/release/' + proj_name
    branch = 'develop'
    deploy_sharper(root, branch)



@hosts(test_server_bj)
def deploy_release_bj():
    root = base_root + '/release/' + proj_name
    branch = 'release'
    deploy_sharper(root, branch)


@hosts(test_server)
def deploy_dev():
    root = base_root + '/dev/' + proj_name
    branch = 'dev'
    deploy_sharper(root, branch)


@hosts(p1)
def deploy_prod():
    root = base_root + '/' + proj_name
    branch = 'master'
    deploy_sharper(root, branch)


@hosts(foxconn)
def deploy_foxconn():
    root = base_root + '/' + proj_name
    branch = 'master'
    deploy_sharper(root, branch)


@hosts(bj)
def deploy_bj():
    root = base_root + '/' + proj_name
    branch = 'master'
    deploy_sharper(root, branch)


def deploy_sharper(root, branch):
    if not exists(root):
        parent = root.rstrip(proj_name)
        with cd(parent):
            run('git clone git@gitcafe.com:hiwifiio/luhu-sharper.git --depth 1 luhu_sharper')

            with cd(root):
                run('git checkout %s' % branch)
    else:
        with cd(root):
            run('git checkout %s' % branch)
            run('git pull')

    touchload()


def touchload():
    run('touch /var/run/uwsgi/reload.uwsgi')