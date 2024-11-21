from rich.table import Table
from rich import box
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH
from rich.console import Console

console = Console()


def make_selection(options, error_msg, input_msg="Choose by number: "):
    for i, option in enumerate(options):
        if isinstance(option, list):
            print(f"{i + 1}: {option[0].title()}")
        else:
            print(f"{i + 1}: {option.title()}")

    if error_msg:
        print(error_msg)

    choice = int(input(input_msg)) - 1

    if 0 <= choice < len(options):
        return choice
    else:
        raise Exception("Invalid input")
    


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
    item = item_data[0].title()
    amount = item_data[1]
    return f"{item} x{amount}"



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



