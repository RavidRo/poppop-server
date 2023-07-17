chown -vR $USER_ID:$GROUP_ID /opt/mcserver/worlds
chown -vR $USER_ID:$GROUP_ID /opt/mcserver/logs

exec gosu $DOCKER_USER:$DOCKER_GROUP make start