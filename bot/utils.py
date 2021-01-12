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
    return f"""
<strong>Header</strong>: <i>{data[1]}</i>
<strong>Text</strong>: <i>{data[2]}</i>
<strong>Status</strong>: <i>{status_codes[data[3]].get('str')}</i>
<strong>Due time</strong>: <i>{data[4]}</i>
"""


def check_time(date_time_str):
    try:
        datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        return True
    except ValueError as e:
        print(f'Error: {e}')
        return False
# ------------ Program functions end ------------ #
