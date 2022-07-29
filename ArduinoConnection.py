import serial
import time
import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def main():
    arduino_data = serial.Serial("com3", 9600)
    time.sleep(2)
    indicator_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ticker = 0

    while True:
        while arduino_data.inWaiting() == 0:
            pass
        indicator = int(str(arduino_data.readline(), "utf-8").strip())
        indicator_array[ticker] = indicator
        ticker = (ticker + 1) % 10
        if indicator_array == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
            arduino_data.close()
            print("Phone Picked Up")
            recording_session()
            indicator_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            arduino_data = serial.Serial("com3", 9600)


def recording_session():

    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l",
        "--list-devices",
        action="store_true",
        help="show list of audio devices and exit",
    )
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser],
    )
    parser.add_argument(
        "filename",
        nargs="?",
        metavar="FILENAME",
        help="audio file to store recording to",
    )
    parser.add_argument(
        "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
    )
    parser.add_argument("-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument(
        "-c", "--channels", type=int, default=1, help="number of input channels"
    )
    parser.add_argument(
        "-t", "--subtype", type=str, help='sound file subtype (e.g. "PCM_24")'
    )
    args = parser.parse_args(remaining)

    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
    if args.filename is None:
        args.filename = tempfile.mktemp(
            prefix="Wedding_Message_", suffix=".wav", dir=""
        )

    # Make sure the file is opened before recording anything:
    try:
        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                          channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                fresh_data = serial.Serial("com3", 9600)
                while fresh_data.inWaiting() == 0:
                    pass
                indicator = int(str(fresh_data.readline(), 'utf-8').strip())
                while indicator == 1:
                    indicators = fresh_data.read_all()
                    if "0" in str(indicators):
                        indicator = 0
                    file.write(q.get())
                raise Exception("Phone Hung Up")
    except Exception as e:
        print(e)
        return


main()
