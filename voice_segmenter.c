#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>

#define CHUNK_SIZE 480
#define SAMPLE_RATE 16000

snd_pcm_t *capture_handle;

void init_audio() {

    int err;

    err = snd_pcm_open(
        &capture_handle,
        "default",
        SND_PCM_STREAM_CAPTURE,
        0
    );

    if (err < 0) {
        fprintf(stderr, "Mic open failed\n");
        exit(1);
    }

    err = snd_pcm_set_params(
        capture_handle,
        SND_PCM_FORMAT_S16_LE,
        SND_PCM_ACCESS_RW_INTERLEAVED,
        1,
        SAMPLE_RATE,
        1,
        500000
    );

    if (err < 0) {
        fprintf(stderr, "Mic config failed\n");
        exit(1);
    }
}

int read_audio(short *buffer) {

    int frames = snd_pcm_readi(
        capture_handle,
        buffer,
        CHUNK_SIZE
    );

    if (frames < 0) {

        snd_pcm_prepare(capture_handle);

        return 0;
    }

    return frames;
}
