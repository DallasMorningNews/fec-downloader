import csv
import json
import time

import requests


def parse_multi_val(val):
    return val.split(',')


def json_to_csv(json_response):
    csv_output = {}

    for outer_key, outer_value in json_response.items():
        if isinstance(outer_value, dict):
            for nested_key, nested_value in outer_value.items():
                csv_output['%s__%s' % (outer_key, nested_key,)] = nested_value
        elif isinstance(outer_value, list) or isinstance(outer_value, tuple):
            csv_output[outer_key] = ', '.join(outer_value)
        else:
            csv_output[outer_key] = outer_value

    return csv_output


def api_request(url, params, last_indices=None, page=None):
    req_params = params.copy()

    if last_indices is not None:
        req_params.update(**last_indices)

    if page is not None:
        req_params.update(dict(page=page))

    r = requests.get(url, params=req_params)
    r.raise_for_status()

    json_response = r.json()

    time.sleep(0.5)

    return json_response['results'], json_response['pagination']


def write_csv(outfile, rows):
    headers = set()
    for row in rows:
        headers.update(set(row.keys()))

    csvwriter = csv.DictWriter(outfile, list(headers), quoting=csv.QUOTE_ALL)
    csvwriter.writeheader()
    csvwriter.writerows(rows)


def write_json(outfile, rows):
    outfile.write(json.dumps(rows))
