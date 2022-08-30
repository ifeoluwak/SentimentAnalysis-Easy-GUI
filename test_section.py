import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QTableView)
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex

import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer

train_labels = []
train_msg = []

count_vect = {}
train_counts = {}
training_words = []

classifier = {}

test_labels = []
test_msgs = []


class TestSection(qtw.QWidget):
    prediction_counter = 0
    def __init__(self, parent: qtw.QWidget):
        super().__init__(parent)

        self.test_upload_section()
        # self.plot()

        self.layout = qtw.QVBoxLayout()        

        self.layout.addWidget(self.test_info_text)
        self.create_classification_report_table([])
        self.layout.addWidget(self.table_title)
        self.layout.addWidget(self.reportTableView)
        self.layout.addWidget(self.predict_title)
        self.layout.addWidget(self.text_to_predict)
        self.layout.addWidget(self.predict_button)
        
        
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.show()

    def test_upload_section(self):
        self.test_info_text = qtw.QLabel("<h3>Test Section<h3>")
        self.test_info_text.setStyleSheet("""
            font-size: 24px;
        """)
        
        self.table_title = qtw.QLabel("<h3>Classification Report<h3>")
        
        
        self.predict_title = qtw.QLabel("<h3>Analyse a Text<h3>")
    
        self.text_to_predict = qtw.QPlainTextEdit()
        self.text_to_predict.setPlaceholderText("Enter a text to predict")
        self.text_to_predict.setFixedHeight(50)

        self.predict_button = qtw.QPushButton('Predict text')
        # self.upload_button.setFixedSize(100, 40)
        self.predict_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #2ABf9E; padding: 10px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.predict_button.clicked.connect(self.predict_user_text)

        # self.create_test_table()


    def create_test_table(self):
        self.testTableView = QTableWidget()
        self.testTableView.setFixedHeight(150)
        self.testTableView.setColumnCount(2)
        self.testTableView.setRowCount(10)
        self.testTableView.setHorizontalHeaderLabels(["Label", "Text"])
        self.testTableView.horizontalHeader().setStretchLastSection(True)
        # self.testTableView.setAlignment(Qt.AlignTop)
        # self.layout.setAlignment(self.testTableView, Qt.AlignTop)

    
    def test_classifier(self):
        count_vect_test = CountVectorizer(vocabulary=training_words)
        print('\n', classifier['value'])
        X_new_counts = count_vect_test.fit_transform(test_msgs)
        predicted = classifier['value'].predict(X_new_counts)
        prediction_metrics = metrics.classification_report(test_labels, predicted, output_dict=True)
        print(prediction_metrics)

        self.create_classification_report_table(prediction_metrics)
        self.layout.addWidget(self.table_title)
        self.layout.addWidget(self.reportTableView)
        self.populate_metrics_table(prediction_metrics)
        self.populate_prediction_frame(predicted)
        self.layout.addStretch()
        self.layout.addWidget(self.predict_title)
        self.layout.addWidget(self.text_to_predict)
        self.layout.addWidget(self.predict_button)
        
        
    def create_classification_report_table(self, prediction_metrics):
        if len(prediction_metrics) < 1:
            self.reportTableView = QTableWidget()
        else:
            self.layout.removeWidget(self.table_title)
            self.layout.removeWidget(self.reportTableView)
            self.layout.removeWidget(self.predict_title)
            self.layout.removeWidget(self.text_to_predict)
            self.layout.removeWidget(self.predict_button)
            # self.reportTableView.deleteLater()
        # self.reportTableView.setFixedHeight(150)
        self.reportTableView.setColumnCount(5)
        self.reportTableView.setRowCount(len(prediction_metrics))
        self.reportTableView.setHorizontalHeaderLabels(["", "Precision", "Recall", "F1-score", "Support"])
        self.reportTableView.horizontalHeader().setStretchLastSection(True)

    
    def populate_metrics_table(self, prediction_metrics):
        for index, (key, value) in enumerate(prediction_metrics.items()):
            self.reportTableView.setItem(index, 0, QTableWidgetItem(key))
            if (key != 'accuracy'):
                for index2, (key2, value2) in enumerate(value.items()):
                    tableItem = QTableWidgetItem(str(round(value2, 3)))
                    tableItem.setTextAlignment(4)
                    self.reportTableView.setItem(index, index2 + 1, tableItem)
            else:
                tableItem = QTableWidgetItem(str(round(value, 3)))
                tableItem.setTextAlignment(4)
                self.reportTableView.setItem(index, 1, QTableWidgetItem(''))
                self.reportTableView.setItem(index, 2, QTableWidgetItem(''))
                self.reportTableView.setItem(index, 3, QTableWidgetItem(''))
                self.reportTableView.setItem(index, 4, tableItem)

    
    def populate_prediction_frame(self, predicted):
        # unique_labels = list(set(test_labels))
        # label_dict = {}
        # for label in unique_labels:
        #     label_dict[label] = [lbl for lbl in predicted if lbl == label]
        #     # neu = [lbl for lbl in predicted if lbl == '2']

        # count = []
        # for label in unique_labels:
        #     count.append(len(label_dict[label]))
        # table = pd.DataFrame.from_dict({ 'labels': unique_labels, 'count': count })
        # print(table)

        predicted_int = list(map(lambda x: x, predicted))
        predicted_category = list(map(lambda x: 'Predicted', predicted))
        
        test_int = list(map(lambda x: x, test_labels))
        test_category = list(map(lambda x: 'Actual', test_labels))
        
        table = pd.DataFrame.from_dict({ 'labels': predicted_int + test_int, 'category': predicted_category + test_category  })
        self.plot(table)
        
        
    def plot(self, df):
        # penguins = sns.load_dataset("titanic")
        # print('-------', penguins)
        if (self.prediction_counter > 0):
            # self.canvas = FigureCanvas(Figure())
            self.layout.removeWidget(self.canvas)
        # else:
        #     self.layout.removeWidget(self.canvas)
        print('-------', df)
        self.canvas = FigureCanvas(Figure())
        unique_labels = list(set(test_labels))
        ax = self.canvas.figure.subplots()
        sns.countplot(x="labels", hue="category", data=df, ax=ax)
        # bins=len(unique_labels)
        ax.set_title(classifier['value'])
        self.canvas.draw()
        self.layout.addWidget(self.canvas)
        self.prediction_counter += 1
        
        
    def predict_user_text(self):
        text_to_predict = self.text_to_predict.toPlainText()
        if not text_to_predict:
            qtw.QMessageBox.about(self, "Error", "Cannot be empty")
        else:
            count_vect_test = CountVectorizer(vocabulary=training_words)
            print('\n', classifier['value'])
            X_new_counts = count_vect_test.fit_transform([text_to_predict])
            predicted = classifier['value'].predict(X_new_counts)
            print(predicted)
            sentiment = "Sentiment of Text is: " + predicted[0]
            qtw.QMessageBox.about(self, "Text Sentiment", sentiment)
            # prediction_metrics = metrics.classification_report(test_labels, predicted, output_dict=True)
            # print(prediction_metrics)
    
    def update_variables(
        self,
        test_labels_param,
        test_msg_param,
        train_count_vect_param,
        train_counts_param,
        training_words_param,
        classifier_param
        ):
        test_labels.clear()
        test_msgs.clear()
        training_words.clear()
        for label in test_labels_param:
            test_labels.append(label)
        for msg in test_msg_param:
            test_msgs.append(msg)
        for word in training_words_param['value']:
            training_words.append(word)
        count_vect['value'] = train_count_vect_param['value']
        train_counts['value'] = train_counts_param['value']
        classifier['value'] = classifier_param['value']
        
        if (len(test_msgs) > 0):
            self.test_classifier()
