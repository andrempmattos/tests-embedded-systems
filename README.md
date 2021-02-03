<h1 align="center">
	Tests for embedded systems
	<br>
</h1>

<h4 align="center">Automation tests experiment using a hybrid strategy of Continuos Integration (CI) and Hardware-In-the-Loop (HIL) concepts.</h4>

<p align="center">
	<a href="">
		<img src="https://img.shields.io/badge/status-in%20development-red?style=for-the-badge">
	</a>
	<a href="">
		<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/andrempmattos/tests-embedded-systems?style=for-the-badge">
	</a>
	<a href="">
		<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/andrempmattos/tests-embedded-systems?style=for-the-badge">
	</a>
	<a href="">
		<img alt="GitHub issues" src="https://img.shields.io/github/issues/andrempmattos/tests-embedded-systems?style=for-the-badge">
	</a>
</p>

<p align="center">
  	<a href="#overview">Overview</a> •
  	<a href="#workflows">Workflows</a> •
  	<a href="#workflows">Scripts</a> •
  	<a href="#workflows">Tests</a>
</p>

## Overview

This repository was intended to acts as a start point and experiment for implementing a workflow for [Spacelab](https://github.com/spacelab-ufsc) automated tests using the GitHub actions feature, but it might help beginner embedded system developers to setup their own automated tests environment. This workflow was designed considering a specific hardware platform (TI's MSP-430 familly), in a controlled environment (a self-hosted runner computer) and for evaluating results using the UART port. Then, since the workflow it is not generic, adaptations are required for different platforms and contexts.


## Workflows

The .github/workflows folder contains python scripts, bash scripts and yaml files, which allows the execution of a complete set of tests in the target hardware device connected to a self-hosted runner computer. This workflow is powered by the GitHub Actions that enable continuos integration in a very customizable manner.

The workflow consists of the following:
```
Files to setup the workflow actions:
- app-workflow.yml
- devices-workflow.yml
- drivers-workflow.yml
- hardware-workflow.yml
- integration-workflow.yml

Python script to setup and deploy each test within a workflow context: 
- test-deployer.py
Python script to implement a serial terminal for monitoring the UART port:
- uart-terminal.py

Bash script for detecting physically connected USBs in the runner computer:
check-devices.sh
```

Inside each file there comments to help undestand the workflow/CI/HIL operation. In summary, the yaml workflows are triggered manually and calls the execution of a category of tests. This is possible through the use of a self-hosted runner computer, which has the environment already configured: target module connected using the programmer, UART connected using a FTDI and the programs/IDE/applications already intalled/configured. This computer is configured using the [GitHub](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners#about-self-hosted-runners) framework.

The most import details are: the self-hosted runner computer configured and ready to test; the JSON file created from the test/[type] folder using the `test-deployer.py`; the workflow action matrix generation from this JSON file, which create several iterations to loop the tests in different setups for each execution; the `makefile` to call the IDE compiler and the flash tool; and the execution of the `uart-terminal.py` for reading the serial port and waiting a termination for evaluating the test result.

The JSON file format created is the presented below. It is based on what is found by the test-deployer.py in the tests/[type] folder. 

```json
{
  "include": [
    {
      "name": "main_dummy_1",
      "type": "driver",
      "file": "main_dummy_1.c"
    },
    {
      "name": "main_dummy_2",
      "type": "driver",
      "file": "main_dummy_2.c"
    },
    {
      "name": "main_dummy_3",
      "type": "driver",
      "file": "main_dummy_3.c"
    }
  ]
}
```

## Scripts

### uart-terminal.py

It is a simple serial terminal written in Python. **This script was written by [Lucas Luza](https://github.com/lucasmluza) from [LIRMM](http://www.lirmm.fr/)'s group under the supervision of [Luigi Dilillo](http://www.lirmm.fr/~dilillo/).** 

**Software requirements**
```
- Python 3
```

> Tested with Python 3.7.3 using Windows 10 [Build 18362] and Python 3.5.2 using ubuntu 16.04 LTS

**Python required libraries**
```
- re
- sys
- datetime
- pyserial
```

**Usage**

```
./uart-terminal.py [port] [baud] *[logfile]
```
Where:
```
- [port]: device port (ex: /dev/ttyUSB0)
- [baud]: device baud rate (ex: 115200)
- [logfile]: if defined, will store the input data to the file (ex: log_yyyy_mm_dd.txt)
- *: optional
```

Example:
```
./uart-terminal.py /dev/ttyACM0 115200 log_2020-02-17.txt
```
> To solve permission access to the USB port: sudo usermod -a -G dialout $USER



### test-deployer.py

It is a simple test deployer written in Python, which generate JSON files from a test folder and replace the test files before compilation starts in each test iteration.

**Software requirements**
```
- Python 3
```

> Tested with Python 3.5.2 using ubuntu 16.04 LTS

**Python required libraries**
```
- sys
- os
- json
- re
```

**Usage**

```
./test-deployer.py [flag] [parameter]
```
Where:
```
- [flag]: --generate, for creating JSON file and --replace, for replacing main.c file
- [parameter]: flag parameter
```

Examples:
```
./test-deployer.py --generate /test/app                # create .json from app folder
./test-deployer.py --replace /test/app/main_dummy_1.c  # replace main.c by the main_dummy_1.c
```

### check-devices.sh

It is a simple USB written for bash. **This script was written by [Lucas Luza](https://github.com/lucasmluza) from [LIRMM](http://www.lirmm.fr/)'s group under the supervision of [Luigi Dilillo](http://www.lirmm.fr/~dilillo/).** 

**Usage**

```
./check-devices.sh
```

## Tests

**Test scheme**
- The workflow is always a build->flash->test, change main and repeat.
- It must have a test folder containing subfolders (hardware, drivers, devices, app, integration) and a json file (with name, path and type).
- Inside the workflow is called a python script that updates/reads this JSON and setup variables to allow running multiple main file swaps for each test type.
- There are 5 different workflows, one for each test type: hardware, drivers, devices, app, integration;
- Unit Tests = Tests performed per firmware unit.
- Integration Tests = Tests performed per firmware component (several units abstracted).

**Unit Tests:**
- Hardware checks (might require mock circuitry).
- Driver operation checks: not extensive, might use loopback and fake sensor data schemes for hardware checks.
- Device operation checks: one test file for each device implemented, more extensive than driver checks, but should avoid development overhead.
- Standalone application checks: evaluate the application logic (masking or faking operating system calls, such as waiting for queue or a delay). It should be implement without the operating system, in other words, evaluate inputs/outputs in dedicated main file.

**Integration Tests**
- Operating system initialization: assert memory allocation (RAM, stack, heap), hooks and etc;
- Boot sequence (as similar to the actual procedure as possible).
- Operating system task/queue/interrupts priority, constraints, size, depth and delay checks: use dummy task/queue/interrupts (same config as actual system).
- Short-term system check: after 1 hour, exit without error logs.
- Mid-term system check: after 1 day, exit without error logs.
- Long-term system check (used in flatsat): after 1 week, exit without flatsat/integration error logs.
