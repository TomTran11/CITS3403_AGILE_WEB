def test_about_page_loads(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert response.request.path == "/about"