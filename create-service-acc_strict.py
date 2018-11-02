import json
import subprocess
import os
import time
import re
import string
from datetime import datetime
import cluster_strict

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
