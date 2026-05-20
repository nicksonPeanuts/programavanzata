CC = gcc
CFLAGS = -O3 -fopenmp
LIB = lib

all: tensorforth

tensorforth: main.o tensor.o stack.o ops.o
	${CC} ${CFLAGS} -o $@ $^ -L./${LIB}/ -lm

${LIB}:
	mkdir -p $@

main.o: main.c 
	${CC} ${CFLAGS} -c $<

%.o: %.c %.h
	${CC} ${CFLAGS} -c $<


.PHONY: clean clean-all
clean:
	rm -f *.o

clean-all: clean
	rm -rf ${LIB}
	rm -f tensorforth
