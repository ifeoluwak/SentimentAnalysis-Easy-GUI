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

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn import tree
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

from classifier_tab import ClassifierTab
from feature_tab import FeatureExtractionTab
from test_section import TestSection

naive_bayes_params = {
    "fit_prior": True,
    "alpha": 1,
}
naive_bayes_type = MultinomialNB

train_labels = []
train_msg = []

test_label = []
test_msg = []

feature_params = {}

count_vect = {}
train_counts = {}
training_words = {}

classifier = {}

class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_classifier = qtc.pyqtSignal()
        knn_params = qtc.pyqtSignal(dict)

        sns.set_theme(style="darkgrid")

        self.training_upload_section()
        # TestSection(self)
        self.setUpMainTab()
        self.widget_layout()

        self.show()

    def training_upload_section(self):
        self.textedit = qtw.QTextEdit()

        self.info_text = qtw.QLabel("<h3>Training Section<h3>")
        self.info_text.setStyleSheet("""
            font-size: 24px;
        """)

        self.upload_button = qtw.QPushButton('Upload Training Data Set')
        # self.upload_button.setFixedSize(100, 40)
        self.upload_button.setStyleSheet("""
            border-radius: 45px;
            background-color: #2ABf9E;
            padding: 10px;
            font-size: 18px;
            color: white;
        """)
        self.upload_button.clicked.connect(self.open)

        self.create_table()


    def create_table(self):
        self.traintableView = QTableWidget()
        self.traintableView.setFixedHeight(150)
        self.traintableView.setColumnCount(2)
        self.traintableView.setRowCount(10)
        self.traintableView.setHorizontalHeaderLabels(["Label", "Text"])
        self.traintableView.horizontalHeader().setStretchLastSection(True)


    def widget_layout(self):
        layout = qtw.QHBoxLayout()
        layout.setSpacing(50)

        self.left_layout = qtw.QVBoxLayout()
        # self.left_layout.setFixedWidth(550)
        right_layout = qtw.QVBoxLayout()
        # right_layout.setFixedWidth(550)

        self.left_layout.addWidget(self.info_text)
        self.left_layout.addWidget(self.traintableView)
        self.left_layout.addWidget(self.upload_button)

        self.left_layout.addWidget(self.tabwidget)

        # right_layout.addWidget(TestSection(self))

        left_widget = qtw.QWidget()
        left_widget.setLayout(self.left_layout)

        # right_widget = qtw.QWidget()
        # right_widget.setLayout(right_layout)

        self.test_section = TestSection(self)

        layout.addWidget(left_widget)
        layout.addWidget(self.test_section)

        # main_widget = qtw.QWidget()
        # main_widget.setLayout(layout)

        self.setLayout(layout)
        # self.setCentralWidget(main_widget)


    def setUpMainTab(self):
        self.tabwidget = qtw.QTabWidget()
        self.featureTab = FeatureExtractionTab(self)
        self.featureTab.submitted.connect(self.handle_feature_params)

        self.classifierTab = ClassifierTab(self)
        self.classifierTab.naive_bayes_submitted.connect(self.handle_naive_bayes_submit)
        self.classifierTab.knn_submitted.connect(self.handle_knn_submit)
        self.classifierTab.dt_submitted.connect(self.handle_dt_submit)
        self.classifierTab.lvc_submitted.connect(self.handle_lvc_submit)


        self.tabwidget.addTab(self.featureTab, "Feature extraction")
        self.tabwidget.addTab(self.classifierTab, "Classifiers")

        self.tabwidget.tabBar().setTabTextColor(0, Qt.black)
        self.tabwidget.tabBar().setTabTextColor(1, Qt.black)
        
        
    def open(self):
        filename, vv = qtw.QFileDialog.getOpenFileName(filter="*.csv *.txt")
        if filename:
            file = open(filename, 'r')
            first = file.read(1)
            print(first)
            # print(filename)
            hasHeader = first not in '.-0123456789'
            print(hasHeader)
            # lines = file.readlines()
            # print(filename)
            # we want to split the data to 70% training and 30% test
            # len_of_train_data = round(len(lines) * 0.7)
            # i = 0
            # train_labels.clear()
            # train_msg.clear()
            # test_label.clear()
            # test_msg.clear()
            # for line in lines:
            #     print(line)
                # splitLine = line.split('\t')
                # item_label = splitLine[0]
                # item_msg = splitLine[2]
                # if (i < len_of_train_data):
                #     train_labels.append(item_label)
                #     train_msg.append(item_msg)
                # else:
                #     test_label.append(item_label)
                #     test_msg.append(item_msg)
                # if i < 10:
                #     self.traintableView.setItem(i, 0, QTableWidgetItem(item_label))
                #     self.traintableView.setItem(i, 1, QTableWidgetItem(item_msg))
                # i += 1
                # if i > 9:
                #     break

            # if len(train_msg):
                


    def train_dataset(self):
        # print(feature_params)
        count_vect['value'] = CountVectorizer(**feature_params)
        # print(count_vect)
        train_counts['value'] = count_vect['value'].fit_transform(train_msg)
        training_words['value'] = count_vect['value'].get_feature_names()
        print("train_counts", train_counts)
        # print(training_words)


        # self.h_layout = qtw.QHBoxLayout()
        # self.h_layout.setSpacing(4)
        # self.h_layout.setContentsMargins(4, 4, 4, 4)
        # feature_widget = qtw.QWidget()
        # feature_widget.setLayout(self.h_layout)

        # gh = qtw.Qtwev

        # for word in training_words:
        #     self.add_tag_to_bar(word)
        
        # self.left_layout.addWidget(feature_widget)

    def add_tag_to_bar(self, text):
        label = qtw.QLabel(text)
        label.setStyleSheet('border:1px solid rgb(192, 192, 192); border-radius: 4px;')
        # label.setFixedHeight(16)
        label.setFixedSize(50, 20)
        self.h_layout.addWidget(label)
        label.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Preferred)
        # self.h_layout.addWidget(tag)


    @qtc.pyqtSlot(str, str, bool, bool, str, str, str, str, str, str)
    def handle_feature_params(
        self,
        strip_accents,
        analyzer,
        lowercase,
        binary,
        stop_words,
        token_pattern,
        ngram_range,
        max_df,
        min_df,
        max_features
        ):
        if (strip_accents):
            feature_params['strip_accents'] = strip_accents
        if (analyzer):
            feature_params['analyzer'] = analyzer
        feature_params['lowercase'] = lowercase
        feature_params['binary'] = binary
        if stop_words:
            feature_params['stop_words'] = stop_words
        if token_pattern:
            feature_params['token_pattern'] = token_pattern
        if ngram_range:
            (min, max) = ngram_range.split(',')
            feature_params['ngram_range'] = (int(min), int(max))
        if max_df:
            feature_params['max_df'] = max_df
        if min_df:
            feature_params['min_df'] = min_df
        if max_features:
            feature_params['max_features'] = max_features

        if (len(train_labels)):
            self.train_dataset()
        else:
            qtw.QMessageBox.about(self, "Error", "Please upload training data set")


    @qtc.pyqtSlot(str, bool, str)
    def handle_naive_bayes_submit(
        self,
        type,
        fit_prior,
        alpha,
        ):
        if (len(train_labels)):
            if 'value' not in count_vect:
                self.train_dataset()

            naive_bayes_params['fit_prior'] = fit_prior
            if alpha:
                naive_bayes_params['alpha'] = float(alpha)

            if (type == 'Complement'):
                classifier['value'] = ComplementNB(**naive_bayes_params)
            else:
                classifier['value'] = MultinomialNB(**naive_bayes_params)

            classifier['value'].fit(train_counts['value'], train_labels)
            self.update_test_section_data()
        else:
            qtw.QMessageBox.about(self, "Error", "Please upload training data set")
        
        
    @qtc.pyqtSlot(str, str, str, str, str)
    def handle_knn_submit(
        self,
        weights,
        algorithm,
        n_neighbors,
        leaf_size,
        p,
        ):
        if (len(train_labels)):
            if 'value' not in count_vect:
                self.train_dataset()

            knn_params = {}
            if n_neighbors:
                knn_params['n_neighbors'] = int(n_neighbors)
            knn_params['weights'] = weights
            knn_params['algorithm'] = algorithm
            if leaf_size:
                knn_params['leaf_size'] = int(leaf_size)

            print("knn_params -----", knn_params)
            if p:
                knn_params['p'] = int(p)

            classifier['value'] = KNeighborsClassifier(**knn_params)
            classifier['value'].fit(train_counts['value'], train_labels)
            self.update_test_section_data()
        else:
            qtw.QMessageBox.about(self, "Error", "Please upload training data set")
           
    @qtc.pyqtSlot(str, str, str, str, str, str, str, str)
    def handle_dt_submit(
        self,
        criterion,
        splitter,
        max_depth,
        min_samples_split,
        min_samples_leaf,
        max_features,
        random_state,
        max_leaf_nodes,
        ):
        if (len(train_labels)):
            if 'value' not in count_vect:
                self.train_dataset()
            dt_params = {}
            dt_params['criterion'] = criterion
            dt_params['splitter'] = splitter
            if max_depth:
                dt_params['max_depth'] = int(max_depth)
            if min_samples_split:
                dt_params['min_samples_split'] = float(min_samples_split)
            if min_samples_leaf:
                dt_params['min_samples_leaf'] = float(min_samples_leaf)
            if max_features:
                dt_params['max_features'] = float(max_features)
            if random_state:
                dt_params['random_state'] = int(random_state)
            if max_leaf_nodes:
                dt_params['max_leaf_nodes'] = int(max_leaf_nodes)

            classifier['value'] = tree.DecisionTreeClassifier(**dt_params)
            classifier['value'].fit(train_counts['value'], train_labels)
            print('classifier------', classifier['value'])
            self.update_test_section_data()
        
        else:
            qtw.QMessageBox.about(self, "Error", "Please upload training data set")
            
    
    @qtc.pyqtSlot(str, str, str, str, bool, str)       
    def handle_lvc_submit(
        self,
        regularization,
        tolerance,
        penalty,
        loss,
        dual,
        multi_class
    ):
        if (len(train_labels)):
            if 'value' not in count_vect:
                self.train_dataset()

            lvc_params = {}
            lvc_params['penalty'] = penalty
            lvc_params['loss'] = loss
            lvc_params['dual'] = dual
            lvc_params['multi_class'] = multi_class
            if regularization:
                lvc_params['regularization'] = float(regularization)
            if tolerance:
                lvc_params['tolerance'] = float(tolerance)

            classifier['value'] = svm.LinearSVC(**lvc_params)
            classifier['value'].fit(train_counts['value'], train_labels)
            print('classifier------', classifier['value'])
            self.update_test_section_data()
        
        else:
            qtw.QMessageBox.about(self, "Error", "Please upload training data set")
            
        

    def update_test_section_data(self):
        # print(test_labels)
        # print(test_msg)
        self.test_section.update_variables(
            test_label,
            test_msg,
            count_vect,
            train_counts,
            training_words,
            classifier
        )



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    w.setFixedWidth(1200)
    w.setFixedHeight(900)
    # w.setGeometry(0, 0, 1200, 400)
    app.exec_()