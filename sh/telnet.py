import pexpect
import sys
host = sys.argv[1]
print 'host is ', host
child = pexpect.spawn('telnet -l root '+str(host))
child.logfile_read = sys.stdout
child.expect ('Password:')
child.sendline ('neteye')
child.expect('#')
#child.sendline('telnet 192.168.81.102 -l root')
#child.expect ('Password:')
#child.sendline ('neteye')
child.interact()
