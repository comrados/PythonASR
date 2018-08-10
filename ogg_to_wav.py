import argparse
import os
import sys
import glob
import time
from pydub import AudioSegment


def init_args(argv):
    """
    Inits input arguments for interaction with command prompt

        :param argv: input arguments

        :return: returns namespace with arguments
    """
    parser = argparse.ArgumentParser(description='''Converts .ogg file(s) to wav. 
                                                 Files are saved under the same name
                                                 but extension is different.''', prog='ogg_to_wav.py')
    parser.add_argument('-v', '--verbose', help='Verbose output: parsed args, files, elapsed time, sample rate.',
                        default=False, action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--path', help='Path to the folder with .ogg files.', metavar='<path>')
    group.add_argument('-f', '--files', nargs='+', help='Distinct file(s) to convert.', metavar='<files>')
    parser.add_argument('-s', '--sample_rate', help='Sample rate of the output file.', metavar='<sample_rate>',
                        default=16000, type=int)
    parser.add_argument('-o', '--out_path', help='Output path. Script saves to the input directory if omitted.')
    try:
        args = parser.parse_args(argv)
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(2)
    else:
        if args.verbose:
            print("\nParsed arguments: ")
            for arg in vars(args):
                attr = getattr(args, arg)
                if hasattr(attr, '__iter__') and not isinstance(attr, str):
                    attr = ', '.join(attr)
                if attr not in [None, False]:
                    print(f'{arg:12} --> {attr}')
        return args
    finally:
        print()


def convert_ogg_to_wav(file, rate, out_path):
    """
    Converts .ogg file to .wav file. Saves to given path

        :param file: filename
        :param rate: sample rate
        :param out_path: file output path

        :return: name of the saved file
    """
    try:
        name, ext = os.path.splitext(file)
        if ext == ".ogg":
            song = AudioSegment.from_ogg(file)
            song = song.set_frame_rate(rate)
            song.export(os.path.join(out_path, name + '.wav'), format="wav")
            return name + '.wav'
        else:
            print("Not .ogg file", file)
    except FileNotFoundError:
        print("Can't read/convert file", file)
        sys.exit(2)


def convert_path(argv):
    """
    Function to process conversion of all .ogg files from given path

    :param argv: input arguments

    :return: number of converted files and output path
    """
    out_path = argv.out_path
    count = 0
    if os.path.isdir(argv.path):
        if argv.verbose:
            print("Converting files from", argv.path)
        os.chdir(argv.path)
        if out_path is None:
            out_path = argv.path
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        for file in glob.glob("*.ogg"):
            out = convert_ogg_to_wav(file, argv.sample_rate, out_path)
            count += 1
            if argv.verbose:
                print(f'{count}> {file} -> {out}')
    else:
        print("Given path is not directory", argv.path)
        sys.exit(2)
    return count, out_path


def convert_files(argv):
    """
    Function to process conversion of distinct .ogg files

    :param argv: input arguments

    :return: number of converted files and output path
    """
    out_path = argv.out_path
    count = 0
    if argv.verbose:
        print("Converting", len(argv.files), "distinct file(s): ")
    for file in argv.files:
        if os.path.exists(file):
            path, name = os.path.split(file)
            os.chdir(path)
            if out_path is None:
                out_path = path
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            out = convert_ogg_to_wav(name, argv.sample_rate, out_path)
            count += 1
            if argv.verbose:
                print(f'{count}> {name} -> {out}')
        else:
            print("File doesn't exist", file)
    return count, out_path


def main(argv):
    """
    Main function. Selects what to do: convert distinct files or files from given directory

    :param argv: input arguments
    """
    time0 = int(round(time.time() * 1000))
    args = init_args(argv)
    count = 0
    out_path = args.out_path
    if args.files is None:
        count, out_path = convert_path(args)
    if args.path is None:
        count, out_path = convert_files(args)
    time1 = int(round(time.time() * 1000))
    print()
    print("Done,", count, "files converted.")
    if args.verbose:
        print("Output directory:", out_path)
        print("Sample rate:", args.sample_rate)
        print("Elapsed time:", time1-time0)


if __name__ == "__main__":
    main(sys.argv[1:])
