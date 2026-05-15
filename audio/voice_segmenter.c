// ==========================================
// audio/voice_segmenter.c
// ==========================================

#include <pulse/simple.h>
#include <pulse/error.h>

#include <stdio.h>
#include <stdlib.h>

#include <signal.h>
#include <stdbool.h>

#define SAMPLE_RATE 16000
#define CHUNK_SIZE 480

pa_simple *stream = NULL;

volatile bool stop_recording = false;

// ==========================================
// SIGNAL HANDLER
// ==========================================

void handle_sigint(int sig) {

    stop_recording = true;
}

// ==========================================
// INIT AUDIO
// ==========================================

void init_audio() {

    signal(SIGINT, handle_sigint);

    static const pa_sample_spec ss = {
        .format = PA_SAMPLE_S16LE,
        .rate = SAMPLE_RATE,
        .channels = 1
    };

    int error;

    stream = pa_simple_new(
        NULL,
        "VoiceAI",
        PA_STREAM_RECORD,
        NULL,
        "record",
        &ss,
        NULL,
        NULL,
        &error
    );

    if (!stream) {

        fprintf(
            stderr,
            "PulseAudio init failed: %s\n",
            pa_strerror(error)
        );

        exit(1);
    }

    printf(
        "[PulseAudio] Microphone Ready\n"
    );
}

// ==========================================
// READ AUDIO
// ==========================================

int read_audio(short *buffer) {

    int error;

    if (
        pa_simple_read(
            stream,
            buffer,
            sizeof(short) * CHUNK_SIZE,
            &error
        ) < 0
    ) {

        fprintf(
            stderr,
            "PulseAudio read failed: %s\n",
            pa_strerror(error)
        );

        return 0;
    }

    return CHUNK_SIZE;
}

// ==========================================
// STOP CHECK
// ==========================================

int should_stop() {

    return stop_recording;
}

// ==========================================
// RESET FLAG
// ==========================================

void reset_stop_flag() {

    stop_recording = false;
}
