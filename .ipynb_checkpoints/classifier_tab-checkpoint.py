import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from PyQt5.QtCore import Qt

svmFormWidgets = []

class ClassifierTab(qtw.QWidget):
    naive_bayes_submitted = qtc.pyqtSignal(str, bool, str)
    knn_submitted = qtc.pyqtSignal(str, str, str, str, str)
    dt_submitted = qtc.pyqtSignal(str, str, str, str, str, str, str, str)
    lvc_submitted = qtc.pyqtSignal(str, str, str, str, bool, str)
    svc_submitted = qtc.pyqtSignal(str, str, str, str, str, str, bool, bool, str)
    
    def __init__(self, parent: qtw.QWidget):
        super().__init__(parent)

        classifiers_layout = qtw.QVBoxLayout()
        self.setUpClassifierTabs()
        classifiers_layout.addWidget(self.tabwidget)
        self.setLayout(classifiers_layout)

    
    def setUpClassifierTabs(self):
        self.tabwidget = qtw.QTabWidget()
        self.svmClassifier()
        self.dtClassifier()
        self.knnClassifier()
        self.nbClassifier()

        self.tabwidget.addTab(self.main_widget, "SVM")
        self.tabwidget.addTab(self.decisionTreeWidget, "Decision Tree")
        self.tabwidget.addTab(self.knnWidget, "KNN")
        self.tabwidget.addTab(self.naiveBayesWidget, "Naive Bayes")

        self.tabwidget.tabBar().setTabTextColor(0, Qt.black)
        self.tabwidget.tabBar().setTabTextColor(1, Qt.black)
        self.tabwidget.tabBar().setTabTextColor(2, Qt.black)
        self.tabwidget.tabBar().setTabTextColor(3, Qt.black)


    def svmClassifier(self):
        self.radioButton1 = qtw.QRadioButton("C-Support Vector")
        self.radioButton1.setChecked(True)
        self.radioButton1.type = "svc"

        self.radioButton2 = qtw.QRadioButton("Linear Support Vector")
        self.radioButton2.type = "lvc"

        self.radioButton1.toggled.connect(self.onClicked)
        self.radioButton2.toggled.connect(self.onClicked)


        self.svm_type_widget = qtw.QWidget()
        layout = qtw.QHBoxLayout()
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)

        self.svm_type_widget.setLayout(layout)

        self.regularization = qtw.QLineEdit()
        self.regularization.setValidator(qtg.QIntValidator())
        self.regularization.setFixedWidth(200)

        self.tol_edit = qtw.QLineEdit()
        self.tol_edit.setValidator(qtg.QDoubleValidator())
        self.tol_edit.setFixedWidth(200)

        self.kernel_edit = qtw.QComboBox()
        self.kernel_edit.addItems(['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'])

        self.degree_edit = qtw.QLineEdit()
        self.degree_edit.setValidator(qtg.QIntValidator())
        self.degree_edit.setFixedWidth(200)

        self.gamma_edit = qtw.QComboBox()
        self.gamma_edit.addItems(['scale', 'auto'])

        self.coeff_edit = qtw.QLineEdit()
        self.coeff_edit.setValidator(qtg.QIntValidator())
        self.coeff_edit.setFixedWidth(200)

        self.shrinking_edit = qtw.QCheckBox()
        self.probability_edit = qtw.QCheckBox()

        self.decision_function_shape_edit = qtw.QComboBox()
        self.decision_function_shape_edit.addItems(['ovr', 'ovo'])

        self.penalty_edit = qtw.QComboBox()
        self.penalty_edit.addItems(['l2', 'l1'])

        self.loss_edit = qtw.QComboBox()
        self.loss_edit.addItems(['squared_hinge', 'hinge'])

        self.dual_edit = qtw.QCheckBox('Is Dual?')
        self.dual_edit.setChecked(True)

        self.multi_class_edit = qtw.QComboBox()
        self.multi_class_edit.addItems(['ovr', 'crammer_singer'])

        self.svmClassifierType1()

        self.main_widget = qtw.QWidget()
        self.main_layout = qtw.QVBoxLayout()

        self.main_layout.addWidget(self.svm_type_widget)

        self.main_widget.setLayout(self.main_layout)

        self.generateSvmForm()

    
    def generateSvmForm(self):
        print(len(svmFormWidgets))
        for wid in svmFormWidgets:
            self.main_layout.addWidget(wid)


    def clearSvmForm(self):
        for layout in svmFormWidgets:
            print(layout)
            self.main_layout.removeWidget(layout)
            layout.hide()
            svmFormWidgets.pop()


    def svmClassifierType1(self):
        formlayout = qtw.QFormLayout()
        formlayout.setFieldGrowthPolicy(qtw.QFormLayout.AllNonFixedFieldsGrow)
        formlayout.setLabelAlignment(Qt.AlignLeft)

        form_layout_widget = qtw.QWidget()

        formlayout.addRow('Regularization (C)', self.regularization)
        formlayout.addRow('Tolerance', self.tol_edit)
        formlayout.addRow('Kernel', self.kernel_edit)
        formlayout.addRow('Degree', self.degree_edit)
        formlayout.addRow('Gamma', self.gamma_edit)
        formlayout.addRow('Coef0', self.coeff_edit)
        formlayout.addRow('Shrinking', self.shrinking_edit)
        formlayout.addRow('Probability', self.probability_edit)
        formlayout.addRow('Decision function of shape', self.decision_function_shape_edit)
        
        form_widget = qtw.QWidget()
        form_widget.setLayout(formlayout)
        
        v_layout = qtw.QVBoxLayout()
        self.svm1_button = qtw.QPushButton("Generate model")
        self.svm1_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #2ABf9E; padding: 10px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.svm1_button.clicked.connect(self.submit_svc)
        
        v_layout.addWidget(form_widget)
        v_layout.addStretch()
        v_layout.addWidget(self.svm1_button)

        form_layout_widget.setLayout(v_layout)
        svmFormWidgets.append(form_layout_widget)


    def svmClassifierType2(self):
        formlayout = qtw.QFormLayout()
        formlayout.setFieldGrowthPolicy(qtw.QFormLayout.AllNonFixedFieldsGrow)
        formlayout.setLabelAlignment(Qt.AlignLeft)


        form_layout_widget = qtw.QWidget()
        

        formlayout.addRow('Regularization (C)', self.regularization)
        formlayout.addRow('Tolerance', self.tol_edit)
        formlayout.addRow('Penalty', self.penalty_edit)
        formlayout.addRow('Loss', self.loss_edit)
        formlayout.addRow('Dual', self.dual_edit)
        formlayout.addRow('Multi-class strategy', self.multi_class_edit)
        
        form_widget = qtw.QWidget()
        form_widget.setLayout(formlayout)
        
        v_layout = qtw.QVBoxLayout()
        self.svm2_button = qtw.QPushButton("Generatesss model")
        self.svm2_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #2ABf9E; padding: 10px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.svm2_button.clicked.connect(self.submit_lvc)
        
        v_layout.addWidget(form_widget)
        v_layout.addStretch()
        v_layout.addWidget(self.svm2_button)

        form_layout_widget.setLayout(v_layout)
        svmFormWidgets.append(form_layout_widget)

    def knnClassifier(self):
        self.knn_weights_edit = qtw.QComboBox()
        self.knn_weights_edit.addItems(['uniform', 'distance'])

        self.knn_algorithm_edit = qtw.QComboBox()
        self.knn_algorithm_edit.addItems(['auto', 'ball_tree', 'kd_tree', 'brute'])

        self.knn_leaf_size_edit = qtw.QLineEdit()
        self.knn_leaf_size_edit.setValidator(qtg.QIntValidator())
        self.knn_leaf_size_edit.setFixedWidth(200)

        self.knn_p_edit = qtw.QLineEdit()
        self.knn_p_edit.setValidator(qtg.QIntValidator())
        self.knn_p_edit.setFixedWidth(200)

        self.knn_neighbors_edit = qtw.QLineEdit()
        self.knn_neighbors_edit.setValidator(qtg.QIntValidator())
        self.knn_neighbors_edit.setFixedWidth(200)


        self.knnWidget = qtw.QWidget()

        formlayout = qtw.QFormLayout()
        formlayout.setFieldGrowthPolicy(qtw.QFormLayout.AllNonFixedFieldsGrow)
        formlayout.setLabelAlignment(Qt.AlignLeft)

        formlayout.addRow('N neighbors', self.knn_neighbors_edit)
        formlayout.addRow('Weights', self.knn_weights_edit)
        formlayout.addRow('Algorithm', self.knn_algorithm_edit)
        formlayout.addRow('Leaf size', self.knn_leaf_size_edit)
        formlayout.addRow('P', self.knn_p_edit)

        # self.knnWidget.setLayout(formlayout)
        form_widget = qtw.QWidget()
        form_widget.setLayout(formlayout)
        
        v_layout = qtw.QVBoxLayout()
        self.knn_button = qtw.QPushButton("Generate model")
        self.knn_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #2ABf9E; padding: 10px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.knn_button.clicked.connect(self.submit_knn)

        v_layout.addWidget(form_widget)
        v_layout.addWidget(self.knn_button)

        self.knnWidget.setLayout(v_layout)

    def nbClassifier(self):
        self.nb_type_edit = qtw.QComboBox()
        self.nb_type_edit.addItems(['Complement', 'Multinomial'])

        self.nb_fit_prior_edit = qtw.QCheckBox()
        self.nb_fit_prior_edit.setChecked(True)

        self.nb_alpha_edit = qtw.QLineEdit()
        self.nb_alpha_edit.setValidator(qtg.QIntValidator())
        self.nb_alpha_edit.setFixedWidth(200)

        self.naiveBayesWidget = qtw.QWidget()

        formlayout = qtw.QFormLayout()
        formlayout.setFieldGrowthPolicy(qtw.QFormLayout.AllNonFixedFieldsGrow)
        formlayout.setLabelAlignment(Qt.AlignLeft)

        formlayout.addRow('Classifier', self.nb_type_edit)
        formlayout.addRow('Alpha', self.nb_alpha_edit)
        formlayout.addRow('Fit prior', self.nb_fit_prior_edit)

        form_widget = qtw.QWidget()
        form_widget.setLayout(formlayout)

        v_layout = qtw.QVBoxLayout()
        self.nb_button = qtw.QPushButton("Generate model")
        self.nb_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #2ABf9E; padding: 10px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.nb_button.clicked.connect(self.submit_naive_bayes)

        v_layout.addWidget(form_widget)
        v_layout.addWidget(self.nb_button)

        self.naiveBayesWidget.setLayout(v_layout)

    def dtClassifier(self):
        self.dt_criterion_edit = qtw.QComboBox()
        self.dt_criterion_edit.addItems(['gini', 'entropy', 'log_loss'])
        # self.strip_accents_edit.setAlign

        self.dt_splitter_edit = qtw.QComboBox()
        self.dt_splitter_edit.addItems(['best', 'random'])

        self.dt_max_depth_edit = qtw.QLineEdit()
        self.dt_max_depth_edit.setValidator(qtg.QIntValidator())
        self.dt_max_depth_edit.setFixedWidth(200)

        self.dt_min_samples_split_edit = qtw.QLineEdit()
        self.dt_min_samples_split_edit.setValidator(qtg.QIntValidator())
        self.dt_min_samples_split_edit.setFixedWidth(200)

        self.dt_min_samples_leaf_edit = qtw.QLineEdit()
        self.dt_min_samples_leaf_edit.setValidator(qtg.QIntValidator())
        self.dt_min_samples_leaf_edit.setFixedWidth(200)

        self.dt_max_leaf_nodes_edit = qtw.QLineEdit()
        self.dt_max_leaf_nodes_edit.setValidator(qtg.QIntValidator())
        self.dt_max_leaf_nodes_edit.setFixedWidth(200)

        self.dt_random_state_edit = qtw.QLineEdit()
        self.dt_random_state_edit.setValidator(qtg.QIntValidator())
        self.dt_random_state_edit.setFixedWidth(200)

        self.dt_max_features_edit = qtw.QPlainTextEdit()
        self.dt_max_features_edit.setFixedHeight(30)
        self.dt_max_features_edit.setPlaceholderText("e.g int, float or “auto”, “sqrt”, “log2”")


        self.decisionTreeWidget = qtw.QWidget()

        formlayout = qtw.QFormLayout()
        formlayout.setFieldGrowthPolicy(qtw.QFormLayout.AllNonFixedFieldsGrow)
        formlayout.setLabelAlignment(Qt.AlignLeft)

        formlayout.addRow('Criterion', self.dt_criterion_edit)
        formlayout.addRow('Splitter', self.dt_splitter_edit)
        formlayout.addRow('Max depth', self.dt_max_depth_edit)
        formlayout.addRow('Min samples split', self.dt_min_samples_split_edit)
        formlayout.addRow('Min samples leaf', self.dt_min_samples_leaf_edit)
        formlayout.addRow('Max leaf nodes', self.dt_max_leaf_nodes_edit)
        formlayout.addRow('Random state', self.dt_random_state_edit)
        formlayout.addRow('Max Features', self.dt_max_features_edit)
        
        form_widget = qtw.QWidget()
        form_widget.setLayout(formlayout)

        v_layout = qtw.QVBoxLayout()
        self.dt_button = qtw.QPushButton("Generate model")
        self.dt_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #2ABf9E; padding: 10px; color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.dt_button.clicked.connect(self.submit_decision_tree)

        v_layout.addWidget(form_widget)
        v_layout.addWidget(self.dt_button)

        self.decisionTreeWidget.setLayout(v_layout)
    
    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.clearSvmForm()
            if (radioButton.type == 'svc'):
                self.svmClassifierType1()
            else:
                self.svmClassifierType2()

            self.generateSvmForm()

    def submit_naive_bayes(self):
       self.naive_bayes_submitted.emit(
        self.nb_type_edit.currentText(),
        self.nb_fit_prior_edit.isChecked(),
        self.nb_alpha_edit.text(),
        )
        
    def submit_knn(self):
       self.knn_submitted.emit(
        self.knn_weights_edit.currentText(),
        self.knn_algorithm_edit.currentText(),
        self.knn_neighbors_edit.text(),
        self.knn_leaf_size_edit.text(),
        self.knn_p_edit.text(),
        )
    
    def submit_decision_tree(self):
       self.dt_submitted.emit(
        self.dt_criterion_edit.currentText(),
        self.dt_splitter_edit.currentText(),
        self.dt_max_depth_edit.text(),
        self.dt_min_samples_split_edit.text(),
        self.dt_min_samples_leaf_edit.text(),
        self.dt_max_leaf_nodes_edit.text(),
        self.dt_random_state_edit.text(),
        self.dt_max_features_edit.toPlainText(),
        )
    
    def submit_lvc(self):
        self.lvc_submitted.emit(
            self.regularization.text(),
            self.tol_edit.text(),
            self.penalty_edit.currentText(),
            self.loss_edit.currentText(),
            self.dual_edit.isChecked(),
            self.multi_class_edit.currentText(),
        )
        
    def submit_svc(self):
        self.svc_submitted.emit(
            self.regularization.text(),
            self.tol_edit.text(),
            self.kernel_edit.currentText(),
            self.degree_edit.text(),
            self.gamma_edit.currentText(),
            self.coeff_edit.text(),
            self.shrinking_edit.isChecked(),
            self.probability_edit.isChecked(),
            self.decision_function_shape_edit.currentText(),
        )
