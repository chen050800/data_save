#!/bin/bash

# 请先输入您的相关参数，不要输入错误了！
  EXTIF="eth1"              # 这个是可以连上 Public IP 的网路介面
  INIF="eth0"               # 内部 LAN 的连接介面；若无请填 ""
  INNET="60.60.0.0/16"    # 内部 LAN 的网域，若没有内部 LAN 请设定为 ""
  export EXTIF INIF INNET

# 第一部份，针对本机的防火墙设定！###########################
# 1. 先设定好核心的网路功能：
  echo "1" > /proc/sys/net/ipv4/tcp_syncookies
  echo "1" > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts
  for i in /proc/sys/net/ipv4/conf/*/rp_filter; do
        echo "1" > $i
  done
  for i in /proc/sys/net/ipv4/conf/*/log_martians; do
        echo "1" > $i
  done
  for i in /proc/sys/net/ipv4/conf/*/accept_source_route; do
        echo "0" > $i
  done
  for i in /proc/sys/net/ipv4/conf/*/accept_redirects; do
        echo "0" > $i
  done
  for i in /proc/sys/net/ipv4/conf/*/send_redirects; do
        echo "0" > $i
  done

# 2. 清除规则、设定预设政策及开放 lo 与相关的设定值
  PATH=/sbin:/usr/sbin:/bin:/usr/bin; export PATH
  iptables -F
  iptables -X
  iptables -Z
  iptables -P INPUT   ACCEPT
  iptables -P OUTPUT  ACCEPT
  iptables -P FORWARD ACCEPT
  iptables -A INPUT -i lo -j ACCEPT
  iptables -A INPUT -m state --state RELATED -j ACCEPT

# 3. 启动额外的防火墙 script 模组
  if [ -f /usr/local/virus/iptables/iptables.deny ]; then
        sh /usr/local/virus/iptables/iptables.deny
  fi
  if [ -f /usr/local/virus/iptables/iptables.allow ]; then
        sh /usr/local/virus/iptables/iptables.allow
  fi
  if [ -f /usr/local/virus/httpd-err/iptables.http ]; then
        sh /usr/local/virus/httpd-err/iptables.http
  fi
  iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT

# 4. 允许某些类型的 ICMP 封包进入
  AICMP="0 3 3/4 4 11 12 14 16 18"
  for tyicmp in $AICMP
  do
     iptables -A INPUT -i $EXTIF -p icmp --icmp-type $tyicmp -j ACCEPT
  done

# 5. 允许某些服务的进入，请依照您自己的环境开启
iptables -A INPUT -p TCP -i $EXTIF --dport  22  -j ACCEPT   # SSH
iptables -A INPUT -p TCP -i $EXTIF --dport  25  -j ACCEPT   # SMTP
iptables -A INPUT -p UDP -i $EXTIF --sport  53  -j ACCEPT   # DNS
iptables -A INPUT -p TCP -i $EXTIF --sport  53  -j ACCEPT   # DNS
iptables -A INPUT -p TCP -i $EXTIF --dport  80  -j ACCEPT   # WWW
iptables -A INPUT -p TCP -i $EXTIF --dport 110  -j ACCEPT   # POP3
iptables -A INPUT -p TCP -i $EXTIF --dport 443  -j ACCEPT   # HTTPS
iptables -A INPUT -p TCP -i $EXTIF --dport 3690  -j ACCEPT   # svn
iptables -A INPUT -p TCP -i $EXTIF --dport 3306  -j ACCEPT    #mysql
# 第二部份，针对后端主机的防火墙设定！##############################
# 1. 先载入一些有用的模组
  modules="ip_tables iptable_nat ip_nat_ftp ip_nat_irc ip_conntrack 
ip_conntrack_ftp ip_conntrack_irc"
  for mod in $modules
  do
        testmod=`lsmod | grep "${mod} "`
        if [ "$testmod" == "" ]; then
                modprobe $mod
        fi
  done

# 2. 清除 NAT table 的规则吧！
  iptables -F -t nat
  iptables -X -t nat
  iptables -Z -t nat
  iptables -t nat -P PREROUTING  ACCEPT
  iptables -t nat -P POSTROUTING ACCEPT
  iptables -t nat -P OUTPUT      ACCEPT

# 3. 开放成为路由器，且为 IP 分享器！
  if [ "$INIF" != "" ]; then
    iptables -A INPUT -i $INIF -j ACCEPT
    echo "1" > /proc/sys/net/ipv4/ip_forward
    if [ "$INNET" != "" ]; then
      for innet in $INNET
      do
        iptables -t nat -A POSTROUTING -s $innet -o $EXTIF -j SNAT --to 192.168.84.206 #vpc client de ip
      done
    fi
  fi
  # 如果你的 MSN 一直无法连线，或者是某些网站 OK 某些网站不 OK，
  # 可能是 MTU 的问题，那你可以将底下这一行给他取消注解来启动 MTU 限制范围
  # iptables -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -m tcpmss \
  #          --mss 1400:1536 -j TCPMSS --clamp-mss-to-pmtu

# 4. 内部伺服器的设定：
# iptables -t nat -A PREROUTING -p tcp -i $EXTIF --dport 80  \
#          -j DNAT --to 192.168.1.210:80
#iptables -t nat -A POSTROUTING -s $innet -o $EXTIF -j MASQUERADE
