################################################   Author - Saran Karthikeyan     #######################################################
################################################ Thanks to tensorflow and Keras    ######################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import collections
import warnings

import numpy as np
from keras import activations
from keras import backend as K
from keras import constraints
from keras import initializers
from keras import regularizers
from keras.engine.base_layer import Layer
from keras.engine.input_spec import InputSpec
from keras.utils import tf_utils
from tensorflow.python.keras.layers.recurrent import DropoutRNNCellMixin
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training.tracking import data_structures
from tensorflow.python.util.tf_export import keras_export

"""
Classes for LSTMCells for each column in Progressive Neural Network Architecture. The cell state formulation for 
each extended LSTM cell varies depending on the previous column LSTMCell values with self attention

LSTMCell has different calculations of cell formulation for each column and number of layer. Hence three classses 
have defined for three separate column. 

PROG_ATTLSTMCELL - LSTMCell for initial column and it has cell state formulation as same as built-in LSTMCell of keras
PROG_ATTLSTMCELL_1 - LSTMCell for extended column 1, which has cell state formulation depending on built-in LSTMCell
                  and previous cell state of initial column according to Progressive Neural Network
PROG_ATTLSTMCELL_2 - LSTMcell for extended column 2, which has cell stae formulation depending on built-in LSTMCell of
                  keras, and previous cell state of initial and previous column according to Progressive Neural Network

References:
- [Long short-term memory](
    http://www.bioinf.jku.at/publications/older/2604.pdf)
- [Progressive Neural Networks](
    https://arxiv.org/pdf/1606.04671.pdf)
- [Supervised sequence labeling with recurrent neural networks](
    http://www.cs.toronto.edu/~graves/preprint.pdf)
- [A Theoretically Grounded Application of Dropout in
    Recurrent Neural Networks](https://arxiv.org/abs/1512.05287)
- [Efficient Estimation of Word Representations in Vector Space](
    https://arxiv.org/pdf/1301.3781.pdf)
- [Long Short-Term Memory Networks for Machine Reading](
    https://www.aclweb.org/anthology/D16-1053.pdf)
    
"""

RECURRENT_DROPOUT_WARNING_MSG = (
    'RNN `implementation=2` is not supported when `recurrent_dropout` is set. '
    'Using `implementation=1`.')

