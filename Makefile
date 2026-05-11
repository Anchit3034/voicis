CC=gcc
CFLAGS=-shared -fPIC
LIBS=-lasound -lpthread

all:
	$(CC) $(CFLAGS) voice_segmenter.c -o libsegmenter.so $(LIBS)

clean:
	rm -f *.so *.wav
