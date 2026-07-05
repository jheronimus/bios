# Domain Context: BIOS Archive Project

This document establishes the ubiquitous language and domain model for the MR BIOS and Unicore Award BIOS Archive project.

## Core Domain Concepts

### BIOS Image
The raw binary firmware file (typically with a `.BIN` extension) representing a dump of the ROM chip for a specific motherboard BIOS.

### MR BIOS Catalog
The list of MR BIOS firmware images, organized by chipset/manufacturer tabs (e.g., `Intel`, `Acer`, `C&T`), containing fields such as:
- **Part Number**: The unique identifier for Microid Research BIOS versions (e.g., `V058B300`).
- **Code**: The filename prefix associated with the firmware.
- **Chipset**: The target motherboard chipset.
- **Turbo**: Notes about Turbo LED behavior.
- **Note**: General hardware capability observations.

### Unicore Award BIOS Catalog
The list of upgraded Award BIOS images customized by Unicore Software (primarily for Socket 5/7 motherboards to support larger HDDs or newer CPUs), organized by manufacturer/chipset tabs (e.g., `ALi`, `Intel`, `VIA`), containing fields such as:
- **Folder**: The unique identifier directory name containing the BIOS binary (e.g., `2A5KKA29`).
- **Manufacturer**: The motherboard maker.
- **Chipset**: The chipset name.
- **I/O**: The input/output controller model.
- **Release**: Version or release date reference.
- **Motherboard**: The specific target motherboard model.
- **Aliases**: Other names the motherboard is known by.

### Catalog Database
The plain-text source-of-truth representation of the catalogs stored as YAML lists in the repository (e.g., `/data/mrbios/*.yml` and `/data/unicore/*.yml`).

### Hugo SSG (Static Site Generator)
The tool used during GitHub CI/CD to read the Catalog Database YAML files and generate the HTML files serving the website.
