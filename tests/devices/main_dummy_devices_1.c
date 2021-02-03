/*
 * main.c
 * 
 * Copyright (C) 2019, SpaceLab.
 * 
 * This file is part of OBDH 2.0.
 * 
 * OBDH 2.0 is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * OBDH 2.0 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with OBDH 2.0. If not, see <http://www.gnu.org/licenses/>.
 * 
 */

/**
 * \brief Main file.
 * 
 * \author Gabriel Mariano Marcelino <gabriel.mm8@gmail.com>
 * 
 * \version 0.1.0
 * 
 * \date 25/10/2019
 * 
 * \defgroup main Main file
 * \{
 */

/* 
 * Keep the compiler directives in THIS order to allow proper compilation.
 * The CI workflow python script reads and removes this #define when replacing 
 * the main.c file. This scheme avoid compilation errors by disabling this main().
 */
#define _MAIN_DUMMY_DEVICES_1_C_ 
#ifndef _MAIN_DUMMY_DEVICES_1_C_

#include "system/clocks.h"
#include "hal/gpio.h"
#include "system/sys_log/sys_log.h"
#include <msp430.h>

#define DUMMY_NAME    "MAIN"

void main(void)
{
    WDTCTL = WDTPW + WDTHOLD;             // Stop WDT
    
    /* System clocks and gpio configuration */
    clocks_setup((clocks_config_t){.mclk_hz = 32000000UL, .smclk_hz=32000000UL, .aclk_hz=32768});
    GPIO_setAsOutputPin(GPIO_PORT_P5, GPIO_PIN3);

    /* WARNING: This initial delay is required to properly complete de github actions workflow */
    int i;
    for(i = 0; i < 20; i++) {
        GPIO_toggleOutputOnPin(GPIO_PORT_P5, GPIO_PIN3);
        __delay_cycles(32000000UL);     // Delay 1 second
    }

    /* Logger device initialization */
    sys_log_init();

    /* Print the system clocks */
    clocks_config_t clks = clocks_read();
    sys_log_print_event_from_module(SYS_LOG_INFO, DUMMY_NAME, "System clocks: MCLK=");
    sys_log_print_uint(clks.mclk_hz);
    sys_log_print_msg(" Hz, SMCLK=");
    sys_log_print_uint(clks.smclk_hz);
    sys_log_print_msg(" Hz, ACLK=");
    sys_log_print_uint(clks.aclk_hz);
    sys_log_print_msg(" Hz");
    sys_log_new_line();

    sys_log_print_event_from_module(SYS_LOG_INFO, DUMMY_NAME, "Unit test devices dummy 1");
    sys_log_new_line();

    /* Log syntax for the automated verification through the UART port */
    sys_log_print_event_from_module(SYS_LOG_TEST, DUMMY_NAME, "Automated test passed!");
    //sys_log_print_event_from_module(SYS_LOG_TEST, DUMMY_NAME, "Automated test failed!");
    
    sys_log_new_line();

    /* Will only get here if there was insufficient memory to create the idle and/or timer task */
    while(1);
}

#endif /* _MAIN_DUMMY_DEVICES_1_C_ */

/** \} End of main group */
