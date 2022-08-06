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
        self.layout.addWidget(self.testTableView)
        self.layout.addWidget(self.upload_test_button)
        
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.show()

    def test_upload_section(self):
        self.test_info_text = qtw.QLabel("<h3>Upload Test Data Set<h3>")
        # self.test_info_text.setStyleSheet("""
        #     font-size: 24px;
        # """)

        self.upload_test_button = qtw.QPushButton('Upload')
        # self.upload_button.setFixedSize(100, 40)
        self.upload_test_button.setStyleSheet("""
            border-radius: 45px;
            background-color: #2ABf9E;
            padding: 10px;
            font-size: 18px;
            color: white;
        """)
        self.upload_test_button.clicked.connect(self.open)

        self.create_test_table()


    def create_test_table(self):
        self.testTableView = QTableWidget()
        self.testTableView.setFixedHeight(150)
        self.testTableView.setColumnCount(2)
        self.testTableView.setRowCount(10)
        self.testTableView.setHorizontalHeaderLabels(["Label", "Text"])
        self.testTableView.horizontalHeader().setStretchLastSection(True)
        # self.testTableView.setAlignment(Qt.AlignTop)
        # self.layout.setAlignment(self.testTableView, Qt.AlignTop)


    def open(self):
        filename, _ = qtw.QFileDialog.getOpenFileName()
        if filename:
            file = open(filename, 'r')
            lines = file.readlines()
            i = 0
            test_labels.clear()
            test_msgs.clear()
            for line in lines:
                splitLine = line.split('\t')
                item_label = splitLine[0]
                item_msg = splitLine[2]
                test_labels.append(item_label)
                test_msgs.append(item_msg)
                if i < 10:
                    self.testTableView.setItem(i, 0, QTableWidgetItem(item_label))
                    self.testTableView.setItem(i, 1, QTableWidgetItem(item_msg))
                i += 1
        
        if (len(train_labels)):
            self.test_classifier()
        # else:
        #     qtw.QMessageBox.about(self, "Error", "Please upload training data set")

    
    def test_classifier(self):
        count_vect_test = CountVectorizer(vocabulary=training_words)
        print('\n', classifier['value'])
        X_new_counts = count_vect_test.fit_transform(test_msgs)
        predicted = classifier['value'].predict(X_new_counts)
        prediction_metrics = metrics.classification_report(test_labels, predicted, output_dict=True)
        print(prediction_metrics)

        self.create_classification_report_table(prediction_metrics)
        self.layout.addWidget(self.reportTableView)
        self.populate_metrics_table(prediction_metrics)
        self.populate_prediction_frame(predicted)
        
        
    def create_classification_report_table(self, prediction_metrics):
        if (self.prediction_counter < 1):
            self.reportTableView = QTableWidget()
        else:
            self.layout.removeWidget(self.reportTableView)
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

        predicted_int = list(map(lambda x: int(x), predicted))
        predicted_category = list(map(lambda x: 'Predicted', predicted))
        
        train_int = list(map(lambda x: int(x), test_labels))
        train_category = list(map(lambda x: 'Actual', test_labels))
        
        table = pd.DataFrame.from_dict({ 'labels': predicted_int + train_int, 'category': predicted_category + train_category  })
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
    
    def update_variables(
        self,
        train_labels_param,
        train_msg_param,
        train_count_vect_param,
        train_counts_param,
        training_words_param,
        classifier_param
        ):
        train_labels.clear()
        train_msg.clear()
        training_words.clear()
        for label in train_labels_param:
            train_labels.append(label)
        for msg in train_msg_param:
            train_msg.append(msg)
        for word in training_words_param['value']:
            training_words.append(word)
        count_vect['value'] = train_count_vect_param['value']
        train_counts['value'] = train_counts_param['value']
        classifier['value'] = classifier_param['value']
        
        if (len(test_msgs) > 0):
            self.test_classifier()
