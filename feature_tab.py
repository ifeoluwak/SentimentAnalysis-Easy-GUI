import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from PyQt5.QtCore import Qt

class FeatureExtractionTab(qtw.QWidget):
    submitted = qtc.pyqtSignal(str, str, bool, bool, str, str, str, str, str, str)

    def __init__(self, parent: qtw.QWidget):
        super().__init__(parent)

        count_vectorizer_layout = qtw.QVBoxLayout()
        count_vectorizer_layout.setAlignment(Qt.AlignRight)

        self.count_vectorizer_params()
       
        count_vectorizer_layout.addWidget(self.layoutWidget)

        self.setLayout(count_vectorizer_layout)


    def count_vectorizer_params(self):
        self.strip_accents_edit = qtw.QComboBox()
        self.strip_accents_edit.addItems(['', 'ascii', 'unicode'])

        self.analyzer_edit = qtw.QComboBox()
        self.analyzer_edit.addItems(['word', 'char', 'char_wb'])

        self.lowercase_edit = qtw.QCheckBox('Convert to lowercase')
        self.lowercase_edit.setChecked(True)
        self.binary_edit = qtw.QCheckBox('Is binary?')
        self.stop_words_edit = qtw.QPlainTextEdit()
        self.stop_words_edit.setPlaceholderText("e.g the,an,he,she")
        # self.stop_words_edit.setFixedHeight(50)
        # self.stop_words_edit.setFixedWidth(150)
        self.token_pattern_edit = qtw.QPlainTextEdit()
        self.token_pattern_edit.setFixedHeight(30)
        self.token_pattern_edit.setPlaceholderText("e.g [a-z0-9A-Z]")
        # self.token_pattern_edit.setFixedWidth(150)
        self.ngram_range_edit = qtw.QTextEdit()
        self.ngram_range_edit.setFixedHeight(20)
        self.ngram_range_edit.setText("1, 1")
        self.ngram_range_edit.setFixedWidth(200)
        self.max_df_edit = qtw.QLineEdit()
        self.max_df_edit.setValidator(qtg.QIntValidator())
        self.max_df_edit.setFixedWidth(200)
        self.min_df_edit = qtw.QLineEdit()
        self.min_df_edit.setValidator(qtg.QIntValidator())
        self.min_df_edit.setFixedWidth(200)
        self.max_features_edit = qtw.QLineEdit()
        self.max_features_edit.setValidator(qtg.QIntValidator())
        self.max_features_edit.setFixedWidth(200)
        # self.vocabulary_edit = qtw.QTextEdit()
        # self.vocabulary_edit.setFixedHeight(50)


        self.layoutWidget = qtw.QWidget()

        form_layout = qtw.QFormLayout()
        form_layout.setFieldGrowthPolicy(qtw.QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignLeft)


        form_layout.addRow('Strip Accents', self.strip_accents_edit)
        form_layout.addRow('Analyzer', self.analyzer_edit)
        form_layout.addRow('', self.lowercase_edit)
        form_layout.addRow('', self.binary_edit)
        form_layout.addRow('Stop words', self.stop_words_edit)
        form_layout.addRow('Regex Pattern', self.token_pattern_edit)
        form_layout.addRow('Range', self.ngram_range_edit)
        form_layout.addRow('Max Features', self.max_features_edit)
        form_layout.addRow('Max df', self.max_df_edit)
        form_layout.addRow('Min df', self.min_df_edit)

        submit_button = qtw.QPushButton('Save')
        submit_button.clicked.connect(self.submit)

        form_widget = qtw.QWidget()
        form_widget.setLayout(form_layout)

        v_layout = qtw.QVBoxLayout()
        v_layout.addWidget(form_widget)
        v_layout.addWidget(submit_button)
        self.layoutWidget.setLayout(v_layout)


    # def combo_changed(self):
        


    def submit(self):
       print(self.strip_accents_edit.currentText())
       self.strip_accents_edit.currentText()

       print(self.analyzer_edit.currentText())

       self.submitted.emit(
        self.strip_accents_edit.currentText(),
        self.analyzer_edit.currentText(),
        self.lowercase_edit.isChecked(),
        self.binary_edit.isChecked(),
        self.stop_words_edit.toPlainText(),
        self.token_pattern_edit.toPlainText(),
        self.ngram_range_edit.toPlainText(),
        self.max_df_edit.text(),
        self.min_df_edit.text(),
        self.max_features_edit.text(),
        )

    #    print(self.lowercase_edit.isChecked())
    #    print(self.binary_edit.isChecked())
    #    print(self.stop_words_edit.toPlainText())
    #    print(self.token_pattern_edit.toPlainText())
    #    print(self.ngram_range_edit.toPlainText())
    #    print(self.max_df_edit.text())
    #    print(self.min_df_edit.text())
    #    print(self.max_features_edit.text())