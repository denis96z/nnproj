FROM golang:1.14.4 as base
WORKDIR /tmp/nnproj-backend-mock
COPY . .
RUN go build -o mock .

FROM ubuntu:20.04
WORKDIR /usr/local/bin
COPY --from=base /tmp/nnproj-backend-mock/data ./data
COPY --from=base /tmp/nnproj-backend-mock/mock ./mock
CMD ["/usr/local/bin/mock", "0.0.0.0:80", "./data"]
