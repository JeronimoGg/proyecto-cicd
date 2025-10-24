import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    """Configura el navegador en modo headless para el entorno CI/CD."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_smoke_todo_app(browser):
    """SMOKE TEST: Verifica carga básica, título y elementos esenciales de la app."""
    app_url = os.environ.get("APP_BASE_URL", "http://localhost:5000")
    print(f"Smoke test ejecutándose contra: {app_url}")

    try:
        # Verificar que la app carga correctamente
        browser.get(app_url + "/")
        print(f"Título de la página: {browser.title}")
        assert "To-Do List" in browser.title

        # Verificar que el encabezado principal es correcto
        h1 = browser.find_element(By.TAG_NAME, "h1")
        print(f"Texto del H1: {h1.text}")
        assert "📝 To-Do List" in h1.text

        # Verificar el campo de texto para agregar tareas
        input_tarea = browser.find_element(By.NAME, "tarea")
        assert input_tarea.is_displayed(), "El campo de texto no está visible"

        # Verificar el botón de agregar
        boton_agregar = browser.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        assert boton_agregar.is_displayed(), "El botón 'Agregar' no está visible"
        assert boton_agregar.text.strip().lower() == "agregar", "El texto del botón no coincide"

        # Verificar el endpoint de salud
        browser.get(app_url + "/health")
        page_text = browser.page_source.strip()
        print(f"Respuesta /health: {page_text}")
        assert "OK" in page_text, f"Respuesta inesperada en /health: {page_text}"

        print("✅ Smoke test pasado exitosamente.")

    except Exception as e:
        print(f"❌ Smoke test falló: {e}")
        browser.save_screenshot("smoke_test_failure.png")
        raise
