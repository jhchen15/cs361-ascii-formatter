import requests

url = "http://127.0.0.1:8000/format-table"

test_table = {
    "columns": ["col1111", "col2", "col3"],
    "data": [
        {"col1111": 1, "col2": 2, "col3": 3},
        {"col1111": 4, "col2": 5, "col3": 6},
        {"col1111": 7, "col2": 8, "col3": 9},
    ]
}

response = requests.post(url, json=test_table)
for row in response.json():
    print(row)
