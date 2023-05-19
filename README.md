# prometheus-jmx-exporter

Docker Container to connect to remote jmx and convert jmx metrics to prometheus metrics
Default port: 9000
Path: /metrics
possible parameters:
- target: jmx target and port in format host:port
- query: jmx query example - "java.lang:*"
- timeout: query timeout in seconds - default 50 


`Using jmxquery`

