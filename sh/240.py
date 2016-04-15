import pexpect
import sys
#host = sys.argv[1]
ssh_newkey = 'Are you sure you want to continue connecting'
p = pexpect.spawn('ssh -l test 10.1.1.240')
i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    print "I say yes"
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    print "I give password",
    p.sendline("neteye123")
elif i==2:
    print "I either got key or connection timeout"
    pass
p.expect(['$'])
p.sendline('sudo bash')
p.expect(['for test'])
p.sendline('neteye123')
p.interact()

