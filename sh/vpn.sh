#!/bin/sh
service ipsec restart
sleep 2
ipsec whack --name roadwarrior --initiate
