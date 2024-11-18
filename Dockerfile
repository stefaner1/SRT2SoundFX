
FROM jrottenberg/ffmpeg:4.1-scratch as ffmpeg
FROM nikolaik/python-nodejs:python3.8-nodejs14-slim

WORKDIR /   
COPY --from=ffmpeg ./ /

# FIX packages
RUN rm  /etc/apt/sources.list.d/yarn.list


RUN	sed -i "s/main/main non-free/g" /etc/apt/sources.list
RUN	apt-get update 
RUN    apt-get full-upgrade -y && \
    apt-get install -y \
        libasound2 \
		libssl1.1 build-essential gcc


# Certificates install
RUN apt install -y ca-certificates --no-install-recommends && rm -rf /var/lib/apt/lists/*


ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt


