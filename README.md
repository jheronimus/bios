This is an attempt to document all known MrBIOS http://mrbios.com and Unicore Award images for retro PC motherboards, from XT to Pentium generations.

Depending on the platform and version benefits may include support for newer CPUs, larger hard disks. Biggest one IMHO is an almost instant boot — MrBIOS can be configured to omit all diagnostics info and memory tests and just let you boot your OS in a couple of seconds.

The MR BIOS collection currently includes ~450 images for XT, 286, 386, 486 and Soc5/Soc7 motherboards, versions from 1.0A to 3.46.
The Unicore collection includes 3337 images, around half of them are identified. With the exception of a few images, all of this is meant for Socket 5 and Socket 7 motherboards.

Sources of information include:

[MrBIOS 1.65 documentation](https://archive.org/details/target5)

[Evergreen Spectra companion CD v4](https://archive.org/details/evergreenspectrabios)

[Vogons](https://www.vogons.org/viewtopic.php?f=61&t=59146)

[The Retro Web](https://theretroweb.com/bios?biosManufacturerId=284Id=284)

[BIOS Companion by Phil Croucher](https://archive.org/details/pc_engineers_vol1_BIOS)

[BIOS Kompendium by Hans-Peter Shulz](https://www.hzdr.de/FWR/VB/BIOS/mrboard.htm) (note: I'm pretty sure the lines in this table got misplaced, but I did use this to identify the chipset for some Socket 7 images). Dead.

[archived version of Wim's BIOS](https://web.archive.org/web/19990508213249/http://www.ping.be/bios/mrbios.html)

[list of Triton motherboards](https://web.archive.org/web/20010802132444/http://mrbios.com/tritonmb.htm)

For Intel-made Soc5/Soc7 boards it's recommended to use Evergreen Spectra [floppy](https://www.vogonsdrivers.com/getfile.php?fileid=551) and [CD](http://www.vogonsdrivers.com/getfile.php?fileid=547). 

Note that I have no way of validating all these images, so there is no guarantee they are correctly identified — even MrBIOS docs seem to contain errors. I recommend only trying these images if you know how to restore the original BIOS on your motherboard.

The original catalogues are available here:

[MR BIOS](https://docs.google.com/spreadsheets/d/1vtPsoKNyGD3ujMWK_G7ldm7G-jBiyPGXZOp8ZeyuFf8/edit?gid=1763344312#gid=1763344312)
[Unicore](https://docs.google.com/spreadsheets/d/1LAG0ofYZlIE-chpsF85FRbC5i21hUMRf8iWHp90YDLQ/edit?gid=1802190894#gid=1802190894)

Note on AI usage:

This catalogue is a result of years of manual research. AI was only used for the web version (and even that one is just standard Hugo) and data migration (currently working on rechecking all of it).
