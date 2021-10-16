import argparse
import os
import sys

import logging
import json

import re

def convert_log_to_json(infile, outfile):
    try:
        filename = os.path.basename(outfile)
        ext = os.path.splitext(filename)[1]
        if ext == '.json':
            with open(infile) as file, open(outfile, "w") as ofile:
                # content = file.read().strip()

                lines = file.readlines()

                json_dict = {
                    'trace' : {
                        'messages' : list()
                    },
                    'info' : {
                        'messages' : list()
                    },
                    'warning' : {
                        'messages' : list()
                    },
                    'error' : {
                        'messages' : list()
                    },
                    

                }

                for line in lines:
                    words = line.strip().split()
                    if 'TRACE' in words:
                        json_dict['trace']['messages'].append(line)
                    elif 'INFO' in words:
                        json_dict['info']['messages'].append(line)
                    elif 'WARNING' in words:
                        json_dict['warning']['messages'].append(line)
                    elif 'ERROR' in words:
                        json_dict['error']['messages'].append(line)

                from pprint import pp
                pp(json_dict)
                        
                result = json.dumps(json_dict)
                ofile.write(result)
        else :
            raise ValueError('Output file extension is not .json')
    except ValueError as e:
        logging.critical(repr(e))
    except Exception as e:
        print(repr(e))
        logging.critical('Failed to convert file log to .json')        


def convert_log_to_text(infile, outfile):
    try:
        filename = os.path.basename(outfile)
        ext = os.path.splitext(filename)[1]
        if ext == '.json':
            with open(infile) as file, open(outfile, "w") as ofile:
                ofile.write(file.read().strip())
        else :
            raise ValueError('Output file extension is not .txt')
    except ValueError as e:
        logging.critical(repr(e))
    except Exception as e:
        logging.critical('Failed to convert file log to .txt')


if __name__ == '__main__':
    convert_type = ['json', 'text']

    # create parser
    parser = argparse.ArgumentParser(
        prog='getlog',
        description='Mengambil file log dan mengubah format file.'
    )

    parser.add_argument('path',
        help="Direktori file log yang akan diambil.", 
        default=os.getcwd()
    )

    parser.add_argument('-t',
        action='store',
        choices=convert_type,
        help="Menentukan jenis output file log yang akan diambil.",
        required=False
    )

    parser.add_argument('-o',
        help='Output file direktori dimana akan disimpan.',
        metavar='output_path',
        required=False
    )

    args = parser.parse_args()
    var_args = vars(args)
    
    infile, type, outfile = var_args.values()
    if not type: 
        convert_log_to_text(infile, outfile)
    elif type == 'text':
        convert_log_to_text(infile, outfile)
    elif type == 'json':
        convert_log_to_json(infile, outfile)


