from agents.bankassist.evidence import extract_structured_rows


def test_extracts_rows_from_genie_query_attachment():
    response = {
        "content": {
            "queryAttachments": [
                {
                    "queryResult": {
                        "columns": [{"name": "customer_id"}, {"name": "days_past_due"}],
                        "data_array": [["CUST-002", 48], ["CUST-003", 37]],
                    }
                }
            ]
        }
    }
    assert extract_structured_rows(response) == [
        {"customer_id": "CUST-002", "days_past_due": 48},
        {"customer_id": "CUST-003", "days_past_due": 37},
    ]


def test_extracts_rows_from_genie_statement_response():
    response = {
        "content": {
            "queryAttachments": [
                {
                    "statement_response": {
                        "manifest": {
                            "schema": {
                                "columns": [
                                    {"name": "customer_id"},
                                    {"name": "latest_arrangement_date"},
                                ]
                            }
                        },
                        "result": {
                            "data_array": [
                                {
                                    "values": [
                                        {"string_value": "CUST-002"},
                                        {"null_value": "NULL_VALUE"},
                                    ]
                                }
                            ]
                        },
                    }
                }
            ]
        }
    }
    assert extract_structured_rows(response) == [
        {"customer_id": "CUST-002", "latest_arrangement_date": None}
    ]
