#!venv/bin/python3


import sys
import pprint
import logging
import argparse
from local_api_pusher import send_data_through_api


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    logger = logging.getLogger('requests_kerberos')
    parser = argparse.ArgumentParser()
    parser.add_argument('--contur', '-c', help='countur D or I', type=str, default='LOCAL')
    args = parser.parse_args()
    response = send_data_through_svip_api('GET', '/poll/kerberos/', args.contur)
    print(response.text)
#    pprint.pprint(response)
