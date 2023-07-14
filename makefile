WORLD_NAME := poppop
INITIAL_MEMORY := 10G
MAX_MEMORY := 10G
MEMOMRY_FLAGS := -Xms$(INITIAL_MEMORY) -Xmx$(MAX_MEMORY)

RUN_CMD := java $(MEMOMRY_FLAGS) \
	-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \
	-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \
	-XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M \
	-XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \
	-XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 \
	-XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem \
	-XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true \
	-jar server.jar --universe ./worlds

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