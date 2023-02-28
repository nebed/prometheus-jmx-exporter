#!/usr/bin/env python
"""JMX metric exporter"""


from flask import Flask, request, make_response
from jmxquery import JMXConnection, JMXQuery, MetricType
from json import loads
import logging

class JmxMetrics:

	def __init__(self, target="", metric_query='java.lang:*', query_timeout=50, metric_labels=None):
		self.target = target
		self.uri = "service:jmx:rmi:///jndi/rmi://" + target + "/jmxrmi"
		self.metric_query = metric_query
		self.metric_prefix = metric_query.split(":")[0].replace(".","_")
		self.query_timeout = query_timeout
		self.metric_labels = metric_labels
		self.metrics = "#JMX Exporter metrics \n"
		self.allowed_types = ['Long','Integer','Boolean']

	def fetch_metrics(self):
		jmxConnection = JMXConnection(self.uri)
		jmxQuery = [JMXQuery(self.metric_query, metric_name=self.metric_prefix+"_{type}_{name}_{attribute}_{attributeKey}", metric_labels=self.metric_labels)]
		try:
			metrics = jmxConnection.query(jmxQuery,timeout=self.query_timeout)
			for metric in metrics:
				if metric.value_type not in self.allowed_types:
					continue
				if metric.value_type == 'Boolean':
					metric.value = int(metric.value)
				metric.metric_name = metric.metric_name.replace("_{name}","").replace("_{attributeKey}","").replace("_{attribute}","")
				app.logger.info("Metric Name: {}, Metric labels: {}, Metric value: {}".format(metric.metric_name, metric.metric_labels, metric.value))
				metric.metric_labels.update(target=self.target)
				self.metrics += '%s{%s} %s\n' % (metric.metric_name, "".join(str(key) + "=" + str(value) + "," for key, value in metric.metric_labels.items()), metric.value)
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
	metric_labels = request.args.get('labels', default = None, type = str)
	if metric_labels != None:
		metric_labels = loads(metric_labels)
	jmx = JmxMetrics(target,metric_query,query_timeout,metric_labels)
	response = jmx.fetch_metrics()
	return response
