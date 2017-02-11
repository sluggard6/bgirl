from fabric.api import *
from fabric.contrib.files import exists

test_server = 'admin@123.206.33.80'
foxconn = 'admin@210.83.232.53'
env.passwords = {test_server: 'luhu#2014!'}
base_root = '/var/www/hiwifi'
proj_name = 'luhu_admin'
old_prod = 'admin@120.132.69.41'
new_prod = 'admin@123.206.20.48'


@hosts(test_server)
def deploy_release():
    root = '%s/%s_release' % (base_root, proj_name)
    branch = 'develop'
    deploy_admin(root, branch)


@hosts(old_prod)
def deploy_prod():
    root = base_root + '/' + proj_name
    branch = 'master'
    deploy_admin(root, branch)


@hosts(new_prod)
def deploy_prod_new():
    root = base_root + '/' + proj_name
    branch = 'master'
    deploy_admin(root, branch)


def deploy_admin(root, branch):
    if not exists(root):
        deploy_dir = root.split('/')[-1]
        parent = root.rstrip(deploy_dir)
        with cd(parent):
            print 'enter dir ' + parent
            run('git clone git@git.hi-wifi.cn:hiwifi/admin.git --depth 1 %s ' % proj_name)
            if deploy_dir != proj_name:
                run('mv %s %s' % (proj_name, deploy_dir))
            with cd(root):
                run('git checkout %s' % branch)
    else:
        with cd(root):
            run('git stash')
            run('git checkout %s' % branch)
            run('git pull')

    touchload()


@hosts(foxconn)
def deploy_foxconn():
    root = base_root + '/' + proj_name
    branch = 'master'
    config = '%s/%s' % (root, 'config/config.py')
    foxconn_config = '%s/%s' % (root, 'config/config_foxconn.py')
    if not exists(root):
        deploy_dir = root.split('/')[-1]
        parent = root.rstrip(deploy_dir)
        with cd(parent):
            print 'enter dir ' + parent
            run('git clone git@gitcafe.com:hiwifiio/luhu-admin.git --depth 1 %s ' % proj_name)
            if deploy_dir != proj_name:
                run('mv %s %s' % (proj_name, deploy_dir))
            with cd(root):
                run('git checkout %s' % branch)
                run('mv %s %s' % ('', 'config/config.py'))
    else:
        with cd(root):
            run('git stash')
            run('git checkout %s' % branch)
            run('git pull')

    run('mv %s %s' % (foxconn_config, config))
    touchload()


def touchload():
    run('touch /var/run/uwsgi/reload.uwsgi')
