# Refrences
# https://github.com/mtoensing/Docker-Minecraft-PaperMC-Server
# https://github.com/Phyremaster/papermc-docker

FROM eclipse-temurin:20-jre

RUN apt-get update \
	&& apt-get install -y make \
	&& apt-get install -y screen \
	&& rm -rf /var/lib/apt/lists/* 

COPY . /opt/server
WORKDIR /opt/server

EXPOSE 25565

ENTRYPOINT make start