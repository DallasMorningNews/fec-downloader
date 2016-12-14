# FEC bulk downloader

All of this data is available, in some form, on the FEC's website through the old, clunky [fec.gov](http://www.fec.gov) or the slick new [beta.fec.gov](https://beta.fec.gov/). However, the online interface frequently limits searches to a single campaign cycle so searching for (and, by extension, exporting CSVs for) a single contributor across multiple decades is time-consuming.

This downloader CLI aims to solve that for bulk queries that are commonly-requested by reporters using the excellent [FEC API](https://api.open.fec.gov/developers/).

## Requirements

- Python 3

## Installation

1. Clone the Github repo:
  ```
  $ git clone git@github.com:DallasMorningNews/fec-downloader.git
  ```

2. Step into the directory and install using `pip`:
  ```
  $ cd fec-downloader
  $ pip install .
  ```

3. Get an API key at https://api.data.gov/signup/.

3. Enjoy:
  ```
  fec --help
  ```

## Usage

The `--help` command provides a list of available commands and all query parameters for individual commands are documented at the command line (`fec sub-command --help`). In general, though, there are a few common behaviors across all of the below:

- all commands write to `STDOUT`, but can just as easily write to a file with the `-o` flag
- both CSV and JSON are available with the `-f` flag
- API responses are nested, so CSV outputs are flattened to fit in a tabular format; `__` indicate nested JSON fields that have been flattened into a single row in the CSV

See below for detailed instructions on individual commands.

## Schedule A - individual contributions

- [API documentation for `/schedules/schedule_a/`](https://api.open.fec.gov/developers/#!/receipts/get_schedules_schedule_a)
- [Data dictionary for source file](http://www.fec.gov/finance/disclosure/metadata/metadataforcommitteesummary.shtml)

#### Usage

```
$ fec contribs --help

Download itemized individual contributions.

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -n CONTRIB_NAME, --name CONTRIB_NAME
                        Contributor name to seach for. Ex: "Tillerson"
  -s CONTRIB_STATE, --state CONTRIB_STATE
                        Limit search to contributors in a specific state.
                        Separate multiple states with a comma. Ex: "TX"
  -e CONTRIB_EMPLOYER, --employer CONTRIB_EMPLOYER
                        Search by the contributor's employer. Ex: "Exxon"
  -t TO_COMMITTEE, --to-committee TO_COMMITTEE
                        The destination(s) for the contribution by committee
                        ID. Ex: "C00573634"
  -f FMT, --format FMT  Format to export. Either "json" or "csv". Defaults to
                        "csv".
  -o OUT_FILE, --out-file OUT_FILE
                        Path to an output file. Writes to STDOUT by default.
                        Ex: "contribs.csv"
```

#### Examples

Get all contributions from Xerox employees:

```
$ fec contribs -e xerox
```

Get all contributions (in JSON this time) from anyone with the last name "Decherd" in Texas:

```
$ fec contribs -n decherd
```

Get all contributions to any of Rick Perry's presidential committees:

```
$ fec contribs --to-committee C00500587,C00573634,C00580092,C00580969
```

## Schedule B - disbursements

- [API documentation for `/schedules/schedule_b/`](https://api.open.fec.gov/developers/#!/disbursements/get_schedules_schedule_b)
- [Data dictionary for source file](http://www.fec.gov/finance/disclosure/metadata/CandidateDisbursements.shtml)

#### Usage

```
$ fec committee-disbursements --help

Download all disbursements for a committee.

positional arguments:
  COMMITTEE_ID          Committee ID(s) to search for. Ex: "C00121368"

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -p PURPOSE, --purpose PURPOSE
                        The purpose(s) of disbursement to downloads. Ex:
                        "contribution"
  -m, --include-memos   Include memo-ed transactions (unsuitable for
                        calculating subtotals).
  -f FMT, --format FMT  Format to export. Either "json" or "csv". Defaults to
                        "csv".
  -o OUT_FILE, --out-file OUT_FILE
                        Path to an output file. Writes to STDOUT by default.
                        Ex: "contribs.csv"
```

#### Examples

Get all disbursements from Exxon-Mobil's two PACs:

```
$ fec committee-disbursements C00095406,C00121368 --purpose=contributions
```
