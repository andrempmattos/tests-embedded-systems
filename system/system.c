/*
 * system.c
 * 
 * Copyright (C) 2020, SpaceLab.
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
 * \brief System management routines implementation.
 * 
 * \author Gabriel Mariano Marcelino <gabriel.mm8@gmail.com>
 * 
 * \version 0.5.1
 * 
 * \date 29/01/2020
 * 
 * \addtogroup system
 * \{
 */

#include <msp430.h>

#include "system.h"

sys_time_t sys_time = 0;

void system_reset(void)
{
    PMMCTL0 = PMMPW | PMMSWBOR;     /* Triggers a software BOR */

    WDTCTL = 0xDEAD;                /* Reset system by writing to the WDT register without using the proper password */
}

uint8_t system_get_reset_cause(void)
{
    return (SYSRSTIV & 0xFF);
}

void system_set_time(sys_time_t tm)
{
    sys_time = tm;
}

void system_increment_time(void)
{
    sys_time++;
}

sys_time_t system_get_time(void)
{
    return sys_time;
}

/** \} End of system group */
