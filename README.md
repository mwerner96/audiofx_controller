# AudioFX Controller
A simple (and not so pretty) UI for sending AudioFX commands via the serial interface. Made as a little side project for a course at Leibniz Uni Hannover.

## How it's done
Made with [Tkinter](https://docs.python.org/3/library/tkinter.html) and [pyserial](https://pythonhosted.org/pyserial/).

## How to run
Run it from the command line with

    python3 controller.py

If you have trouble accessing the serial ports, try running it as root (or administrator on win).

If the script doesn't start at all, mabe you are missing the Tkinter and pyserial libraries.
