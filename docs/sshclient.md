# Creating an SSH Client

Creating a Conch based SSH Client involves  knowledge/experience about/with four things:

* async/await
* host key fingerprints (SSH trust)
* certificates (SSH authentication)
* Conch SSH Framework

# Creating Host Fingerprint

When creating an SSH Client using the Conch framework we need to provide a fingerprint of the
host we are connecting to. This is used to validate we trust that host. 

The following script will generate the fingerprints for a given list of target hosts:

``` bash
#!/usr/bin/env bash
hosts=('raspie.lan' 'expressionist.lan')
for i in ${hosts[*]}; do
        echo ${i}
        ssh-keyscan "${i}" 2>/dev/null | ssh-keygen -l -E md5 -f - | grep ECDSA | awk '{print $2}' | sed 's/MD5://g'
done
```

This will output something like:

```
raspie.lan
4a:32:2d:09:8a:7e:03:4c:d9:ab:95:a3:c0:cd:2a:56
expressionist.lan
ab:44:42:95:12:53:d2:8f:f8:99:fa:e9:f7:3e:35:27
```

The fingerprints output by this script can be used to validate hosts connected to using the Conch framework.
Typically this verification is done in function 'verifyHostKey' in the SSHClientTransport implementation.

# Creating Certificates

The client needs to authenticate itself to the server using a certificate. The Twisted/Conch
has a convenience script 'ckeygen' to create a certificate specifically to be used for one application:

```$bash    
ckeygen -C 'sshclient key' -b 2048 -t rsa --no-passphrase -f ~/.ssh/sshclient_rsa
```

This will create '~/.ssh/sshclient_rsa' and '~/.ssh/sshclient_rsa.pub'. The public key needs to 
be installed in the hosts where we connect to. Both keys need to be provided by
the SSHUserAuthClient implementation.

# Starting the SSH Client module






