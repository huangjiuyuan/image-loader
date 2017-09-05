FROM docker
RUN apk add --no-cache python
RUN git clone https://github.com/huangjiuyuan/image_loader.git
WORKDIR image_loader
CMD ['./upload -h']
