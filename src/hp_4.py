# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = list()
    date_obj = list()
    for date in old_dates:
        date_obj.append(datetime.strptime(date, '%Y-%m-%d'))

    for date in date_obj:
        new_dates.append(datetime.strftime(date, '%d %b %Y'))
    return new_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    n_datetime_list = list()
    if not (isinstance(start, str)):
        raise "TypeError:not a string"
    elif not (isinstance(n, int)):
        raise "TypeError:not an integer"
    else:
        for i in range(n):
            n_datetime_list.append(datetime.strptime(start, '%Y-%m-%d') + timedelta(days=i))
    return n_datetime_list

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    date_sequence = [start_date_obj + timedelta(days=i) for i in range(len(values))]
    result = list(zip(date_sequence, values))
    return result


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees = defaultdict(float)
    with open(infile, 'r') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            patron_id = row['patron_id']
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            late_days = (date_returned - date_due).days
            if late_days > 0:
                late_fee = late_days * 0.25
                late_fees[patron_id] += late_fee

    with open(outfile, 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            writer.writerow({
                'patron_id': patron_id,
                'late_fees': f'{fee:.2f}',
            })


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    #BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
