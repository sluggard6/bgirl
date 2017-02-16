from fabric.api import *
from fabric.contrib.files import exists

test_server = 'admin@106.75.97.108'
server = ''
env.passwords = {test_server: 'bg@2016#girl'}
base_root = '/var/www/bgirl'
proj_name = 'admin'
base_code = '/data/code'
base_project = 'bgirl'
remote_code = "git@git.coding.net:sluggard/bgirl.git"
full_path = "%s/%s" % (base_code, base_project)

@hosts(test_server)
def deploy_release():
    # root = '%s/%s_release' % (base_root, proj_name)
    proj_folder = '%s_release' % proj_name
    deploy_project(proj_folder, "release")
#
# @hosts(test_server)
# def deploy_dev():
#     root = '%s/%s_dev' % (base_root, proj_name)
#     branch = 'dev'
#     deploy_project(root, branch)


@hosts(server)
def deploy_biz():
    deploy({
        'remote': 'git@git.coding.net:sluggard/biz.git',
        'local': 'luhu_biz',
        'base': '/usr/mfwifi/lib'
    },"master")


@hosts(test_server)
def deploy_biz_release():
    deploy({
        'local': 'bg_biz',
        'base': '/usr/bgirl/lib/release'
    },"release")

@hosts(test_server)
def deploy_sharper_release():
    deploy({
        'local': 'sharper',
        'base': '/usr/bgirl/lib/release'
    },"release")



# @hosts(server)
# def deploy_prod():
#     #10.10.131.25
#     #10.10.84.253
#     root = '%s/%s' % (base_root, proj_name)
#     branch = 'master'
#     deploy_project(root, branch)


def deploy_project(proj_floder, branch):
    update_code(branch)
    with cd(full_path):
        deploy_path = '%s/%s' % (base_root, proj_floder);
        if exists(deploy_path):
            run('rm -rf %s' % deploy_path)
        run('cp -rf %s %s' % (proj_name, deploy_path))
    touchload()

def update_code(branch):
    if not exists(full_path):
        with cd(base_code):
            run('git clone %s %s' % (remote_code, base_project))
            with cd(full_path):
                run('git checkout %s' % branch)
    else:
        with cd(full_path):
            run('git stash')
            run('git checkout %s' % branch)
            run('git pull')

def deploy(project, branch, need_reload=True):
    config = project
    base = config.get('base')
    proj_name = config.get('local')
    update_code(branch)
    with cd(full_path):
        deploy_path = '%s/%s' % (base, proj_name);
        if exists(deploy_path):
            run('rm -rf %s/%s' % (base, proj_name))
        run('cp -rf %s %s' % (proj_name, base))
    if need_reload:
        touchload()



def touchload():
    run('touch /var/run/uwsgi/reload.uwsgi')
