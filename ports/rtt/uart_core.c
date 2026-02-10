#if 0
#include <unistd.h>
#include "py/mpconfig.h"
#include "rtthread.h"
//#include "E:\RK1808\luban-lite-master\packages\third-party\micropython\ports\nrf\drivers\bluetooth\ringbuffer.h"
#include <kernel\rt-thread\components\drivers\include\ipc\ringbuffer.h>

#include "interrupt_char.h"

#define UART_FIFO_SIZE 256
static struct rt_ringbuffer *rx_fifo = NULL;
static rt_err_t (*odev_rx_ind)(rt_device_t dev, rt_size_t size) = NULL;


static rt_err_t getchar_rx_ind(rt_device_t dev, rt_size_t size) {
    uint8_t ch;
    rt_size_t i;
    rt_base_t int_lvl;

    for (i = 0; i < size; i++) {
        /* read a char */
        if (rt_device_read(dev, 0, &ch, 1))
         {
            // if (ch == mp_interrupt_char) {
            //     mp_keyboard_interrupt();
            // } else {
                int_lvl = rt_hw_interrupt_disable();
                rt_ringbuffer_put_force(rx_fifo, &ch, 1);
                rt_hw_interrupt_enable(int_lvl);
            // }
        }
    }
    return RT_EOK;
}

void mp_getchar_init(void) {
    rt_base_t int_lvl;
    rt_device_t console;

    /* create RX FIFO */
    rx_fifo = rt_ringbuffer_create(UART_FIFO_SIZE);
    /* created must success */
    RT_ASSERT(rx_fifo);

    int_lvl = rt_hw_interrupt_disable();
    console = rt_console_get_device();
    if (console) {
        /* backup RX indicate */
        odev_rx_ind = console->rx_indicate;
        rt_device_set_rx_indicate(console, getchar_rx_ind);
    }
    rt_hw_interrupt_enable(int_lvl);

}
void mp_getchar_deinit(void) {
    rt_base_t int_lvl;
    rt_device_t console;

    rt_ringbuffer_destroy(rx_fifo);

    int_lvl = rt_hw_interrupt_disable();
    console = rt_console_get_device();
    if (console && odev_rx_ind) {
        /* restore RX indicate */
        rt_device_set_rx_indicate(console, odev_rx_ind);
    }
    rt_hw_interrupt_enable(int_lvl);
}
int mp_getchar(void) {
    uint8_t ch;
    rt_base_t int_lvl;

    int_lvl = rt_hw_interrupt_disable();
    if (!rt_ringbuffer_getchar(rx_fifo, &ch)) {
        ch = 0xFF;
    }
    rt_hw_interrupt_enable(int_lvl);

    return ch;

}

// Receive single character
int mp_hal_stdin_rx_chr(void) {
    char ch;
    while (1) {
        ch = mp_getchar();
        if (ch != (char)0xFF) {
            break;
        }
        MICROPY_EVENT_POLL_HOOK;
        rt_thread_delay(1);
    }
    return ch;
}

/*-------------------------------------------------------------------------------*/

// void mp_hal_stdout_tx_strn_stream(const char *str, size_t len) {
//     mp_putsn_stream(str, len);
// #ifdef PKG_USING_OPENMV_CP
//     extern void serial_dbg_send_strn_cooked(const char *str, int len);
//     serial_dbg_send_strn_cooked(str, len);
// #endif
// }

static rt_device_t console_dev = NULL;
static struct rt_device dummy_console = { 0 };
static rt_uint16_t console_open_flag;

void mp_putsn(const char *str, size_t len) {
    if (console_dev) {
        rt_device_write(console_dev, 0, str, len);
    }
}


void mp_putsn_init(void) {
    {/* register dummy console device */
#ifdef RT_USING_DEVICE_OPS
        static struct rt_device_ops _ops = {0};
        dummy_console.ops = &_ops;
#endif

        dummy_console.type = RT_Device_Class_Char;
        rt_device_register(&dummy_console, "dummy", RT_DEVICE_FLAG_RDWR);
    }

    /* backup the console device */
    console_dev = rt_console_get_device();
    console_open_flag = console_dev->open_flag;
    console_dev->open_flag = 0;

    /* set the new console device to dummy console */
    rt_console_set_device(dummy_console.parent.name);
    /* reopen the old console device for mp_putsn */
    rt_device_close(console_dev);
    rt_device_open(console_dev, RT_DEVICE_OFLAG_RDWR | RT_DEVICE_FLAG_INT_RX);
}

void mp_putsn_deinit(void) {
    /* close the old console, it's already in mp_putsn_init */
    rt_device_close(console_dev);
    /* restore the old console device */
    rt_console_set_device(console_dev->parent.name);
    console_dev->open_flag = console_open_flag;

    rt_device_unregister(&dummy_console);
}


// Send string of given length

void mp_hal_stdout_tx_strn(const char *str, mp_uint_t len) {
    mp_putsn(str, len);
    // rt_kprintf(str,len);
#ifdef PKG_USING_OPENMV_CP
    extern void serial_dbg_send_strn(const char *str, int len);
    serial_dbg_send_strn(str, len);
#endif
}

#endif