import pexpect
import time

expect_str = ['system32']
ip = '172.160.200.235'
child = pexpect.spawn('ssh administrator@'+ip)
child.linesep = '\r\n'
try:
    i = child.expect(['[P|p]assword', 'continue connecting (yes/no)?'], timeout=5)
    if i == 0:
        child.sendline('guobinwsx@165')
    elif i ==1:
        child.sendline('yes\n')
        child.expect('[P|p]assword')
        child.sendline('guobinwsx@165')
except pexpect.EOF:
    print "EOF"
    child.close()
except pexpect.TIMEOUT:
    print "timeout"
    child.close()


child.expect(expect_str)
    # del usr before add
    # child.sendline('net user %s /del'%(ixia_user))
    # child.expect(expect_str)
    #
    # child.sendline('net user %s %s /add'%(ixia_user,ixia_pwd))
    # child.expect(expect_str)
    # child.sendline('net localgroup "Remote Desktop Users" test /add')
    # child.expect(expect_str)

child.sendline('net user')
time.sleep(5)
child.expect(expect_str)
print 'result:',child.before,'\nafter: ',child.after,'\nbuffer : ',child.buffer




