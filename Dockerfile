FROM docker
RUN apk update --no-cache
RUN apk add --no-cache python git
ENV GOPATH /go
RUN mkdir -p /go/src/k8s.io
WORKDIR /go/src/k8s.io
RUN git clone -b 'v1.6.5' --single-branch --depth 1 https://github.com/kubernetes/kubernetes.git
WORKDIR /
RUN git clone https://github.com/huangjiuyuan/image_loader.git
WORKDIR /image_loader
CMD ['./upload -h']
