import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = os.environ.get("APP_BASE_URL", "http://localhost:5000")


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def wait_for_text(browser, text, timeout=8):
    try:
        el = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), \"{text}\")]"))
        )
        return el.text
    except TimeoutException:
        return None


def add_task(browser, tarea_text):
    browser.get(BASE_URL)
    input_el = WebDriverWait(browser, 8).until(
        EC.presence_of_element_located((By.NAME, "tarea"))
    )
    submit = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    input_el.clear()
    input_el.send_keys(tarea_text)
    submit.click()


def task_exists(browser, tarea_text):
    browser.get(BASE_URL)
    try:
        WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), \"{tarea_text}\")]"))
        )
        return True
    except TimeoutException:
        return False


def find_delete_for_task(browser, tarea_text):
    browser.get(BASE_URL)
    try:
        # Busca un enlace de eliminar dentro del nodo que contiene el texto de la tarea
        delete_el = WebDriverWait(browser, 6).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), \"{tarea_text}\")]//following::a[contains(@href, '/eliminar')][1]"))
        )
        return delete_el
    except TimeoutException:
        return None


def test_agregar_tarea_valida(browser):
    tarea = "Tarea aceptación 1"
    add_task(browser, tarea)
    assert wait_for_text(browser, "Tarea agregada") or task_exists(browser, tarea)


def test_agregar_tarea_vacia_muestra_error(browser):
    add_task(browser, "")  # envía formulario vacío
    assert "La tarea no puede estar vac" in (wait_for_text(browser, "La tarea no puede estar vac") or "")


def test_eliminar_tarea(browser):
    tarea = "Tarea a eliminar aceptación"
    add_task(browser, tarea)
    # esperar confirmación de agregado o que aparezca en la lista
    assert wait_for_text(browser, "Tarea agregada") or task_exists(browser, tarea)

    delete_el = find_delete_for_task(browser, tarea)
    assert delete_el is not None, "No se encontró enlace de eliminar para la tarea"

    delete_el.click()
    assert wait_for_text(browser, "Tarea eliminada") or not task_exists(browser, tarea)


def test_eliminar_tarea_inexistente_muestra_aviso(browser):
    browser.get(f"{BASE_URL}/eliminar/99999")
    assert "La tarea seleccionada no existe" in (wait_for_text(browser, "La tarea seleccionada no existe") or "")