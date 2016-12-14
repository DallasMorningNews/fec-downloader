#!/usr/bin/env python
from cement.core.controller import CementBaseController, expose
from cement.core.foundation import CementApp

from fecdownloader.api import committee_disbursements, individual_contribs
from fecdownloader.utils import json_to_csv, write_csv, write_json


DEFAULT_FORMAT = 'csv'

DEFAULT_ARGUMENTS = [
    (
        ['-f', '--format'],
        dict(
            action='store',
            dest='fmt',
            default=DEFAULT_FORMAT,
            help='Format to export. Either "json" or "csv". Defaults to "csv".'
        ),
    ),
    (
        ['-o', '--out-file'],
        dict(
            action='store',
            dest='out_file',
            help=('Path to an output file. Writes to STDOUT by '
                  'default. Ex: "contribs.csv"')
        ),
    ),
]


class WriterMixin(object):
    def write_out(self, results, show_summary=True):
        if self.app.pargs.out_file is not None:
            outfile = open(self.app.pargs.out_file, 'w')
        else:
            import sys
            outfile = sys.stdout

        fmt = self.app.pargs.fmt.lower()

        if fmt == 'csv':
            write_csv(outfile, list(map(json_to_csv, results)))
        elif fmt == 'json':
            write_json(outfile, results)
        else:
            raise ValueError

        outfile.close()


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'Command-line toolbelt to bulk download FEC API data.'


class ContribController(WriterMixin, CementBaseController):
    @expose(hide=True)
    def default(self):
        results = individual_contribs(
            name=self.app.pargs.contrib_name,
            state=self.app.pargs.contrib_state,
            employer=self.app.pargs.contrib_employer,
            to_committee=self.app.pargs.to_committee
        )

        self.write_out(results)

    class Meta:
        label = 'contribs'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Download itemized individual contributions.'
        arguments = [
            (
                ['-n', '--name'],
                dict(
                    action='store',
                    dest='contrib_name',
                    help='Contributor name to seach for. Ex: "Tillerson"'
                ),
            ),
            (
                ['-s', '--state'],
                dict(
                    action='store',
                    dest='contrib_state',
                    help=('Limit search to contributors in a specific state. '
                          'Separate multiple states with a comma. Ex: "TX"')
                ),
            ),
            (
                ['-e', '--employer'],
                dict(
                    action='store',
                    dest='contrib_employer',
                    help=('Search by the contributor\'s employer. Ex: "Exxon"')
                ),
            ),
            (
                ['-t', '--to-committee'],
                dict(
                    action='store',
                    dest='to_committee',
                    help=('The destination(s) for the contribution by '
                          'committee ID. Ex: "C00573634"')
                ),
            ),
        ] + DEFAULT_ARGUMENTS


class CommitteeContoller(WriterMixin, CementBaseController):
    @expose(hide=True)
    def default(self):
        results = committee_disbursements(
            self.app.pargs.COMMITTEE_ID,
            purpose=self.app.pargs.purpose,
            include_memos=self.app.pargs.include_memos
        )

        self.write_out(results)

    class Meta:
        label = 'committee_disbursements'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Download all disbursements for a committee.'
        arguments = [
            (
                ['COMMITTEE_ID'],
                dict(
                    action='store',
                    help='Committee ID(s) to search for. Ex: "C00121368"'
                ),
            ),
            (
                ['-p', '--purpose'],
                dict(
                    action='store',
                    dest='purpose',
                    help=('The purpose(s) of disbursement to downloads. Ex: '
                          '"contribution"')
                ),
            ),
            (
                ['-m', '--include-memos'],
                dict(
                    action='store_true',
                    dest='include_memos',
                    help=('Include memo-ed transactions (unsuitable for '
                          'calculating subtotals).')
                ),
            ),
        ] + DEFAULT_ARGUMENTS


class FecDownloaderApp(CementApp):
    class Meta:
        label = 'fec'
        handlers = [
            BaseController,
            ContribController,
            CommitteeContoller,
        ]


def main():
    with FecDownloaderApp() as app:
        app.run()


if __name__ == '__main__':
    main()
