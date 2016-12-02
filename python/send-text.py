#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse

def send_text(number: str, message: str):
    assert len(message) > 1, 'The mesage cannot be empty'
    payload = {'number': number, 'message': message}
    request = requests.post("http://textbelt.com/text", data=payload)
    json_result = request.json()
    if not json_result['success']:
        if 'message' in json_result:
            raise ValueError("POST to textbelt.com/text failed: {}".format(json_result['message']))
        else:
            raise ValueError("POST to textbelt.com/text failed with unknown error")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a text message.')
    parser.add_argument('--number', required=True, type=str, help='A string in the form 222-222-2222, or 2222222222, +1-222-222-2222')
    parser.add_argument('--message', required=True, type=str, help='Any message with nonzero length')
    opts = parser.parse_args()
    send_text(opts.number, opts.message)

