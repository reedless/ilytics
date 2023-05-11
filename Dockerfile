FROM nvidia/cuda:10.0-cudnn7-devel AS builder

WORKDIR /src

COPY . .

run  make

FROM nvidia/cuda:10.0-cudnn7-runtime

WORKDIR /src

COPY . .
COPY --from=builder /src/libdarknet.so .
COPY ./aimodel/*.weights backup/yolo-obj_best.weights
COPY ./aimodel/*.cfg yolo-obj.cfg
COPY ./aimodel/*.names data/obj.names
COPY ./aimodel/*.data data/obj.data

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN rm -rf /var/cache/apt/archives/*
RUN apt-get update && \
                apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools
RUN apt install -y libsm6 libxext6 libxrender-dev &&\
        rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip --no-cache-dir
RUN pip3 install gunicorn --no-cache-dir
RUN pip3 install setuptools wheel virtualenv awscli --upgrade --no-cache-dir
RUN pip3 install -U scikit-image --no-cache-dir
RUN pip3 install -r requirements.txt --no-cache-dir
RUN chmod +x run.sh

EXPOSE 8080

CMD ["./run.sh"]




