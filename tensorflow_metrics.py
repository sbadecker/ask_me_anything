from tensorboard.compat.tensorflow_stub import tensor_shape
from tensorflow.python.framework import ops
from tensorflow.python.keras.metrics import AUC
from tensorflow.python.keras.utils import metrics_utils
from tensorflow.python.ops import check_ops
from tensorflow.python.util.tf_export import keras_export
import tensorflow as tf


@keras_export('keras.metrics.AUC')
class AUCWithLogits(AUC):
    def update_state(self, y_true, y_pred, sample_weight=None):
        """Accumulates confusion matrix statistics.
        Args:
          y_true: The ground truth values.
          y_pred: The predicted values.
          sample_weight: Optional weighting of each example. Defaults to 1. Can be a
            `Tensor` whose rank is either 0, or the same rank as `y_true`, and must
            be broadcastable to `y_true`.
        Returns:
          Update op.
        """
        y_pred = tf.math.softmax(y_pred)
        deps = []
        if not self._built:
            self._build(tensor_shape.TensorShape(y_pred.shape))

        if self.multi_label or (self.label_weights is not None):
            # y_true should have shape (number of examples, number of labels).
            shapes = [
                (y_true, ('N', 'L'))
            ]
            if self.multi_label:
                # TP, TN, FP, and FN should all have shape
                # (number of thresholds, number of labels).
                shapes.extend([(self.true_positives, ('T', 'L')),
                               (self.true_negatives, ('T', 'L')),
                               (self.false_positives, ('T', 'L')),
                               (self.false_negatives, ('T', 'L'))])
            if self.label_weights is not None:
                # label_weights should be of length equal to the number of labels.
                shapes.append((self.label_weights, ('L',)))
            deps = [
                check_ops.assert_shapes(
                    shapes, message='Number of labels is not consistent.')
            ]

        # Only forward label_weights to update_confusion_matrix_variables when
        # multi_label is False. Otherwise the averaging of individual label AUCs is
        # handled in AUC.result
        label_weights = None if self.multi_label else self.label_weights
        with ops.control_dependencies(deps):
            return metrics_utils.update_confusion_matrix_variables(
                {
                    metrics_utils.ConfusionMatrix.TRUE_POSITIVES:
                        self.true_positives,
                    metrics_utils.ConfusionMatrix.TRUE_NEGATIVES:
                        self.true_negatives,
                    metrics_utils.ConfusionMatrix.FALSE_POSITIVES:
                        self.false_positives,
                    metrics_utils.ConfusionMatrix.FALSE_NEGATIVES:
                        self.false_negatives,
                },
                y_true,
                y_pred,
                self._thresholds,
                sample_weight=sample_weight,
                multi_label=self.multi_label,
                label_weights=label_weights)
