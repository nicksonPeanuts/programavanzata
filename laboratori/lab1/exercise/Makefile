CC = gcc
LIB_DIR = lib
STATIC = yes

# Impostazione CFLAGS e nomi libreria
ifeq "${STATIC}" "yes"
    CFLAGS = -O3 -Wall -pedantic -std=c17
    LIB_NAME = libbst.a
else
    CFLAGS = -fPIC -O3 -Wall -pedantic -std=c17
    LIB_NAME = libbst.so
endif

all: main

# Compilazione dell'eseguibile (linka la libreria in ./lib)
main: main.o $(LIB_DIR)/$(LIB_NAME)
	$(CC) $(CFLAGS) -o main main.o -L./$(LIB_DIR) -lbst

# Creazione della libreria STATICA
$(LIB_DIR)/libbst.a: bst.o
	@mkdir -p $(LIB_DIR)
	ar rcs $@ bst.o

# Creazione della libreria DINAMICA
$(LIB_DIR)/libbst.so: bst.o
	@mkdir -p $(LIB_DIR)
	$(CC) -shared -o $@ bst.o

# Compilazione dei file oggetto
main.o: main.c bst.h
	$(CC) $(CFLAGS) -c main.c

bst.o: bst.c bst.h node.h
	$(CC) $(CFLAGS) -c bst.c

.PHONY: clean
clean:
	rm -f *.o main $(LIB_DIR)/libbst.*
	rm -rf $(LIB_DIR)