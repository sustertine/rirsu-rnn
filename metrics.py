import tensorflow as tf
from tensorflow.keras.metrics import Metric

class ExplainedVarianceScore(Metric):
    def __init__(self, name="explained_variance_score", **kwargs):
        super(ExplainedVarianceScore, self).__init__(name=name, **kwargs)
        self.explained_variance = self.add_weight(name="explained_variance", initializer="zeros")
        self.total_variance = self.add_weight(name="total_variance", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true_mean = tf.reduce_mean(y_true)
        self.explained_variance.assign_add(tf.reduce_sum(tf.square(y_pred - y_true_mean)))
        self.total_variance.assign_add(tf.reduce_sum(tf.square(y_true - y_true_mean)))

    def result(self):
        return self.explained_variance / (self.total_variance + tf.keras.backend.epsilon())

    def reset_state(self):
        self.explained_variance.assign(0.0)
        self.total_variance.assign(0.0)