import pytest

@pytest.mark.benchmark
def test_homepage_performance(benchmark, client):
    def load_home():
        return client.get("/")
    
    response = benchmark(load_home)
    assert response.status_code == 200
