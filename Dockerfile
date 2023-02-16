FROM alpine:3.17

RUN mkdir -p /opt/service

WORKDIR /opt/service

COPY requirements.txt .

RUN apk add --no-cache git gcc python3-dev py3-pip musl-dev linux-headers openjdk11-jre \
	&& pip install --no-cache-dir -r requirements.txt \
	&& find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' + \
	&& rm requirements.txt \
	&& rm -rf dep

COPY bin bin

CMD ["python", "/opt/service/bin/pywsgi.py"]