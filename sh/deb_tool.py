# -*- coding:utf8 -*- 
'''
Created on 2012-5-9
向smtp服务器上发送相应的邮件。


@author: chen
'''
import sys
import os
from subprocess import Popen, PIPE

from optparse import OptionParser

def main():
    parser = OptionParser(usage="""\
this tool use dpkg command to process *.deb
it's used in linux system

Usage: python %prog [options] 

""")
    parser.add_option('-x', '--extract',
                      action='store_true',
                    dest='extract',
                      help="""pthon %prog -x -d *.deb 
                              the actions are: mkdir tmp && cd tmp && dpkg  -X ../*.deb . && dpkg -e ../*.deb && cd ..""")
    parser.add_option('-d', '--deb', type='string',
                      action='store',
                    dest='deb',
                      help="""
                      the name of deb which be extracted
                      """)


    parser.add_option('-c', '--compress',
                      action='store_true',
                    dest='compress',
                      help="""python %prog -c -n dir_name
                              it will read the content of  dir_name/DEBIAN/control,
                              and look for the package_name and the package_version
                              the arctions are:
                              dpkg -b dir_name package_name_package_version_i386.deb
                              """)

    parser.add_option('-n', '--dir_name',
                      type='string', action='store', 
                      default='', dest='dir_name',
                      help='the dir name which should be compressed')    

    parser.add_option('-f', '--find_depends',
                      type='string', action='store', 
                      default='', dest='find_depends',
                      help= ''' find  the debs which is used by   the bin of file  
                              python %prog -f /usr/local/bin/test
                              ''')    

##发件人的用户名和密码
#    parser.add_option('-n', '--package_name',
#                      type='string', action='store', 
#                      default='', dest='package_name',
#                      help='package name for the deb')
#    parser.add_option('-v', '--package_version',
#                      type='string', action='store', 
#                      default='', dest='package_version',
#                      help='package version for the deb')
  

    opts, args = parser.parse_args()
#    print opts, args
    if not (opts.extract and opts.deb) and not (opts.compress and opts.dir_name) and not opts.find_depends:
        parser.print_help()
        sys.exit(1)

    if opts.extract:
        deb = opts.deb
        path_deb = os.path.abspath(deb)
        cmd_list1 = ['rm tmp -fr', 'mkdir tmp'] 
        cmd_list2 = [ 'dpkg -X '+path_deb+' .', 'dpkg -e '+path_deb]
        for cmd in cmd_list1:
            print cmd
            p = Popen(cmd, shell=True, stdout=PIPE).communicate()
        os.chdir('tmp')
        print 'cd tmp'
        
        for cmd in cmd_list2:
            print cmd
            p = Popen(cmd, shell=True, stdout=PIPE).communicate()        
        os.chdir('..')
        print 'cd ..'
        
    elif opts.compress: 
        dir_name = opts.dir_name   
        if not os.path.isfile(dir_name+'/DEBIAN/control'):
            print """Error: """+dir_name+"""'/DEBIAN/control' is not exsit"""
            sys.exit(1)
        f = open(dir_name+'/DEBIAN/control')
        for line in f.readlines():
            i = 0
            if line.startswith('Package:'):
                package_name = line[8:].strip()
                i +=1
                continue
            elif line.startswith('Version:'):
                package_version = line[8:].strip()
                i += 1
            if i == 2:
                break
        
        name = package_name
        version = package_version
        cmd_list = ['dpkg -b '+dir_name+' '+name+'_'+version+'_i386.deb']
        for cmd in cmd_list:
            print cmd
            p = Popen(cmd, shell=True, stdout=PIPE).communicate()
    elif opts.find_depends :
        cmd = "objdump -p "+opts.find_depends+"| grep NEEDED| cut -d D -f 3| xargs dpkg -S| cut -d ':' -f 1 | sort | uniq | xargs dpkg -l" 
        print cmd
        p = Popen(cmd, shell=True).communicate()

if __name__ == '__main__':
    main()
