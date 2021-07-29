import argparse
import os

parser = argparse.ArgumentParser(description = 'Convert records/resources.')
parser.add_argument('-c', '--config', default=os.path.dirname(__file__) + "/../config/config.yaml", help='Configuration file path.')
parser.add_argument('-s', '--since', default="", help='SINCE=YYYY-MM-DD|vNN.iNN')
# parser.add_argument('-d', '--data', default="", help='Source data')

args = parser.parse_args()

