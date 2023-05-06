WORLD_NAME := poppop
INITIAL_MEMORY := 1G
MAX_MEMORY := 2G

RUN_CMD := java -Xmx$(MAX_MEMORY) -Xms$(INITIAL_MEMORY) -jar server.jar --universe ./worlds

start:
	$(RUN_CMD) --nogui --world $(WORLD_NAME)

start-gui:
	$(RUN_CMD) --world $(WORLD_NAME)

test:
	$(RUN_CMD) --nogui --world test_world

help:
	$(RUN_CMD) --help

# Command for removing from git without deleting file:
# git rm --cached <file>