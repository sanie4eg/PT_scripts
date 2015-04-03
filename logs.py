__author__ = 'Oleksandr Sechko'
#!/usr/bin/python
import os,sys
import paramiko

def ssh_command():
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(sys.argv[2], username='oleksandrse')

        stdin, stdout, stderr = ssh.exec_command('sudo su - apps -c "/opt/local/apps/bin/apps_list| grep chat')
        for line in stdout.readlines():
            print line
#       for line in stderr.readlines():
#           print line
if  len(sys.argv) == 1:
        print "USAGE: remote_service -c <hostname>"
else:
        if  sys.argv[1] == '-c':
                ssh_command()

