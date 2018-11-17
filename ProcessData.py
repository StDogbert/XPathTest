#!/usr/bin/env python3

import csv
import sys
import getopt
import datetime
import numpy

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def usage():
    print("You should provide 3 arguments: Start date, End date and commodity type [gold/silver]")
    print("Start date and end date should conform to format: %y-%m-%d")


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error as msg:
            raise Usage(msg)
    except Usage as err:
        print(sys.stderr, err.msg)
        print(sys.stderr, "for help use --help")
        return 2

    for o, _ in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if len(args) < 3:
        raise Usage("ERROR! Not enough arguments!")

    start_date_str = args[0]
    end_date_str = args[1]
    commodity = args[2].lower()

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%y-%m-%d')
    except Exception:
        print(sys.stderr, "Start date or/and end date has wrong format")
        print(sys.stderr, "for help use --help")
        return 3

    if start_date >= end_date:
        print(sys.stderr, "End date should be higher than start date")
        print(sys.stderr, "for help use --help")
        return 4

    if commodity not in ["gold", "silver"]:
        print(sys.stderr, "Commodity should be one of the following: gold, silver")
        print(sys.stderr, "for help use --help")
        return 5

    prices = []

    with open('{}.csv'.format(commodity), 'r') as csvfile:
        entries = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for date_str, price in entries:
            try:
                date = datetime.datetime.strptime(date_str, '%y-%m-%d')
            except Exception:
                print(sys.stderr, "Stored data is corrupted")
                print(sys.stderr, "for help use --help")
                return 6
            if date >= start_date and date <= end_date:
                prices.append(float(price))

    if len(prices) < 1:
        print(sys.stderr, "No entries match set dates")
        print(sys.stderr, "for help use --help")
        return 7

    mean = numpy.mean(prices)
    variance = numpy.var(prices)
    print(commodity, mean, variance)

if __name__ == "__main__":
    sys.exit(main())

