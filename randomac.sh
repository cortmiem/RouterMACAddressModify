#!/bin/bash
logger -p notice -t randomac "🟢🟢🟢🟢 DAEMON STARTED 🟢🟢🟢🟢";
while true
do
	ip=`ubus call network.interface.wan status | grep \"address\" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | wc -c;`
	if [ $ip -lt 7 ];
	then 
		logger -p notice -t randomac "🔴🔴🔴🔴 NETWORK DROP 🔴🔴🔴🔴";
		sleep 5;
		macpos=`echo $RANDOM|md5sum|sed 's/../&:/g'|cut -c 1-5;`;
		mac="34:2a:2d:8e:"$macpos"";
		uci set network.cfg070f15.macaddr=$mac;
		uci commit;
		logger -p notice -t randomac "new macaddr: $mac";
		sleep 60;
	fi;
	sleep 10;
done;