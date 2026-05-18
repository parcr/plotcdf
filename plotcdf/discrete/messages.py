"""Standardized validation messages for discrete random variable inputs.

These constants are consumed by ``plotcdf.discrete.checks`` and related
validation logic to keep error messages consistent across the package.
"""

from typing import Final

support_dim: Final[str] = 'we need a 1-dimensional vector.'
needs_array: Final[str] = 'Please, input data, in any form that can be converted to a 1-dimensional array. This includes lists, ' \
              'lists of tuples, tuples, tuples of tuples, tuples of lists and ndarrays. '
needs_1_dim_array: Final[str] = 'We need a 1-dimensional array'
needs_more_than_1: Final[str] = 'We need a a cardinality greater than 1.'

needs_all_positive: Final[str] = 'We need a vector of probabilities with all values positive.'
needs_lesser_1: Final[str] = 'We need a vector of probabilities with a sum of positive values equal or lesser than 1.'
needs_same_length: Final[str] = 'We need a support and set of probabilities with the same length.'

needs_same_size: Final[str] = 'Both the support and the set of probabilities must have the same size.'

sum_of_prob: Final[str] = 'The error of the sum of the probabilities exceeds the maximum tolerance allowed for the error. ' \
              'So, you should consider to mark at least one of the tails as incomplete.'

tolerance: Final[str] = 'The tolerance needs to be positive and smaller than 1.'

tails: Final[str] = 'The tails should be True or False. It indicates if the tail is complete, that is, if you are using the ' \
        'minimum and/or maximum mass point of the support, for the left and right tail, respectively.' \
        'By default they are both True.'

is_pmf: Final[str] = 'The is_pmf should be True or False. It indicates if you are using the pmf or the cdf. ' \
         'By default is True.'
