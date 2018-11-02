import json
import subprocess
import os
import time
import re
import string
from datetime import datetime
import cluster_strict

#def create_service_account(service_account_name, service_account_secret,strict):  
force_start_cmd = "sudo rm -rf ~/.dcos && sudo rm -rf /usr/local/bin/dcos && [ -d /usr/local/bin ] || sudo mkdir -p /usr/local/bin && curl https://downloads.dcos.io/binaries/cli/linux/x86-64/dcos-1.10/dcos -o dcos && sudo mv dcos /usr/local/bin && sudo chmod +x /usr/local/bin/dcos && dcos cluster setup "+cluster_strict.CLUSTER_URL+" --insecure --username=bootstrapuser --password=deleteme"

print("Command to Force install Cluster: "+force_start_cmd)
disc_status = subprocess.call(force_start_cmd, shell=True)
time.sleep(3)
print('cluster url is '+cluster_strict.CLUSTER_URL)

pkg_task_value = subprocess.check_output('dcos package install dcos-enterprise-cli --yes', shell=True)
pkg_task_value = subprocess.check_output('curl -k -v '+cluster_strict.CLUSTER_URL+'/ca/dcos-ca.crt -o dcos-ca.crt', shell=True)
pkg_task_value = os.system('export LC_ALL=C.UTF-8')
pkg_task_value = os.system('export LANG=C.UTF-8')
pkg_task_value = os.system('dcos security org service-accounts keypair jenkins-private-key.pem jenkins-public-key.pem')
pkg_task_value = os.system('dcos security org service-accounts create -p jenkins-public-key.pem -d "jenkins service account" jenkins_service_account')
    
pkg_task_value = os.system('dcos security secrets create-sa-secret --strict jenkins-private-key.pem jenkins_service_account dcos_jenkins_secret')
pkg_task_value = os.system('dcos security org users grant jenkins_service_account dcos:superuser full --description "grant permission to superuser"')
print('\033[43m'+'Service account created for account={account} secret={secret}'.format(account='jenkins_service_account',secret='dcos_jenkins_secret')+'\x1b[0m')
config_data=os.system("echo '{\"marathon-lb\": {\"secret_name\": \"dcos_jenkins_secret\",\"marathon-uri\": \"https://marathon.mesos:8443\"}}' > config.json")
pkg_task_value=os.system('dcos package install --options=config.json marathon-lb --yes')
