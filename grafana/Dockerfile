FROM amd64/alpine:latest

WORKDIR /opt/grafana

RUN apk update && apk upgrade
RUN apk --no-cache add curl

RUN curl -O -L "https://github.com/grafana/agent/releases/latest/download/grafana-agent-linux-amd64.zip" \
    && unzip "grafana-agent-linux-amd64.zip" \
    && rm "grafana-agent-linux-amd64.zip"

RUN chmod a+x grafana-agent-linux-amd64

COPY /grafana/agent-config.yaml .

RUN apk add --no-cache libc6-compat

ENTRYPOINT ["./grafana-agent-linux-amd64", "--config.file=agent-config.yaml"]
