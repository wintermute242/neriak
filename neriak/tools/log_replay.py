import argparse, datetime

parser = argparse.ArgumentParser(description=
    'Replays previously saved logs to a new log file that can be used to test bot responses'
    )
parser.add_argument('-i', '--in-file', dest='input_file', type=str, help='Name of the sample log file to replay', required=True)
parser.add_argument('-o', '--out-file', dest='output_file', type=str, help='Name of the output file to write log e, entries to', required=True)
args = parser.parse_args()

input_file_path = args.input_file
output_file_path = args.output_file

input_file = open(input_file_path, 'r')
output_file = open(output_file_path, 'w')

