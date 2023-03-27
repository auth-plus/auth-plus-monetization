def test_request_example(client):
    response = client.get("/health")
    assert b"Ok" in response.data