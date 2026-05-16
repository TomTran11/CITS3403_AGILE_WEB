def test_landing_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.request.path == "/" or response.request.path == "/landing"