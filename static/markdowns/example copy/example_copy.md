---
title: Tutorial: Accessing PL Bram from PS Side
author: Bugra Tufan
date: 2021-01-01
description: In this tutorial, we will walk through the process of interfacing Programmable Logic (PL) BRAM (Block RAM) with the Processing System (PS) in a Xilinx SoC environment. This tutorial covers the setup using Vivado for hardware design and PetaLinux for software deployment. By the end of this tutorial, you will learn how to configure the BRAM and its controller, build a PetaLinux project, and access the BRAM from the PS using simple memory access commands.
header_img: example_copy/block.png
categories: FPGA, Xilinx, Vivado, PetaLinux
---

## Tutorial: Accessing PL Bram from PS Side
![Block Diagram](/static/markdowns/example/images/block.png)

In this tutorial, we will walk through the process of interfacing Programmable Logic (PL) BRAM (Block RAM) with the Processing System (PS) in a Xilinx SoC environment. This tutorial covers the setup using Vivado for hardware design and PetaLinux for software deployment. By the end of this tutorial, you will learn how to configure the BRAM and its controller, build a PetaLinux project, and access the BRAM from the PS using simple memory access commands.

### Prerequisites

- Xilinx Vivado installed with the appropriate licenses.
- PetaLinux Tools installed and configured.
- A supported Xilinx development board (e.g., Zynq-7000 series or Zynq UltraScale+ MPSoC).

### Step 1: Setting Up the Vivado Project

1. Create a new project in Vivado and select the correct part number corresponding to your development board.
2. Add a new block design and include the Zynq PS in your design.
3. Configure the Zynq PS: Double-click on it and set up the necessary peripherals such as UART, I2C, etc., according to your needs.

### Step 2: Adding and Configuring BRAM

1. Add BRAM to your design: In the block design, click on 'Add IP' and search for "Block Memory Generator". Add it to your design.
2. Configure the Block Memory Generator: Double-click on the Block Memory to configure it. Set the memory type to "Single Port RAM" and adjust the width and depth according to your requirements (e.g., width: 32 bits, depth: 1024).
3. Add a BRAM Controller: Search for “AXI BRAM Controller” in the IP catalog and add it to the block design. Connect the AXI port of the BRAM Controller to one of the AXI General Purpose master interfaces of the Zynq PS.

### Step 3: Address Editor Configuration

1. Open the Address Editor: Ensure the BRAM controller and the block memory are correctly connected and then navigate to the Address Editor tab.
2. Assign Memory Address: Specify a memory address range for the BRAM. For instance, set the base address to `0xA0000000`. Ensure that this address does not overlap with other peripherals or memory.

### Step 4: Generating Bitstream and Exporting Hardware

1. Generate the Bitstream: Once your design is complete, generate the bitstream in Vivado.
2. Export the Hardware: Include the bitstream file when prompted and export the hardware. This will create a `.XSA` file that is used by PetaLinux.

### Step 5: Building the PetaLinux Project

1. Create a PetaLinux project: Use the `.XSA` file to create a new PetaLinux project tailored to your hardware design.
2. Configure the project to include necessary drivers and software components. Use `petalinux-config` and enable components as required.
3. Build the PetaLinux project: Run `petalinux-build` to compile your project.

### Step 6: Accessing BRAM from the PS Side

1. Boot your board with the PetaLinux image.
2. Access the BRAM: Use the `devmem` command to read from and write to the BRAM. To write a value, use:

    ```sh
    devmem 0xA0000000 32 0xDEADBEEF
    ```

3. To read back the value, use:

    ```sh
    devmem 0xA0000000 32
    ```

    If the setup is correct, you should see `0xDEADBEEF` displayed on your terminal.

## Conclusion

You have now successfully interfaced BRAM with the PS side of a Xilinx SoC, using Vivado for the hardware setup and PetaLinux for software. This setup allows for efficient and high-speed data storage and retrieval operations critical for many embedded applications.
