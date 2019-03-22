import paramiko
from os.path import expanduser
from user_definition import *

ssh = paramiko.SSHClient()

ec2_address = "ec2-3-18-113-18.us-east-2.compute.amazonaws.com"
user = "ec2-user"
key_file = "/Licenses/ljfernando.pem"

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ec2_address, username=user,
            key_filename=expanduser("~") + key_file)

create_env_command = "conda env create -f ~/google_maps/environment.yml"
update_env_command = "conda env update -f ~/google_maps/environment.yml"
stdin, stdout, stderr = ssh.exec_command(create_env_command)
if(b'already exists' in stderr.read()):
    stdin, stdout, stderr = ssh.exec_command(update_env_command)

git_repo_owner = "ljfernando"
git_repo_name = "google_maps"
git_user_id = "ljfernando"

git_pull_command = "git pull https://github.com/" + \
    git_user_id + "/" + git_repo_name + ".git"
git_clone_command = "git clone https://github.com/" + \
    git_user_id + "/" + git_repo_name + ".git"
stdin, stdout, stderr = ssh.exec_command(git_clone_command)
# If repo already exists, pull recent version
if (b"already exists" in stderr.read()):
    print('Repo exists. Pulling recent changes')
    stdin, stdout, stderr = ssh.exec_command(git_pull_command)
    print(stdout.read())
