from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QCheckBox, QLineEdit, QScrollArea, QWidget
)
class TargetLayout(QScrollArea):
    def __init__(self, target_list):
        super().__init__()
        self.widgetResizable()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.item_data = target_list
        # {
        #     '0':['사람',1000,1000,True],
        #     '69':['test',1000,1000,False],
        #     '67':['핸드폰',1000,1000,False],
        # }
        self.item_widgets = []

        # for item, width, height in self.item_data:
        for key, (item,width,height,checked) in sorted(self.item_data.items()):
            item_layout = QHBoxLayout()
            checkbox = QCheckBox(f'{key}:{item}')
            checkbox.setChecked(checked)
            width_input = QLineEdit()
            width_input.setText(str(width))
            width_input.setMaximumWidth(100)
            width_input.setPlaceholderText("너비")
            height_input = QLineEdit()
            height_input.setText(str(height))
            height_input.setMaximumWidth(100)
            height_input.setPlaceholderText("높이")

            item_layout.addWidget(checkbox)
            item_layout.addWidget(width_input)
            item_layout.addWidget(height_input)

            scroll_layout.addLayout(item_layout)
            self.item_widgets.append((checkbox, width_input, height_input))
        self.setWidget(scroll_content)
    
    def get_targets(self):
        target_data = {}
        for i, (checkbox, width_input, height_input) in enumerate(self.item_widgets):
            item = checkbox.text().split(':')
            width = width_input.text()
            height = height_input.text()
            target_data[item[0]] = [item[1],width,height,checkbox.isChecked()]
        return target_data