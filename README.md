# csv-to-yaml - Prometheus config

take CSV file with something like following headers:

Configuration Item Name,Location,Country,Domain,Status,Secret Server URL,Hostnames,FQDN,IP Address,Application Ports,Exporter_name,Done,OS-Listen-Port,Exporter_name,Done,App-Listen-Port,http_2xx,icmp,ssh-banner,tcp-connect,SNMP,Exporter_SSL,Notes,Description,Story #,Completed,Review comments,MaaS alarm,Resolution

and convert to yaml for prometheus configs

exporter_blackbox
exporter_windows
exporter_linux
