
PYTHON_FLAGS= 
CYTHON_FLAGS= -3
CCFLAGS= -I /usr/include/python3.10 -Wall -g -fPIC
LDFLAGS= -lpython3 -ldl -lm -lcrypt


PYTHON=/usr/bin/python3 $(PYTHON_FLAGS)
CYTHON=$(PYTHON) -m cython $(CYTHON_FLAGS)
CC=gcc $(CCFLAGS)
LD=gcc $(LDFLAGS)

EXT_SUFFIX=cpython-310-x86_64-linux-gnu.so

SOURCE_DIR=byte_ninja/vm

SOURCES= $(wildcard $(SOURCE_DIR)/*.pyx)
CSOURCES= $(patsubst $(SOURCE_DIR)/%.pyx, $(SOURCE_DIR)/%.c, $(SOURCES))
CMODULES= $(patsubst $(SOURCE_DIR)/%.pyx, $(SOURCE_DIR)/%.$(EXT_SUFFIX), $(SOURCES))

all: $(CMODULES)

$(SOURCE_DIR)/%.c: $(SOURCE_DIR)/%.pyx
	$(CYTHON) $< --output-file=$@

$(SOURCE_DIR)/%.$(EXT_SUFFIX): $(SOURCE_DIR)/%.c
	$(CC) $(LDFLAGS) $< -o $@ -shared


clean:
	rm -f $(SOURCE_DIR)/*.$(EXT_SUFFIX) $(SOURCE_DIR)/*.c


.PHONY: clean all
