from app import app


def client():
    return app.test_client()


def test_health():
    r = client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_index_has_version():
    r = client().get("/")
    assert r.status_code == 200
    assert "version" in r.get_json()


def test_items():
    r = client().get("/api/items")
    assert len(r.get_json()["items"]) == 2


def test_metrics_exposed():
    client().get("/health")
    r = client().get("/metrics")
    assert r.status_code == 200
    assert b"http_requests_total" in r.data
