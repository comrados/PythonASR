import sys
import argparse
import random
import time


def main(argv):
    print("Maria starts thinking")
    argv = check_args(argv)
    if argv.verbose:
        verbose_output(argv)
    decision = mashka_core(argv)
    mashka_decision_output(decision)


def mashka_core(argv):
    x = random.random()
    if argv.verbose:
        print("Maria compares if {0:.3} is smaller than {1:.3}".format(x, argv.threshold))
    time.sleep(argv.decision_time / 1000)
    if x < argv.threshold:
        return True
    return False


def mashka_decision_output(decision):
    print("Maria's answer:")
    if decision:
        print(':D')
    else:
        print('D:')


def verbose_output(argv):
    print("Maria's decision threshold:", argv.threshold)
    print("Maria's thinking time:", argv.decision_time)


def check_args(argv):
    if argv.decision_time < 0:
        argv.decision_time = 1000
    if 0 > argv.threshold or argv.threshold >= 1:
        argv.decision_time = 0.01
    return argv


def parse_args(argv):
    parser = argparse.ArgumentParser(description='''100% accurate model of decision making system
                                                        embedded in Maria's brain''', prog='mashka.py')
    parser.add_argument('-v', '--verbose', help='Verbose output', default=False, action='store_true')
    parser.add_argument('-t', '--threshold', help="Maria's decision threshold. Range: [0.0, 1)", metavar='<threshold>',
                        default=0.01, type=float)
    parser.add_argument('-d', '--decision-time', help="Maria's thinking time in ms", metavar='<time>',
                        default=1000, type=int)
    try:
        argp = parser.parse_args(argv)
        return argp
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
