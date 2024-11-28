import re
from rich import box
from rich.table import Table
from rich.console import Console
from ffx_lookup_tool.src.constants import TABLE_WIDTH


console = Console()


def format_num(num):
    if not isinstance(num, int):
        return num
    
    split_num = list(reversed(str(num)))
    new_num = ""

    for i in range(len(split_num)):
        if i % 3 == 0:
            new_num += "."

        new_num += split_num[i]

    new_num = "".join(list(reversed(new_num.lstrip("."))))
    return new_num



def format_item(item_data):
    item = item_data[0]
    amount = item_data[1]
    return format_string(f"{item} x{amount}")



def format_string(string):
    terms = ['Hp', 'Mp', 'Ap', 'Sos', r'Yat-\d\d', r'Ykt-\d\d']
    caps_pattern = fr'\b({"|".join(terms)})\b'
    amount_pattern = r'\d+X|X\d+'

    string = string.title()

    if re.search(caps_pattern, string):
        string = re.sub(caps_pattern, uppercase, string)

    if re.search(amount_pattern, string):
        string = re.sub(amount_pattern, lowercase, string)
    
    if "Mi'Ihen" in string:
        string = string.replace("Mi'Ihen", "Mi'ihen")
    
    if "Th'Uban" in string:
        string = string.replace("Th'Uban", "Th'uban")
    
    return string


def uppercase(match):
    return match.group().upper()


def lowercase(match):
    return match.group().lower()



def initialize_wrapper_table(title=None):
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)

    if title is not None:
        table.add_column(title)

    return table


def initialize_table(tab_title, num_columns, tab_header=True, column_names=[]):
    table = Table(title=tab_title, show_lines=True, expand=True, box=box.SQUARE, title_style="bold", show_header=tab_header)

    col_width = int(TABLE_WIDTH / num_columns)

    if len(column_names) == 0:
        for i in range(num_columns):
            table.add_column("", width=col_width)
    else:
        for i in range(int(num_columns / len(column_names))):
            for name in column_names:
                table.add_column(name, width=col_width)

    return table





