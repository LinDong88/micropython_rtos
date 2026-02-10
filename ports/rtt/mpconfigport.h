#include <stdint.h>
#include <stdbool.h>

#define MICROPY_PY_MACHINE 1
#define MICROPY_PY_PIN 1
#define MICROPY_MODULE_BUILTIN_INIT 1
#define MICROPY_PY_GC 1
#define MICROPY_KBD_EXCEPTION 1
#define MICROPY_PY_RTTHREAD 1
#define MICROPY_PY_MODUOS 1

#define MICROPY_PY_BUILTINS_HELP    (1)
#define MICROPY_PY_BUILTINS_HELP_TEXT rtthread_help_text
#define MICROPY_PY_BUILTINS_HELP_MODULES (1)


#if MICROPY_PY_THREAD
#define MICROPY_EVENT_POLL_HOOK \
    do { \
        extern void mp_handle_pending(bool); \
        mp_handle_pending(true); \
        MP_THREAD_GIL_EXIT(); \
        MP_THREAD_GIL_ENTER(); \
    } while (0);
#else
#define MICROPY_EVENT_POLL_HOOK \
    do { \
        extern void mp_handle_pending(bool); \
        mp_handle_pending(true); \
        rt_thread_delay(1); \
    } while (0);
#endif

// options to control how MicroPython is built

// Use the minimal starting configuration (disables all optional features).
#define MICROPY_CONFIG_ROM_LEVEL (MICROPY_CONFIG_ROM_LEVEL_MINIMUM)

// You can disable the built-in MicroPython compiler by setting the following
// config option to 0.  If you do this then you won't get a REPL prompt, but you
// will still be able to execute pre-compiled scripts, compiled with mpy-cross.
#define MICROPY_ENABLE_COMPILER     (1)

#define MICROPY_REPL_EVENT_DRIVEN (0)
#define MP_ENDIANNESS_LITTLE (1) 
#define MICROPY_NLR_SETJMP (1)
#define MP_UNREACHABLE for (;;);
#define MICROPY_USE_INTERNAL_ERRNO (1)

//#define MICROPY_QSTR_EXTRA_POOL           mp_qstr_frozen_const_pool
#define MICROPY_ENABLE_GC                 (1)
#define MICROPY_HELPER_REPL               (1)
#define MICROPY_MODULE_FROZEN_MPY         (0)
#define MICROPY_ENABLE_EXTERNAL_IMPORT    (1)

#define MICROPY_ALLOC_PATH_MAX            (256)
#define MICROPY_ALLOC_PARSE_CHUNK_INIT    (16)

// type definitions for the specific machine

typedef intptr_t mp_int_t; // must be pointer size
typedef uintptr_t mp_uint_t; // must be pointer size
typedef long mp_off_t;

// We need to provide a declaration/definition of alloca()
// #include <alloca.h>  //change

#define MICROPY_HW_BOARD_NAME "RTT"
#define MICROPY_HW_MCU_NAME "D133"

#define MICROPY_HEAP_SIZE      (2048) // heap size 2 kilobytes


#define MP_STATE_PORT MP_STATE_VM

#define MP_RTT_NOT_IMPL_PRINT mp_printf(&mp_plat_print, "Not implement on %s:%ld, Please add for your board!\n", __FILE__, __LINE__)






