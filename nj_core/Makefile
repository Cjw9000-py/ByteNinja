# This makefile is for debug builds on linux only

SOURCE_EXT=.cxx
EXE_EXT=.elf

INCLUDE= -I include/ 
CCFLAGS= -g -O0 $(INCLUDE)
LDFLAGS= -lm

CC=g++ $(CCFLAGS)
LD=g++ $(LDFLAGS)

TEST_DIR=tests
SRC_DIR=src
OUTPUT=build
TEST_OUTPUT=$(OUTPUT)/tests

SOURCES=$(wildcard $(SRC_DIR)/*$(SOURCE_EXT))
OBJECTS=$(patsubst $(SRC_DIR)/%$(SOURCE_EXT),$(OUTPUT)/%.o,$(SOURCES))

TEST_SOURCES=$(wildcard $(TEST_DIR)/*$(SOURCE_EXT))
TEST_OUTPUTS=$(patsubst $(TEST_DIR)/test%$(SOURCE_EXT),$(TEST_OUTPUT)/test%$(EXE_EXT),$(TEST_SOURCES))

$(OUTPUT)/%.o: $(SRC_DIR)/%$(SOURCE_EXT) $(OUTPUT)
	$(CC) -c $< -o $@

$(TEST_OUTPUT)/test%$(EXE_EXT): $(TEST_DIR)/test%$(SOURCE_EXT) $(OUTPUT) $(OBJECTS)
	$(CC) $< $(OBJECTS) -o $@ $(LDFLAGS) 

$(OUTPUT):
	mkdir -p $(OUTPUT)
	mkdir -p $(TEST_OUTPUT)

all: $(OBJECTS) $(TEST_OUTPUTS)
	echo $(TEST_SOURCES)
clean:
	rm -r $(OUTPUT)

.PHONY: all clean