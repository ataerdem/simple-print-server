# simple-print-server

By using this image on a machine that's connected to my home server via a cable, I can print files through a web interface wirelessly.

In case someone comes accross this at one point:

- It's a simple personal project so it's not maintained.
- This is intended to work on a linux host machine.
- If you intend to use it, make sure your printer is recognized by CUPS running on the host. CUPS printers should be shared between the host and the container.
- It always prints on the default printer of CUPS.
- I know this can be done with CUPS + SAMBA but for some reason, adding the printer did not work out for me. I also find the web interface better.
