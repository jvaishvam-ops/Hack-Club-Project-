# Hack-Club-Projects-

## Project Overview

This project is a custom PCB design for a compact input/control board built around a microcontroller footprint and four push-button switch positions. The design includes the complete board layout, fabrication outputs, and supporting documentation for a small productivity-focused device.

## How The Timer Works

The Lock-In Clock is a productivity tracker designed to help me stay focused during study sessions. At its core, it acts as a Pomodoro timer. When powered on, the Raspberry Pi Pico W runs a MicroPython script that defaults to a 25-minute countdown. The current status (like "PAUSED" or "LOCK IN") and the remaining time are displayed on the 0.96" I2C OLED screen.

## What The 4 Buttons Do

I designed the custom PCB to hold 4 tactile Cherry MX Brown mechanical switches to control the timer without needing a mouse or keyboard.

- **Button 1 (Start/Pause):** Toggles the timer on or off. When pressed, the screen updates to say "LOCK IN" and the countdown begins. Pressing it again pauses the timer.
- **Button 2 (Reset):** Stops the timer immediately and resets the clock back to the default 25 minutes.
- **Button 3 (Add Time):** Adds 5 minutes (300 seconds) to the current timer block if I feel like I need a longer study session.
- **Button 4 (Subtract Time):** Subtracts 5 minutes from the current timer block in case I want a shorter sprint.

## How I Used AI in the PCB Layout

I used AI (specifically a large language model) as a troubleshooting and learning assistant while designing the PCB in KiCad. Because this was my first time designing a custom board, I used AI to help me verify my footprint sizes, double-check that my components (like the Cherry MX switches and I2C screen) would physically fit, and ensure my Gerber manufacturing files were formatted correctly (like renaming the edge cuts to `outline.gml` and removing macOS hidden metadata files) before submitting them to the PCB manufacturer.

## Included Design Files

- [BOM.md](BOM.md) — bill of materials
- [JOURNAL.md](JOURNAL.md) — build and design notes
- [README.md](README.md) — project documentation

## KiCad Project Files

The main KiCad source files for the PCB project are kept in the repository root so they can be opened directly in KiCad:

- [week 1 lock in module .kicad_pro](week%201%20lock%20in%20module%20.kicad_pro)
- [week 1 lock in module .kicad_sch](week%201%20lock%20in%20module%20.kicad_sch)
- [week 1 lock in module .kicad_pcb](week%201%20lock%20in%20module%20.kicad_pcb)
- [week 1 lock in module .kicad_prl](week%201%20lock%20in%20module%20.kicad_prl)

## Schematic and Fabrication Files

The repository contains the complete set of PCB fabrication and schematic output files used for the board design:

- [schematic-B_Cu.gbl](schematic-B_Cu.gbl)
- [schematic-B_Cu.gbr](schematic-B_Cu.gbr)
- [schematic-B_Mask.gbr](schematic-B_Mask.gbr)
- [schematic-B_Mask.gbs](schematic-B_Mask.gbs)
- [schematic-B_Paste.gbp](schematic-B_Paste.gbp)
- [schematic-B_Silkscreen.gbo](schematic-B_Silkscreen.gbo)
- [schematic-Edge_Cuts.gbr](schematic-Edge_Cuts.gbr)
- [schematic-Edge_Cuts.gm1](schematic-Edge_Cuts.gm1)
- [schematic-F_Cu.gbr](schematic-F_Cu.gbr)
- [schematic-F_Cu.gtl](schematic-F_Cu.gtl)
- [schematic-F_Mask.gts](schematic-F_Mask.gts)
- [schematic-F_Paste.gbr](schematic-F_Paste.gbr)
- [schematic-F_Paste.gtp](schematic-F_Paste.gtp)
- [schematic-F_Silkscreen.gbr](schematic-F_Silkscreen.gbr)
- [schematic-NPTH.drl](schematic-NPTH.drl)
- [schematic-PTH.drl](schematic-PTH.drl)
- [schematic-job.gbrjob](schematic-job.gbrjob)

## PCB Render and Layout Screenshots

These images show the board from different design and review perspectives.

![3D PCB render](https://raw.githubusercontent.com/jvaishvam-ops/Hack-Club-Project-/main/board-render.png)

![PCB top layout](https://raw.githubusercontent.com/jvaishvam-ops/Hack-Club-Project-/main/pcb-layout.png)

![PCB schematic view](https://raw.githubusercontent.com/jvaishvam-ops/Hack-Club-Project-/main/schematic-view.png)

![Final assembled concept](https://raw.githubusercontent.com/jvaishvam-ops/Hack-Club-Project-/main/assembled-board.png)

## Notes

The repository is designed to document the PCB development process and provide the core fabrication-ready outputs for the project.
