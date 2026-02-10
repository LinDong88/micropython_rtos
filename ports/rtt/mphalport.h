#include <rtthread.h>
#include <drivers/pin.h>

#define MP_HAL_PIN_FMT                 "%s"

extern void mp_hal_set_interrupt_char (int c);
extern void mp_pin_od_write(void *machine_pin, int stat);
extern void mp_hal_pin_open_set(void *machine_pin, int mode);
extern void mp_hal_stdout_tx_strn_stream(const char *str, size_t len);

#define mp_hal_quiet_timing_enter()         MICROPY_BEGIN_ATOMIC_SECTION()
#define mp_hal_quiet_timing_exit(irq_state) MICROPY_END_ATOMIC_SECTION(irq_state)


/*
static inline mp_uint_t mp_hal_ticks_ms(void) {
    return 0;
}
static inline void mp_hal_set_interrupt_char(char c) {
}
*/