import os
import re
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, \
    QListWidget, QFileDialog, QWidget, QListWidgetItem, QToolTip
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QColor, QCursor, QImage
from PIL import Image
import pytesseract

import config
from blackListDB import BlackListDatabase
from config import ConfigManager
from log import Log
from playerData import PlayerData
import style as style

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'


class BlackListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('BlackList.ico'))
        self.setWindowTitle(f"{config.TABLE_NAME} Blacklist Manager")
        self.setGeometry(100, 100, 700, 500)

        self.setup_ui()

    def setup_ui(self):
        BlackListDatabase.init_database()

        # Widgets
        name_label = QLabel("Имя игрока:")
        self.name_edit = QLineEdit()
        if config.FIND_BY_NAME:
            self.name_edit.textChanged.connect(self.on_name_edit_changed)

        block_game_label = QLabel("Заблокированные игры:")
        self.block_game = QLineEdit()
        self.block_game.setValidator(QIntValidator(0, 999999999))

        description_label = QLabel("Причина:")
        self.description = QLineEdit()

        self.found_players_list = QListWidget()
        self.found_players_list.itemPressed.connect(self.on_player_clicked)
        self.found_players_list.setVisible(False)

        self.players_black_list = QListWidget()
        self.players_black_list.itemPressed.connect(self.on_player_clicked)

        self.add_button = QPushButton("Добавить/Обновить")
        self.add_button.clicked.connect(self.add_player)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_player)

        self.find_players_in_image_label = QLabel("Поиск игроков с фото")
        self.find_players_in_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.load_image_explorer_button = QPushButton("Фото с проводника")
        self.load_image_explorer_button.clicked.connect(self.handle_image_path)

        self.load_image_clipboard_button = QPushButton("Фото с буфера")
        self.load_image_clipboard_button.clicked.connect(self.handle_image_buffer)

        self.players_from_black_list_label = QLabel("Чёрный список")
        self.players_from_black_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clear_found_players_button = QPushButton("Очистить")
        self.clear_found_players_button.clicked.connect(self.clear_found_players)
        self.clear_found_players_button.setVisible(False)

        self.new_game_button = QPushButton("Игра")
        self.new_game_button.clicked.connect(self.new_game)

        # Layouts
        # First column
        first_column = QFormLayout()
        first_column.addRow(name_label, self.name_edit)
        first_column.addRow(block_game_label, self.block_game)
        first_column.addRow(description_label, self.description)

        # Add/Delete buttons
        add_delete_layout = QHBoxLayout()
        add_delete_layout.addWidget(self.add_button)
        add_delete_layout.addWidget(self.delete_button)
        first_column.addRow(add_delete_layout)

        # Image to text
        image_to_text_label_layout = QHBoxLayout()
        image_to_text_label_layout.addWidget(self.find_players_in_image_label)
        image_to_text_button_layout = QHBoxLayout()
        image_to_text_button_layout.addWidget(self.load_image_explorer_button)
        image_to_text_button_layout.addWidget(self.load_image_clipboard_button)
        first_column.addRow(image_to_text_label_layout)
        first_column.addRow(image_to_text_button_layout)

        first_column.addRow(self.found_players_list)
        first_column.addRow(self.clear_found_players_button)

        # Second column
        second_column = QFormLayout()
        second_column.addRow(self.players_from_black_list_label)
        second_column.addRow(self.players_black_list)
        second_column.addRow(self.new_game_button)

        # Horizontal layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(first_column)
        horizontal_layout.addLayout(second_column)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(horizontal_layout)
        self.setCentralWidget(central_widget)

        # Style
        central_widget.setStyleSheet(style.background_css)

        name_label.setStyleSheet(style.text_css)
        description_label.setStyleSheet(style.text_css)
        block_game_label.setStyleSheet(style.text_css)
        self.players_from_black_list_label.setStyleSheet(style.text_css)
        self.find_players_in_image_label.setStyleSheet(style.text_css)

        self.name_edit.setStyleSheet(style.text_area_css)
        self.description.setStyleSheet(style.text_area_css)
        self.block_game.setStyleSheet(style.text_area_css)

        self.add_button.setStyleSheet(style.button_css)
        self.delete_button.setStyleSheet(style.button_css)
        self.load_image_explorer_button.setStyleSheet(style.button_css)
        self.load_image_clipboard_button.setStyleSheet(style.button_css)
        self.clear_found_players_button.setStyleSheet(style.button_css)
        self.new_game_button.setStyleSheet(style.button_css)

        self.found_players_list.setStyleSheet(style.list_css)
        self.players_black_list.setStyleSheet(style.list_css)

        self.fill_player_widget()

    """ Widgets """
    @staticmethod
    def add_player_in_widget(player: PlayerData, listWidget: QListWidget):
        list_item = QListWidgetItem(player.name)

        if player.block_game is None:
            list_item.setForeground(QColor(style.USUAL_PLAYER_COLOR))
        elif player.block_game > 0:
            list_item.setForeground(QColor(style.BAN_PLAYER_COLOR))
        else:
            list_item.setForeground(QColor(style.FORGIVEN_PLAYER_COLOR))

        listWidget.addItem(list_item)

    def fill_player_widget(self):
        players = BlackListDatabase.get_all_players(is_sorted=True)

        self.players_black_list.clear()
        for player in players:
            self.add_player_in_widget(player=player, listWidget=self.players_black_list)

    def delete_player_from_widget(self, player_name: str):
        for item in self.players_black_list.findItems(player_name, Qt.MatchFlag.MatchExactly):
            row = self.players_black_list.row(item)
            self.players_black_list.takeItem(row)

        for item in self.found_players_list.findItems(player_name, Qt.MatchFlag.MatchExactly):
            row = self.found_players_list.row(item)
            self.found_players_list.takeItem(row)

    def fill_player_text_area(self, player: PlayerData):
        self.name_edit.setText(player.name)
        self.block_game.setText(str(player.block_game))
        self.description.setText(player.description)

    def on_name_edit_changed(self):
        player_name = self.name_edit.text().strip()
        player = BlackListDatabase.get_player_by_name(player_name=player_name)
        if player is not None:
            self.fill_player_text_area(player=player)
        else:
            self.block_game.clear()
            self.description.clear()
    """ ================================================================== """

    """ Player manager """
    def add_player(self):
        player_name = re.sub(r'\s', '', self.name_edit.text())
        block_game = re.sub(r'[^0-9]', '', self.block_game.text())
        description = self.description.text().strip()

        if not player_name or not block_game:
            self.show_toast("Имя/Игры не могут быть пустыми!")
            return

        try:
            player = PlayerData(name=player_name, block_game=int(block_game), description=description)
        except ValueError:
            Log.save_log("Неверное значение поля \"Заблокированные игры\"")
            exit(1)

        if BlackListDatabase.get_player_by_name(player_name=player.name) is not None:
            BlackListDatabase.update_player(player=player)
        else:
            BlackListDatabase.insert_player(player=player)

        self.clear_fields()
        self.fill_player_widget()

    def delete_player(self):
        player_name = self.name_edit.text()

        BlackListDatabase.delete_player_by_name(player_name=player_name)
        self.delete_player_from_widget(player_name=player_name)
        self.clear_fields()

    def on_player_clicked(self):
        widget = self.sender()

        if widget == self.players_black_list:
            self.found_players_list.clearSelection()
        elif widget == self.found_players_list:
            self.players_black_list.clearSelection()
        else:
            Log.save_log("Не определён sender в on_player_clicked")
            return

        selected_items = widget.selectedItems()
        if not selected_items:
            Log.save_log("Нет выбранных элементов")
            return

        selected_item_text = selected_items[0].text()

        player = BlackListDatabase.get_player_by_name(selected_item_text)
        if player is None:
            self.name_edit.setText(selected_item_text)
            self.block_game.clear()
            self.description.clear()
            Log.save_log("Игрока не существует в on_player_clicked")
            return

        self.fill_player_text_area(player=player)

    def clear_found_players(self):
        self.found_players_list.clear()
        self.found_players_list.setVisible(False)
        self.clear_found_players_button.setVisible(False)

    @staticmethod
    def image_to_string_arr(image: QImage) -> list[str]:
        temp_image_path = "screenshot.png"
        image.save(temp_image_path)

        text = pytesseract.image_to_string(Image.open(temp_image_path))
        lines = text.split('\n')
        words = [item.split(' ') for item in lines]
        result = set([item for sublist in words for item in sublist if len(item) >= config.MINIMUM_NICKNAME_LENGTH])

        players = [line.strip() for line in result if line.strip()]

        os.remove(temp_image_path)

        return players
    """ ================================================================== """

    """ Image manager """
    def handle_image_buffer(self):
        clipboard = QApplication.clipboard()

        if clipboard.mimeData().hasImage():
            self.find_players_in_image(image=clipboard.image())

    def handle_image_path(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Выберите картинку", "", "Images (*.png *.jpg *.jpeg)")
        if not image_path:
            Log.save_log("Путь до изображения не найден")
            return
        pixmap = QPixmap(image_path)
        image = pixmap.toImage()
        self.find_players_in_image(image=image)

    def find_players_in_image(self, image: QImage):
        self.found_players_list.setVisible(True)

        players_arr = self.image_to_string_arr(image=image)
        Log.save_log(f"Найденные игроки с фото {players_arr}")

        players = BlackListDatabase.find_players_by_name(players_name=players_arr)
        for p in players:
            self.add_player_in_widget(player=p, listWidget=self.found_players_list)

        self.clear_found_players_button.setVisible(True)
    """ ================================================================== """

    """ Other """
    def new_game(self):
        BlackListDatabase.new_game()
        self.fill_player_widget()
        player = BlackListDatabase.get_player_by_name(self.name_edit.text().strip())
        if player is not None:
            self.block_game.setText(str(player.block_game))

    def clear_fields(self):
        self.name_edit.clear()
        self.block_game.clear()
        self.description.clear()
        self.players_black_list.clearSelection()
        self.found_players_list.clearSelection()

    def show_toast(self, text: str):
        QToolTip.setFont(QFont("Arial", 14))
        QToolTip.showText(QCursor.pos(), text, self, QRect(0, 0, 200, 50))
    """ ================================================================== """


if __name__ == "__main__":
    config_manager = ConfigManager("config.txt")
    config_manager.read_config()

    app = QApplication(sys.argv)
    window = BlackListApp()
    window.show()
    sys.exit(app.exec())
