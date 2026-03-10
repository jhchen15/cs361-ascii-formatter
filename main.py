from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator

app = FastAPI()


class TableData(BaseModel):
    """
    Data model containing table column headers and data.
    """
    columns: list[str]
    data: list[dict]

    @model_validator(mode='after')
    def fill_missing_values(self):
        for entry in self.data:
            for column in self.columns:
                if column not in entry:
                    entry[column] = ""

        return self


def flatten_columns(columns: list[str], data: list[dict]) -> list[list]:
    """
    Transforms input dictionaries into flat lists of lists column-wise
    """
    flat_list = []
    for column in columns:
        flat_col = [column]
        for entry in data:
            flat_col.append(entry[column])
        flat_list.append(flat_col)

    return flat_list


def flatten_rows(columns: list[str], data: list[dict]) -> list[list]:
    """
    Transforms input dictionaries into flat lists of lists row-wise
    """
    flat_list = []
    for entry in data:
        flat_row = []
        for column in columns:
            flat_row.append(entry[column])
        flat_list.append(flat_row)

    return flat_list


def calculate_col_widths(flat_list: list[list]) -> list[int]:
    """
    Calculates width of each row in flat list
    """
    col_widths = []
    for item in flat_list:
        lengths = list(map(lambda x: len(str(x)), item))
        col_widths.append(max(lengths))
    return col_widths


@app.post("/format-table")
def format_table(data: TableData):
    """
    Formats ASCII table
    """
    flat_cols = flatten_columns(data.columns, data.data)
    column_widths = calculate_col_widths(flat_cols)
    flat_rows = flatten_rows(data.columns, data.data)
    formatted_table = []

    # Construct header
    header_row = ""
    separator_row = ""
    for col in range(0, len(data.columns)):
        header_row += f"| {data.columns[col]:>{column_widths[col]}} "
        separator_row += "|" + ("-" * (column_widths[col] + 2))
    header_row += "|"
    separator_row += "|"
    formatted_table.append(header_row)
    formatted_table.append(separator_row)

    # Construct data rows
    for row in range(0, len(flat_rows)):
        formatted_row = ""
        for col in range(0, len(data.columns)):
            formatted_row += f"| {flat_rows[row][col]:>{column_widths[col]}} "
        formatted_row += "|"
        formatted_table.append(formatted_row)

    return formatted_table


if __name__ == "__main__":
    test_table = {
        "columns": ["col1", "col2", "col3"],
        "data": [
            {"col1": 1, "col2": 2, "col3": 3},
            {"col1": 4, "col2": 5, "col3": 6},
            {"col1": 7, "col2": 8, "col3": 9},
            {"col1": 100, "col2": 110, "col3": 120},
        ]
    }

    print(flatten_rows(columns=test_table["columns"], data=test_table["data"]))
    print(flatten_columns(columns=test_table["columns"], data=test_table["data"]))
    cols = flatten_columns(columns=test_table["columns"], data=test_table["data"])
    print(calculate_col_widths(cols))

    test_table = {
        "columns": ["col1", "col2", "col3"],
        "data": [
            {"col1": 1, "col2": 2, "col3": 3},
            {"col1": 4, "col2": 5, "col3": 6},
            {"col1": 7, "col2": 8, "col3": 9},
        ]
    }

    formatted_table = format_table(test_table)
    print(formatted_table)