# ===========================
# Multiple options selector
# ===========================


class HandleCategorical:
    """Options to handle categorical data"""

    ONE_HOT = "onehot"
    LABEL = "label"
    TARGET = "target"


class SVMKernel:
    """The function used to map the input to the output"""

    LINEAR = "linear"
    POLY = "poly"
    RBF = "rbf"
    SIGMOID = "sigmoid"


class ANNActivation:
    """The function used to map the input to the output"""

    RELU = "relu"
    TANH = "tanh"
    LOGISTIC = "logistic"


class ANNSolver:
    """The algorithm used to optimize the ANN"""

    ADAM = "adam"
    SGD = "sgd"
    LBFGS = "lbfgs"
