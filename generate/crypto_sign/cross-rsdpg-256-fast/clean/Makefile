# This Makefile can be used with GNU Make or BSD Make

LIB = libcross-rsdpg-256-fast_clean.a

HEADERS = api.h CROSS.h csprng_hash.h fq_arith.h merkle_tree.h pack_unpack.h parameters.h restr_arith.h seedtree.h sha3.h set.h
OBJECTS = CROSS.o csprng_hash.o merkle.o pack_unpack.o seedtree.o sign.o
CFLAGS=-std=c99 -I../../../common $(EXTRAFLAGS) -march=native -O3 -g3 -std=c99 -Wpedantic -Werror -Wredundant-decls -Wmissing-prototypes -Wuninitialized -Wall -Wextra

all: $(LIB)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c -o $@ $<

$(LIB): $(OBJECTS)
	$(AR) -r $@ $(OBJECTS)

clean:
	$(RM) $(OBJECTS)
	$(RM) $(LIB)