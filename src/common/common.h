/* A file containing the compatibility differences between compilers. */
#pragma once

/* Allow use of inline in this file, even if it is not valid. */
#ifndef __STDC_VERSION__
    /* NOTE: the user should not use either of these words */
    #define inline
    #define restrict
#endif

/** A check for function returns.*/
#define RETURN_IF_ERROR(cond_, err_) do { \
    int _err = 0; /* err_ cannot be '_err'. */ \
    /* We cannot use strerror((err_)) because if err_ is an invalid errno, */ \
    /* then strerror may return NULL or may set errno. */ \
    if ((_err = (cond_))) { \
        const int old_errno = errno; \
        errno = 0; /* Reset errno */ \
        /* We use this function so we do not need to include stdio.h. */ \
        _err = print_stderr("[ERROR] %s:%d: err_ = %d: \"%s\"\n" \
                           "\tcond_ = \"%s\" = %d\n", \
                           __FILE__, __LINE__, (err_), _safe_strerror((err_)), \
                           #cond_, _err); \
        assert(_err == 0 && "failed to print error message to stderr"); \
        errno = old_errno; \
        return (err_); \
    } \
} while (0)

const char *_safe_strerror(const int errnum);

int print_stderr(const char *const restrict format, ...);