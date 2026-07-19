from kata1_clean_csv import parse_records

MESSY = """
 Name , Amount ,  Category

 Alice , 12.50 , books
Bob,   3 ,  food

  ,  ,
 Carol ,7.25, books
"""


def test_parses_and_strips():
    records = parse_records(MESSY)
    assert records == [
        {"name": "Alice", "amount": "12.50", "category": "books"},
        {"name": "Bob", "amount": "3", "category": "food"},
        {"name": "Carol", "amount": "7.25", "category": "books"},
    ]


def test_header_lowercased():
    records = parse_records("FirstName,Age\n Dana , 30 ")
    assert records == [{"firstname": "Dana", "age": "30"}]


def test_blank_input_is_empty():
    assert parse_records("\n   \n , , \n") == []



if __name__ == "__main__":
    test_parses_and_strips() 