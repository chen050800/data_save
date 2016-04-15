import pexpect
import sys
import time
host = sys.argv[1]
ssh_newkey = 'Are you sure you want to continue connecting'
p = pexpect.spawn('ssh -l administrator '+host, timeout=1)
p.linesep="\r\n"
#p.logfile = sys.stdout
i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    print "I say yes"
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    print "I give password",
    p.sendline("guobinwsx@165")
elif i==2:
    print "I either got key or connection timeout"
    pass

p.expect(['Windows\\\\system32'])
p.sendline('net user')
time.sleep(5)


p.expect(["Admin"])
p.expect(["system32"])
print p.before, p.after


print "BUFFER:"
print p.buffer


#p.sendline('neteye123')
#p.interact()

