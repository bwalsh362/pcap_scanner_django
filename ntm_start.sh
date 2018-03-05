#!/bin/bash
WORKING_DIR="/root/PycharmProjects/pcap_scanner_django/"
SNMP_COMM="capstone-ro"
SNMP_PORT=161
WEB_IP_PORT="127.0.0.1:8000"
VIRTUAL_ENV="venv/bin/activate"
RUN_SERVER="manage.py"
SNMP_APP="snmp_manager.py"
WAIT_TIME=30
WAIT_CYCLE=30

echo "Starting mongod service..."
if service --status-all | grep -Fq 'mongod'; then
    service mongod start
else
    echo "NOT INSTALLED"
fi
echo "Mongod service started"
source "$WORKING_DIR$VIRTUAL_ENV"
nohup python "$WORKING_DIR$RUN_SERVER" runserver $WEB_IP_PORT &

while true
do 

python "$WORKING_DIR$SNMP_APP" $SNMP_PORT $SNMP_COMM $WAIT_TIME False

sleep $WAIT_TIME

python "$WORKING_DIR$SNMP_APP" $SNMP_PORT $SNMP_COMM $WAIT_TIME True

sleep $WAIT_CYCLE

done

