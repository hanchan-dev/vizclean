from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

class Metrics:

    @staticmethod
    def accuracy(y_true, y_pred):
        return float(accuracy_score(y_true, y_pred))

    @staticmethod
    def confusion_matrix_data(y_true, y_pred):
        return confusion_matrix(y_true, y_pred).tolist()

    @staticmethod
    def classification_report_text(y_true, y_pred):
        return classification_report(y_true, y_pred)
