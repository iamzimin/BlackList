BACKGROUND_COLOR = "#2D2E40"

BACKGROUND_TF_COLOR = "#3F4462"
BORDER_TF_COLOR = "#FFFFFF"
BORDER_TF_RADIUS = "5px"

BACKGROUND_BUTTON_COLOR = "#46475C"
HOVER_BUTTON_COLOR = "#616278"
PUSH_BUTTON_COLOR = "#3c3d52"
PADDING_BUTTON = "5px"

LIST_BACKGROUND_COLOR = "#37384d"

TEXT_COLOR = "#FFFFFF"
TEXT_SIZE = "15px"

BAN_PLAYER_COLOR = "#FF8484"
FORGIVEN_PLAYER_COLOR = "#E2F96F"
USUAL_PLAYER_COLOR = "#919191"

background_css = f"background-color: {BACKGROUND_COLOR};"
text_css = (f"color: {TEXT_COLOR}; "
            f"font-size: {TEXT_SIZE};")

text_area_css = (f"background-color: {BACKGROUND_TF_COLOR}; "
                 f"border: 1px solid {BORDER_TF_COLOR}; "
                 f"color: {TEXT_COLOR}; "
                 f"border-radius: {BORDER_TF_RADIUS}; "
                 f"font-size: {TEXT_SIZE};")

button_css = (f"QPushButton {{"
              f"background-color: {BACKGROUND_BUTTON_COLOR}; "
              f"border: 1px solid {BORDER_TF_COLOR}; "
              f"color: {TEXT_COLOR}; "
              f"border-radius: {BORDER_TF_RADIUS}; "
              f"padding: {PADDING_BUTTON}; "
              f"font-size: {TEXT_SIZE};"
              f"}}"
              f"QPushButton:hover {{"
              f"    background-color: {HOVER_BUTTON_COLOR};"
              f"}}"
              f"QPushButton:pressed {{"
              f"    background-color: {PUSH_BUTTON_COLOR};"
              f"}}"
              )

list_css = (f"background-color: {LIST_BACKGROUND_COLOR}; "
            f"border: 1px solid {BORDER_TF_COLOR}; "
            f"border-radius: {BORDER_TF_RADIUS}; "
            f"font-size: {TEXT_SIZE};")