@keras_export(v1=['keras.layers.LSTMCell'])
class LSTMCell(DropoutRNNCellMixin, Layer):

  """Cell class for the LSTM layer.
  Arguments:
    units: Positive integer, dimensionality of the output space.
    activation: Activation function to use.
      Default: hyperbolic tangent (`tanh`).
      If you pass `None`, no activation is applied
      (ie. "linear" activation: `a(x) = x`).
    recurrent_activation: Activation function to use
      for the recurrent step.
      Default: hard sigmoid (`hard_sigmoid`).
      If you pass `None`, no activation is applied
      (ie. "linear" activation: `a(x) = x`).
    use_bias: Boolean, whether the layer uses a bias vector.
    kernel_initializer: Initializer for the `kernel` weights matrix,
      used for the linear transformation of the inputs.
    recurrent_initializer: Initializer for the `recurrent_kernel`
      weights matrix,
      used for the linear transformation of the recurrent state.
    bias_initializer: Initializer for the bias vector.
    unit_forget_bias: Boolean.
      If True, add 1 to the bias of the forget gate at initialization.
      Setting it to true will also force `bias_initializer="zeros"`.
      This is recommended in [Jozefowicz et al., 2015](
        http://www.jmlr.org/proceedings/papers/v37/jozefowicz15.pdf)
    kernel_regularizer: Regularizer function applied to
      the `kernel` weights matrix.
    recurrent_regularizer: Regularizer function applied to
      the `recurrent_kernel` weights matrix.
    bias_regularizer: Regularizer function applied to the bias vector.
    kernel_constraint: Constraint function applied to
      the `kernel` weights matrix.
    recurrent_constraint: Constraint function applied to
      the `recurrent_kernel` weights matrix.
    bias_constraint: Constraint function applied to the bias vector.
    dropout: Float between 0 and 1.
      Fraction of the units to drop for
      the linear transformation of the inputs.
    recurrent_dropout: Float between 0 and 1.
      Fraction of the units to drop for
      the linear transformation of the recurrent state.
  Call arguments:
    inputs: A 2D tensor.
    states: List of state tensors corresponding to the previous timestep.
    training: Python boolean indicating whether the layer should behave in
      training mode or in inference mode. Only relevant when `dropout` or
      `recurrent_dropout` is used.
  """

  def __init__(self,
               units,
               activation='tanh',
               recurrent_activation='hard_sigmoid',
               use_bias=True,
               kernel_initializer='glorot_uniform',
               recurrent_initializer='orthogonal',
               bias_initializer='zeros',
               unit_forget_bias=True,
               kernel_regularizer=None,
               recurrent_regularizer=None,
               bias_regularizer=None,
               kernel_constraint=None,
               recurrent_constraint=None,
               bias_constraint=None,
               frozen_weights = None,
               column = 0,
               layer = 0,               
               dropout=0.,
               recurrent_dropout=0.,
               **kwargs):
    # By default use cached variable under v2 mode, see b/143699808.
    if tf.compat.v1.executing_eagerly_outside_functions():
      self._enable_caching_device = kwargs.pop('enable_caching_device', True)
    else:
      self._enable_caching_device = kwargs.pop('enable_caching_device', False)
    super(LSTMCell, self).__init__(**kwargs)
    self.units = units
    self.activation = activations.get(activation)
    self.recurrent_activation = activations.get(recurrent_activation)
    self.use_bias = use_bias

    self.kernel_initializer = initializers.get(kernel_initializer)
    self.recurrent_initializer = initializers.get(recurrent_initializer)
    self.bias_initializer = initializers.get(bias_initializer)
    self.unit_forget_bias = unit_forget_bias

    self.kernel_regularizer = regularizers.get(kernel_regularizer)
    self.recurrent_regularizer = regularizers.get(recurrent_regularizer)
    self.bias_regularizer = regularizers.get(bias_regularizer)

    self.kernel_constraint = constraints.get(kernel_constraint)
    self.recurrent_constraint = constraints.get(recurrent_constraint)
    self.bias_constraint = constraints.get(bias_constraint)
    self.layer = layer
    self.column = column
    self.frozen_weights  = None
    self.dropout = min(1., max(0., dropout))
    self.recurrent_dropout = min(1., max(0., recurrent_dropout))
    implementation = kwargs.pop('implementation', 1)
    if self.recurrent_dropout != 0 and implementation != 1:
      logging.debug(RECURRENT_DROPOUT_WARNING_MSG)
      self.implementation = 1
    else:
      self.implementation = implementation
    # tuple(_ListWrapper) was silently dropping list content in at least 2.7.10,
    # and fixed after 2.7.16. Converting the state_size to wrapper around
    # NoDependency(), so that the base_layer.__setattr__ will not convert it to
    # ListWrapper. Down the stream, self.states will be a list since it is
    # generated from nest.map_structure with list, and tuple(list) will work
    # properly.
    self.state_size = data_structures.NoDependency([self.units, self.units])
    self.output_size = self.units

  @tf_utils.shape_type_conversion
  def build(self, input_shape):
    default_caching_device = _caching_device(self)
    input_dim = input_shape[-1]
    self.kernel = self.add_weight(
        shape=(input_dim, self.units * 4),
        name='kernel',
        initializer=self.kernel_initializer,
        regularizer=self.kernel_regularizer,
        constraint=self.kernel_constraint,
        caching_device=default_caching_device)
    self.recurrent_kernel = self.add_weight(
        shape=(self.units, self.units * 4),
        name='recurrent_kernel',
        initializer=self.recurrent_initializer,
        regularizer=self.recurrent_regularizer,
        constraint=self.recurrent_constraint,
        caching_device=default_caching_device)

    if self.use_bias:
      if self.unit_forget_bias:
	      def bias_initializer(_, *args, **kwargs):
          return K.concatenate([
              self.bias_initializer((self.units,), *args, **kwargs),
              initializers.get('ones')((self.units,), *args, **kwargs),
              self.bias_initializer((self.units * 2,), *args, **kwargs),
          ])
      else:
        bias_initializer = self.bias_initializer
      self.bias = self.add_weight(
          shape=(self.units * 4,),
          name='bias',
          initializer=bias_initializer,
          regularizer=self.bias_regularizer,
          constraint=self.bias_constraint,
          caching_device=default_caching_device)
    else:
      self.bias = None
    self.built = True

    if self.column > 1 and self.layer > 1:
        if self.frozen_weights is not None:
            if len(frozen_weights) == 1:
                if self.use_bias:
                    if self.unit_forget_bias:
                        for i, trained_weights in enumerate(self.forzen_weights):
                            self.trained_kernel1, self.trained_recurrent_kernel1, self.bias1 = trained_weights
                        k_ti1, k_tf1, k_tc1, k_to1 = tf.split(self.trained_kernel1, num_or_size_splits=4, axis=1)
                        b_ti1, b_tf1, b_tc1, b_to1 = tf.split(self.bias1, num_or_size_splits=4, axis=0)
                        rk_ti1 = self.trained_recurrent_kernel1[:, : self.units]
                        rk_tf1 = self.trained_recurrent_kernel1[:,self.units:self.units*2]
                        rk_tc1 = self.trained_recurrent_kernel1[:,self.units*2:self.units*3]
                        rk_to1 = self.trained_recurrent_kernel1[:,self.units*3:]
                else:
                    self.trained_kernel1, self.trained_recurrent_kernel1 = trained_weights
                    self.bias1 = None
                    k_ti1, k_tf1, k_tc1, k_to1 = tf.split(self.trained_kernel1, num_or_size_splits=4, axis=1)
                    b_ti1 = None
                    b_tf1 = None 
                    b_tc1 = None 
                    b_to1 = None
                    rk_ti1 = self.trained_recurrent_kernel1[:, : self.units]
                    rk_tf1 = self.trained_recurrent_kernel1[:,self.units:self.units*2]
                    rk_tc1 = self.trained_recurrent_kernel1[:,self.units*2:self.units*3]
                    rk_to1 = self.trained_recurrent_kernel1[:,self.units*3:]
            else:
                if self.use_bias:
                    if self.unit_forget_bias:
                        for i, trained_weights in enumerate(self.forzen_weights):
                            if i == 1:
                                self.trained_kernel1, self.trained_recurrent_kernel1, self.bias1 = trained_weights
                            if i == 2:
                                self.trained_kernel2, self.trained_recurrent_kernel2, self.bias2 = trained_weights

                        k_ti1, k_tf1, k_tc1, k_to1 = tf.split(self.trained_kernel1, num_or_size_splits=4, axis=1)
                        b_ti1, b_tf1, b_tc1, b_to1 = tf.split(self.bias1, num_or_size_splits=4, axis=0)
                        rk_ti1 = self.trained_recurrent_kernel1[:, : self.units]
                        rk_tf1 = self.trained_recurrent_kernel1[:,self.units:self.units*2]
                        rk_tc1 = self.trained_recurrent_kernel1[:,self.units*2:self.units*3]
                        rk_to1 = self.trained_recurrent_kernel1[:,self.units*3:]

                        k_ti2, k_tf2, k_tc2, k_to2 = tf.split(self.trained_kernel2, num_or_size_splits=4, axis=1)
                        b_ti2, b_tf2, b_tc2, b_to2 = tf.split(self.bias1, num_or_size_splits=4, axis=0)                  
                        rk_ti2 = self.trained_recurrent_kernel2[:, : self.units]
                        rk_tf2 = self.trained_recurrent_kernel2[:,self.units:self.units*2]
                        rk_tc2 = self.trained_recurrent_kernel2[:,self.units*2:self.units*3]
                        rk_to2 = self.trained_recurrent_kernel2[:,self.units*3:]
                else:
                    for i, trained_weights in enumerate(self.forzen_weights):
                            if i == 1:
                                self.trained_kernel1, self.trained_recurrent_kernel1 = trained_weights
                                self.bias1 = None
                            if i == 2:
                                self.trained_kernel2, self.trained_recurrent_kernel2 = trained_weights
                                self.bias2 = None
                    
                    k_ti1, k_tf1, k_tc1, k_to1 = tf.split(self.trained_kernel1, num_or_size_splits=4, axis=1)
                    rk_ti1 = self.trained_recurrent_kernel1[:, : self.units]
                    rk_tf1 = self.trained_recurrent_kernel1[:,self.units:self.units*2]
                    rk_tc1 = self.trained_recurrent_kernel1[:,self.units*2:self.units*3]
                    rk_to1 = self.trained_recurrent_kernel1[:,self.units*3:]

                    k_ti2, k_tf2, k_tc2, k_to2 = tf.split(self.trained_kernel2, num_or_size_splits=4, axis=1)
                    rk_ti2 = self.trained_recurrent_kernel2[:, : self.units]
                    rk_tf2 = self.trained_recurrent_kernel2[:,self.units:self.units*2]
                    rk_tc2 = self.trained_recurrent_kernel2[:,self.units*2:self.units*3]
                    rk_to2 = self.trained_recurrent_kernel2[:,self.units*3:]
                    b_ti1 = None
                    b_tf1 = None
                    b_tc1 = None
                    b_to1 = None
                    b_ti2 = None
                    b_tf2 = None
                    b_tc2 = None
                    b_to2 = None







