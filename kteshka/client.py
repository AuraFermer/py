import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel)
from PyQt5.QtCore import Qt

API_URL = "http://127.0.0.1:8000/convert"
CURRENCIES = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

class CurrencyConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💱 Конвертер валют")
        self.resize(350, 320)

        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        
        layout.addWidget(QLabel("💰 Введите сумму:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Например: 100")
        layout.addWidget(self.amount_input)

        
        layout.addWidget(QLabel(" Конвертировать:"))
        h_layout = QHBoxLayout()
        self.from_combo = QComboBox()
        self.from_combo.addItems(CURRENCIES)
        h_layout.addWidget(self.from_combo)

        layout.addWidget(QLabel("➡️ В:"))
        self.to_combo = QComboBox()
        self.to_combo.addItems(CURRENCIES)
        self.to_combo.setCurrentText("EUR")
        h_layout.addWidget(self.to_combo)
        layout.addLayout(h_layout)

        
        self.convert_btn = QPushButton("Конвертировать")
        self.convert_btn.clicked.connect(self.convert)
        layout.addWidget(self.convert_btn)

        
        self.result_label = QLabel("Результат появится здесь")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("QLabel { color: gray; font-size: 14px; }")
        layout.addWidget(self.result_label)

    def convert(self):
        
        self.result_label.setText("⏳ Загрузка...")
        self.result_label.setStyleSheet("QLabel { color: blue; font-size: 14px; }")
        QApplication.processEvents()  

        try:
            
            amount_str = self.amount_input.text().strip()
            if not amount_str:
                raise ValueError("Поле суммы пустое")
            
            amount = float(amount_str)
            if amount < 0:
                raise ValueError("Сумма не может быть отрицательной")

            from_curr = self.from_combo.currentText()
            to_curr = self.to_combo.currentText()

            print(f"📤 Отправляю: {amount} {from_curr} -> {to_curr}")

            
            payload = {
                "amount": amount,
                "from_currency": from_curr,
                "to_currency": to_curr
            }
            response = requests.post(API_URL, json=payload, timeout=5)
            print(f"📥 Статус ответа: {response.status_code}")

            
            response.raise_for_status()

            
            data = response.json()
            print(f"✅ Данные от сервера: {data}")

            result_text = (
                f"💵 {data['amount']} {data['from']} = {data['result']} {data['to']}\n"
                f"📊 Курс: 1 {data['from']} = {data['rate']} {data['to']}"
            )
            self.result_label.setText(result_text)
            self.result_label.setStyleSheet("QLabel { color: green; font-size: 15px; font-weight: bold; }")

        except requests.exceptions.ConnectionError:
            self.show_error("❌ Не удалось подключиться к серверу.\nЗапустите server.py!")
            print("🔴 Ошибка: Сервер не отвечает")
            
        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get("detail", "Ошибка сервера")
            except Exception:
                detail = "Неизвестная ошибка сервера"
            self.show_error(f"❌ Ошибка сервера:\n{detail}")
            print(f"🔴 HTTP ошибка: {detail}")
            
        except ValueError as e:
            self.show_error(f"❌ Ошибка ввода:\n{str(e)}")
            print(f"🔴 Ошибка значения: {e}")
            
        except Exception as e:
            self.show_error(f"❌ Неизвестная ошибка:\n{str(e)}")
            print(f" Исключение: {e}")

    def show_error(self, message):
        self.result_label.setText(message)
        self.result_label.setStyleSheet("QLabel { color: red; font-size: 14px; }")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverterApp()
    window.show()
    sys.exit(app.exec_())