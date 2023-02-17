#!/usr/bin/env python
"""JMX metric exporter"""


from flask import Flask, request, make_response
from jmxquery import JMXConnection, JMXQuery, MetricType
import logging

class JmxMetrics:

	def __init__(self, target="", metric_query='java.lang:*', query_timeout=50):
		self.target = target
		self.uri = "service:jmx:rmi:///jndi/rmi://" + target + "/jmxrmi"
		self.metric_query = metric_query
		self.query_timeout = query_timeout
		self.metrics = "#JMX Exporter metrics \n"
		self.allowed_types = ['Long','Integer','Boolean']

	def fetch_metrics(self):
		jmxConnection = JMXConnection(self.uri)
		jmxQuery = [JMXQuery(self.metric_query)]
		try:
			metrics = jmxConnection.query(jmxQuery,timeout=self.query_timeout)
			for metric in metrics:
				if metric.value_type not in self.allowed_types:
					continue
				if metric.value_type == 'Boolean':
					metric.value = int(metric.value)
				metric_name = metric.to_query_string().replace(".","").replace("name=","").replace("type=","").replace(" ","_").replace(":","_").replace("/","_").replace(",","_").replace("'","").lower()
				app.logger.info("Metric Name: {}, Metric value: {}".format(metric_name, metric.value))
				self.metrics += '%s{target="%s"} %s\n' % (metric_name, self.target, metric.value)
			response = make_response(self.metrics, 200)
			response.mimetype = "text/plain"
			return response
		except:
			response = make_response("Error in fetching metrics", 403)
			response.mimetype = "text/plain"
			return response

logging.getLogger().setLevel(logging.DEBUG)
app = Flask(__name__)

@app.route('/healthz')
def show_health():
	response = make_response("Health: OK", 200)
	response.mimetype = "text/plain"
	return response

@app.route('/metrics')
def show_metrics():
	target = request.args.get('target', default = '', type = str)
	metric_query = request.args.get('query', default = 'java.lang:*', type = str)
	query_timeout = request.args.get('timeout', default = 50, type = int)
	jmx = JmxMetrics(target,metric_query,query_timeout)
	response = jmx.fetch_metrics()
	return response
