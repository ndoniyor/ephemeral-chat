FROM envoyproxy/envoy:v1.29-latest
COPY ./envoy.yaml /etc/envoy/envoy.yaml
CMD ["/usr/local/bin/envoy", "-c", "/etc/envoy/envoy.yaml",  "--log-level", "debug"]