"""Utils for bot"""
from datetime import datetime

# ------------ Program variable start ----------- #
status_codes = {
    0: {'str': 'unready', 'reverse_str': 'ready', 'int': 1},
    1: {'str': 'ready', 'reverse_str': 'unready', 'int': 0},
}
note_fields = ['header', 'text', 'time']
# ------------ Program variables end ------------ #


# ------------ Program functions start ---------- #
def note_template(data):
    """Create note template"""
    return f"""
<strong>Header</strong>: <i>{data[1]}</i>
<strong>Text</strong>: <i>{data[2]}</i>
<strong>Status</strong>: <i>{status_codes[data[3]].get('str')}</i>
<strong>Due time</strong>: <i>{data[4]}</i>
"""


def get_time_obj(date_time_str):
    """Check if date format is correct"""
    try:
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        return date_time_obj
    except ValueError as error:
        print(f'Error: {error}')
        return None
# ------------ Program functions end ------------ #
