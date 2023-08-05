# Refrences
# https://github.com/mtoensing/Docker-Minecraft-PaperMC-Server
# https://github.com/Phyremaster/papermc-docker

FROM eclipse-temurin:20-jre

RUN apt-get update \
	&& apt-get install -y make \
	&& apt-get install -y gosu \
	&& rm -rf /var/lib/apt/lists/* 


ENV USER_ID=1000
ENV GROUP_ID=1000
ENV DOCKER_USER=dockeruser
ENV DOCKER_GROUP=dockergroup

RUN addgroup --gid 1000 dockergroup
RUN adduser dockeruser \
	--shell /bin/sh \
	--ingroup dockergroup \
	--disabled-password \
	--home /home/dockeruser \
	--uid 1000 \
	--gecos ""


COPY --chown=dockeruser:dockergroup ./mcserver /opt/mcserver
WORKDIR /opt/mcserver

EXPOSE 25565
CMD ./run_as_user.sh