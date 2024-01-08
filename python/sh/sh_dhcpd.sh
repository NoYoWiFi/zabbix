#!/bin/sh
sed -i '17,$d' /etc/dhcp/dhcpd.conf
for i in `cat cfg_dhcpd.cfg`
do
  x=`echo $i | awk -F ',' '{print $2}'`
  y=`echo $i | awk -F ',' '{print $1}'`
  echo -e "host $x {">>/etc/dhcp/dhcpd.conf
  echo -e "  hardware ethernet $y;">>/etc/dhcp/dhcpd.conf
  echo -e "  fixed-address $x;">>/etc/dhcp/dhcpd.conf
  echo -e "}">>/etc/dhcp/dhcpd.conf
done
