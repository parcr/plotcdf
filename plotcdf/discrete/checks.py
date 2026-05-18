"""Validation helpers for discrete distribution inputs.

The functions in this module validate user inputs for support values,
probabilities, and related configuration flags used by discrete plotting APIs.
They intentionally raise informative exceptions with standardized messages from
``messages.py``.
"""

from typing import Any, Iterable, Optional

import numpy as np
from . import messages as msn


def support(s: Iterable[Any]) -> np.ndarray:
    """Validate and normalize a support array.

    Parameters
    ----------
    s : iterable
        Input support values.

    Returns
    -------
    numpy.ndarray
        Sorted 1-D array converted to ``float64``.

    Raises
    ------
    ValueError
        If conversion to a NumPy float array fails.
    TypeError
        If the input is not 1-D or has fewer than 2 values.
    """
    try:
        s_ = np.asarray(s, dtype=np.float64)
        s_ = np.sort(s_)
    except ValueError as ve:
        raise ValueError(msn.needs_array + ' ' + str(ve))

    if s_.ndim != 1:
        raise TypeError(msn.needs_1_dim_array)
    elif s_.size == 1:
        raise TypeError(msn.needs_more_than_1)
    else:
        return s_


def prob(p: Iterable[Any], tol: float) -> np.ndarray:
    """Validate and normalize a probability vector.

    Parameters
    ----------
    p : iterable
        Candidate probability values.
    tol : float
        Accepted absolute tolerance when checking whether probabilities sum to 1.

    Returns
    -------
    numpy.ndarray
        Validated probability values as a sorted ``float64`` array.

    Raises
    ------
    ValueError
        If any probability is non-positive or sum checks fail.
    """
    p_ = support(p)
    sum_p = sum(p_)
    if sum(p_ <= 0) > 0:
        raise ValueError(msn.needs_all_positive)
    elif sum_p > 1. + tol:
        # Keep original behavior and message formatting for compatibility.
        message = is_sum_probs_tol(p, tol)
        if sum_p > 1:
            print(f'The sum of the probabilities is {sum_p}>1.')
        if str:
            message = (msn.needs_lesser_1 + ' ' + message).strip()
            raise ValueError(message)
    else:
        return p_


def comp_supp_prob(s: Optional[Iterable[Any]], p: Optional[Iterable[Any]]) -> bool:
    """Check that support and probability arrays have compatible sizes.

    Parameters
    ----------
    s : iterable or None
        Support values.
    p : iterable or None
        Probability values.

    Returns
    -------
    bool
        ``True`` when shapes are compatible.

    Raises
    ------
    TypeError
        If both inputs are provided and their sizes differ.
    """
    if s is not None and p is not None:
        if len(s) != len(p):
            raise TypeError(msn.needs_same_size)
    return True


def is_sum_probs_tol(p: Iterable[float], tol: float) -> str:
    """Build a detailed message when probability sums exceed tolerance.

    Parameters
    ----------
    p : iterable of float
        Probability values.
    tol : float
        Absolute tolerance from 1.0.

    Returns
    -------
    str
        Empty string if valid; otherwise a detailed tolerance error message.
    """
    sum_p = sum(p)
    if abs(sum_p - 1) > tol:
        if sum_p - 1 < 0:
            message = ' The error is ' + str(1 - sum_p) + ' with a tolerance of ' + str(tol) + '.'
            return msn.sum_of_prob + message
        else:
            str_sum_p = str(sum_p)
            str_error_sum_p = str(1. - sum_p)
            return 'The sum of probabilities is ' + str_sum_p + ' with an error of ' + str_error_sum_p + \
                   ' for a max. tolerance of ' + str(tol)
    return ''


def tolerance(t: float) -> float:
    """Validate tolerance bounds.

    Parameters
    ----------
    t : float
        User-defined tolerance.

    Returns
    -------
    float
        The same validated tolerance.

    Raises
    ------
    ValueError
        If tolerance is outside ``[0, 1]``.
    """
    if t > 1 or t < 0:
        raise ValueError(msn.tolerance)
    return t


def tail(t: bool) -> bool:
    """Validate boolean input for tail behavior.

    Parameters
    ----------
    t : bool
        Tail flag.

    Returns
    -------
    bool
        The same validated flag.

    Raises
    ------
    TypeError
        If ``t`` is not boolean.
    """
    if not type(t) == bool:
        raise TypeError(msn.tails)
    return t


def is_pmf(t: bool) -> bool:
    """Validate boolean input indicating PMF mode.

    Parameters
    ----------
    t : bool
        PMF mode flag.

    Returns
    -------
    bool
        The same validated flag.

    Raises
    ------
    TypeError
        If ``t`` is not boolean.
    """
    if not type(t) == bool:
        raise TypeError(msn.is_pmf)
    return t
