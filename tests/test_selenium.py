# tests/test_selenium.py
import pytest, time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Rendre accessible le fichier à github
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATH = "file://" + os.path.normpath(BASE_DIR, "../src/index.html")

class TestCalculator:
    def test_page_loads(self, driver):
        driver.get(FILE_PATH)
        assert "Calculatrice Simple" in driver.title
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()
 
    def test_addition(self, driver):
        driver.get(FILE_PATH)
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")
        Select(driver.find_element(By.ID, "operation")).select_by_value("add")
        driver.find_element(By.ID, "calculate").click()
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result")))
        assert "Résultat: 15" in result.text
 
    def test_division_by_zero(self, driver):
        driver.get(FILE_PATH)
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("0")
        Select(driver.find_element(By.ID, "operation")).select_by_value("divide")
        driver.find_element(By.ID, "calculate").click()
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result")))
        assert "Erreur: Division par zéro" in result.text
    
    def test_all_operations(self, driver):
        ops = [("add","8","2","10"),("subtract","8","2","6"),
        ("multiply","8","2","16"),("divide","8","2","4")]
        for op, n1, n2, expected in ops:
            driver.get(FILE_PATH)
            driver.find_element(By.ID, "num1").send_keys(n1)
            driver.find_element(By.ID, "num2").send_keys(n2)
            Select(driver.find_element(By.ID, "operation")).select_by_value(op)
            driver.find_element(By.ID, "calculate").click()
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result")))
            assert f"Résultat: {expected}" in result.text