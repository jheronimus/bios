---
title: "MR BIOS Revision History"
---

| Version | Description |
|---|---|
| 3.10 | Original Zappa ED,ZP ShareWare release; with new PnP core. |
| 3.11 | n/a |
| 3.12 | Bugfix: PnP core overlapped "manual" setup of PCI interrupts. |
| 3.13 | n/a |
| 3.14 | Force bidirectional parallel-port for Nat'l Semi Super-I/O. |
| 3.15 | n/a |
| 3.16 | Asymmetric 2M dram support (16M/bank, single-sided). |
| 3.17 | Limit ATA-disc "auto" to Mode 3.  Mode 4 only avail via "manual". |
| 3.18 | Update for production Cyrix 6x86. |
| 3.19 | LPT modes: SPP,Bidir,EPP,ECP now user options. (SMC & NSC chips). |
| 3.20 | Upgrade: Add CMD 646 EIDE built-in driver.<br>Upgrade: Longer IDE spindown timer values (1,2,5 --> 2,5,10 min).<br>Upgrade: Provide setup field to disable soundblaster totally.<br>Workaround: De-enhance disk seeks to eliminate Norton8 complaint.<br>Workaround: Fix for Adaptec 2940 bios Ver 1.20 bug.<br>Workaround: Fix for S3 '968 32MB pageframe decode bug.<br>Workaround: Fix for Supra PnP Modem bug (drop Adaptec 1542CP fix). |
| 3.21 | Upgrade: Add aggressive "55nS" memory-type option.<br>Bugfix: Obscure bug in "manual" PCI-Int Setup affects mapping over bridge of Ints B,C,D (not A) for a few non-Zappa's. |
| 3.22 | Workaround: Fix for Adaptec 2940 bios Ver 1.21 warm-boot bug.<br>Workaround: Fix for nVidia/SGS VGA, replicated PCI ROM register.<br>Workaround: Fix for Holtek asic 8042 bug.<br>Workaround: Move Pnp-Data-Read port to avoid gameport decode bug. |
| 3.23 | Workaround: Apply v3.22 fix to *all* Adaptec PCI devices.<br>LPT modes: SPP,Bidir,EPP,ECP options for Winbond Super I/O too.<br>Upgrade: Add "CPU-Pipeline" on/off option (for debug purposes).<br>Upgrade: RAID-0 disk striping option, interleave 2-8 IDE drives. |
| 3.24 | Workaround: Disable CPU Pipelining during POST.<br>Upgrade: Higher performance for Mode4 IDE drives. |
| 3.25 | Fix: Timing problem with certain 512K pipeline cache modules.<br>Fix: Incompatibility with WD 719X SCSI controllers. |
| 3.26 | Workaround: Aha2940 PCI I/O alignment for Chinese OS/2 (TWarp).<br>Reduced binary bios image to 92K.  Changed flash loader, now does not clear cmos century byte (ref: NDD95). |
| 3.27 | Workaround: PnP issues with Crystal soundblaster.<br>Workaround: COM4 port usage by ATI video.<br>Update: Aggressive CMOS-default memory settings.<br>Update: Roundup CPU MHz display (cosmetic).<br>Update: Display dram config in Chipset setup screen.<br>Update: Performance tweaks for 6x86 CPU. |
| 3.28 | Update: Deleting on-board COM/LPT ports in "Ports" setup utility now fully disables them.<br>Fix: 6x86 cacheable range for non-binary memory sizes. |
| 3.29 | EV2,ATX,Atlantis: Fix for Crystal Audio + Win95.<br>UMC/ITE 8669F Super I/O chip:  Fix PnP support. |
| 3.30 | Display MR BIOS logo on powerup screen.<br>Show PnP serial and parallel ports in setup utility.<br>Longer IDE spindown timer values (2,5,10 --> 5,10,20 min). |
| 3.31 | Update: Performance tweaks for Cyrix CPU. |
| 3.40 | Changed serial/parallel port handling to allow on board.<br>COM/LPT ports to be configured for specific I/O address.<br>Setup screen also displays com/lpt irq.<br>Added PnP message display at code boot when 1 or more PnP. ISA cards are found: PnP Card Initalization complete!<br>Added support for USB to Intel Triton VX/HX chipset. added option USB port = Enable/Disable to chipset screen in setup. the usb support added should support usb devices with windows95. |
| 3.41 | Update: Add support for AMD K5 PR166, and K6.<br>Update: Add support for Intel Tuscon and latest Advanced/ML <br>motherboards. Requires MRFLASH Ver 2.00 or greater.<br>Update: Upgrade support for UMC 8669 superio.<br>Update: Configure PCI Video Adapters on other side of PCI to PCI <br>bridge.<br>Update: Add support for LGS Prime 3B/3C superio.<br>Fix: Changes to bios for Intel motherboards containing onboard PCI <br>video to properly configure external video as primary video <br>Fix: Fixed problem with MR BIOS not recognizing slave IDE device when <br>attaching two hard drives greater than 1GB as master and slave. <br>Fixed by adding option "IDE Slave Detection" to ATA-Disc menu <br>in bios setup. <br>Fix: Change supported memory ceiling for Triton HX motherboards <br>from 128MB max to 512MB.<br>Fix: Fixed problem which caused poor bus master dma performance.<br>Fix: Fixed problem with PnP modems being configured to same IRQ resources as on-board COM ports. |
| 3.42 | Upgrade: Add Millenium support.<br>Upgrade: Add support for IBM M2 and Cyrix 6x86MX CPU's.<br>Update: Performance enhancements with AMD K5 & K6 CPUs.<br>Fix: Fixed problem with disabling both on-board IDE's controllers <br>with Windows 95.<br>Fix: AMD-K5/PR200 incorrectly identified as 586SX.<br>Fix: Fixed problem with no video after boot when 6 or more PCI <br>devices installed.<br>Fix: Fixed problem with certain 4MB Fast Page Mode memory not identified properly on motherboards with Triton VX chipset.<br>Fix: Do not allocate IRQ to USB device if disabled.<br>Fix: Drive field not erased properly in ATA-DISC BIOS Setup.<br>Fix: PnP configuration problem with ESS 1868 sound card. |
| 3.43 | Upgrade: Added Ultra DMA/33 support to Triton TX chipset<br>Fix: Problem with unconfigured COM/LPT when CMOS corrupted.<br>Fix: Boot sequence defaulted to SCSI when CMOS corrupted.<br>Fix: Boot problem with PCI adapters containing executable option ROMs.<br>Fix: IDE PIO Mode 4 did not work properly.<br>Fix: Intemittant Gate A20 disabled test failures. |
| 3.44 | Upgrade: Added support for IDT Winchip C6 CPU<br>Upgrade: Added Advanced BIOS Setup option to all Intel Triton versions. Contains options to reserve IRQ's for legacy adapters and  option to disable PnP device configuration.<br>Upgrade: Make IRQ12 available for PCI if no PS/2 mouse attached.<br>Fix: Problem with chipset CMOS settings not working with ALI M6117 chipset.<br>Fix: Increase memory ceiling from 128MB to 256MB on Triton TX |
| 3.45 | Upgrade: Added support for AMD K6-2<br>Upgrade: Added suport for additional Winbond 977 superio's.<br>Upgrade: Added support for SMC 67X superio.<br>Fix: Problem with PS/2 mouse not working with Winbond 877 superio. |
| 3.46 | Fix: Problem which caused L2 cache to not be enabled on some motherboards used with some AMD CPU's. <br>Fix: Problem which caused hard disks containing odd number of <br>heads (e.g. 15) to not boot. |
