import os
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest

@pytest.fixture
def browser():
    """Fixture para configurar el navegador headless."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_smoke_test(browser):
    """SMOKE TEST: Verifica carga básica, título y elementos esenciales."""
    app_url = os.environ.get("APP_BASE_URL", "http://localhost:8000")
    print(f"Smoke test ejecutándose contra: {app_url}")
    
    try:
        # Verificar página principal
        browser.get(app_url + "/")
        print(f"Título de la página: {browser.title}")
        assert "To-Do List" in browser.title
        
        # Verificar elementos esenciales
        h1_element = browser.find_element(By.TAG_NAME, "h1")
        print(f"Texto H1: {h1_element.text}")
        assert "📝 To-Do List" in h1_element.text
        
        # Verificar formulario
        input_element = browser.find_element(By.NAME, "tarea")
        assert input_element.is_displayed(), "Campo de tarea no visible"
        
        button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert button.is_displayed(), "Botón agregar no visible"
        
        # Verificar endpoint de salud
        browser.get(app_url + "/health")
        assert browser.page_source == "OK"
        
        print("✅ Smoke test pasado exitosamente.")
    except Exception as e:
        print(f"❌ Smoke test falló: {e}")
        browser.save_screenshot('smoke_test_failure.png')
        raise