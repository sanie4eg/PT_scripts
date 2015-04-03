import os,sys
import paramiko

hosts = {'pt-stg' : ['intstg1-cmr-privil-server-01.ptstaging.ptec', 'intstg1-cmr-privil-server-02.ptstaging.ptec', 'intstg1-ua-privil-admin-01.ptstaging.ptec']}



def get_host_key(host):
    hostkeytype = None
    hostkey = None
    # try to load host key from known hosts
    try:
        host_keys = paramiko.util.load_host_keys(
            os.path.expanduser("~/.ssh/known_hosts"))
    except IOError:
        host_keys = {}
    if host in host_keys:
        hostkeytype = host_keys[host].keys()[0]
        hostkey = host_keys[host][hostkeytype]
    return hostkeytype, hostkey

def get_private_key(keyfile=None):
    key = None
    keytype = None
    if keyfile is None:
        keyfiles = [os.path.expanduser('~/.ssh/id_%s' % keytype)
                    for keytype in ('dsa', 'rsa')]
    else:
        keyfiles = [keyfile]
    for kf in keyfiles:
        try:
            key = paramiko.DSSKey.from_private_key_file(kf)
            keytype = 'ssh-dsa'
            return keytype, key
        except (IOError, paramiko.SSHException), e:
            try:
                key = paramiko.DSSKey.from_private_key_file(kf)
                keytype = 'ssh-rsa'
            except (IOError, paramiko.SSHException), e:
                pass
    if key is None:
        raise paramiko.SSHException('No rsa or dsa keys are available')

def put_remote_file(user, host, path, pkeyfile=None):
    hostkeytype, hostkey = get_host_key(host)
    userkeytype, userkey = get_private_key(pkeyfile)
    t = paramiko.Transport((host, 22))
    t.connect(hostkey=hostkey, username=user, pkey=userkey)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(path, path)
    t.close()
def get_remote_file(user, host, path, pkeyfile=None):
    hostkeytype, hostkey = get_host_key(host)
    userkeytype, userkey = get_private_key(pkeyfile)
    t = paramiko.Transport((host, 22))
    t.connect(hostkey=hostkey, username=user, pkey=userkey)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(path, sys.argv[3])
    t.close()
def run_command():
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=22)
        channel = client.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(5)
        print os.listdir(path)

        channel.exec_command(command)
        print channel.recv(1024)
        channel.close()
        client.close()

tomcat_webapps = '/opt/local/tomcat/webapps/'
for i in hosts[sys.argv[1]]:
    put_remote_file('oleksandrse', hosts[sys.argv[1]][i], '~/scripts/cm_version.sh')
    print "Done with", hosts[sys.argv[1]][i]





