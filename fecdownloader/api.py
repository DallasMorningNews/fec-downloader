import os

from fecdownloader.utils import api_request, parse_multi_val


API_BASE_URL = 'https://api.open.fec.gov/'
API_VERSION = 'v1'
API_PER_PAGE = 100


def get_api_url(endpoint):
    return '%s%s/%s' % (API_BASE_URL, API_VERSION, endpoint,)


def add_default_params(params):
    req_params = params.copy()

    try:
        api_key = os.environ['FEC_API_KEY']
    except KeyError:
        raise RuntimeError('The FEC_API_KEY environment variable is required.')

    req_params.update(dict(
        api_key=api_key,
        per_page=API_PER_PAGE,
    ))

    return req_params


def multiyear_api_request(endpoint, params={}, start_year=1980, end_year=2018):
    api_url = get_api_url(endpoint)
    req_params = add_default_params(params)

    results = []

    for year in range(start_year, end_year + 1):
        req_params.update(dict(two_year_transaction_period=year))
        more_results, pagination = api_request(
            api_url, req_params
        )
        results = results + more_results

        while len(more_results) != 0:
            more_results, pagination = api_request(
                api_url,
                req_params,
                last_indices=pagination['last_indexes']
            )
            results = results + more_results

    return results


def paginated_api_request(endpoint, params={}):
    api_url = get_api_url(endpoint)
    req_params = add_default_params(params)

    results, pagination = api_request(
        api_url, req_params
    )

    if pagination['pages'] > 1:
        for page in range(2, pagination['pages'] + 1):
            more_results, pagination = api_request(
                api_url, req_params, page=page
            )
            results = results + more_results

    return results


def individual_contribs(name=None, state=None, employer=None,
                        to_committee=None):
    req_params = {
        'sort': 'contribution_receipt_date',
        'is_individual': 'true'
    }

    if to_committee is not None:
        req_params.update(dict(committee_id=parse_multi_val(to_committee)))

    if name is not None:
        req_params.update(dict(contributor_name=parse_multi_val(name)))

    if state is not None:
        req_params.update(dict(contributor_state=parse_multi_val(state)))

    if employer is not None:
        req_params.update(dict(contributor_employer=parse_multi_val(employer)))

    return multiyear_api_request('schedules/schedule_a/', req_params)


def committee_disbursements(committee_id, purpose=None, include_memos=False):
    req_params = dict(committee_id=parse_multi_val(committee_id))

    if purpose is not None:
        req_params.update(dict(
            disbursement_purpose_category=parse_multi_val(purpose)
        ))

    results = multiyear_api_request(
        'schedules/schedule_b/', params=req_params)

    if not include_memos:
        results = list(filter(lambda r: not r['memoed_subtotal'], results))

    return results
