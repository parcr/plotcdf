"""Utilities to model and plot discrete random variables.

This module exposes the :class:`RV` class, which validates support/probability
inputs and renders PMF, CDF, and quantile plots with configurable Matplotlib
style dictionaries.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Any, Dict, Iterable, Optional, Tuple

from . import checks
import numpy as np
import matplotlib.pyplot as plt
from library import systems
import logging


class RV:
    """Discrete random variable model with PMF/CDF/quantile plotting helpers.

    Parameters
    ----------
    support : iterable
        Support values (mass points) for the random variable.
    prob : iterable of float
        PMF values when ``is_pmf=True`` or CDF values when ``is_pmf=False``.
    is_pmf : bool, default=True
        Whether ``prob`` represents PMF values.
    complete_left : bool, default=True
        Whether the left tail is complete.
    complete_right : bool, default=True
        Whether the right tail is complete.
    max_tol : float, default=1e-12
        Tolerance used when checking probability sum consistency.
    """

    def __new__(
        cls,
        support: Iterable[Any],
        prob: Iterable[float],
        is_pmf: bool = True,
        complete_left: bool = True,
        complete_right: bool = True,
        max_tol: float = 1e-12,
    ) -> 'RV':
        """Validate initialization inputs before creating an instance."""
        messages: list[str] = []

        if not is_pmf:
            try:
                # Normalize CDF input into PMF so downstream checks stay unified.
                p = np.array(prob)
                prob = np.append(p[0], p[1:] - p[:-1])
            except TypeError as e:
                messages.append('We need a type that can be converted to a numpy array. ' + str(e))

        try:
            checks.support(support)
        except(ValueError, TypeError) as e:
            messages.append(str(e))

        try:
            checks.prob(prob, max_tol)
        except(ValueError, TypeError) as e:
            messages.append(str(e))

        try:
            checks.comp_supp_prob(support, prob)
        except TypeError as e:
            messages.append(str(e))

        try:
            checks.tolerance(max_tol)
        except ValueError as e:
            messages.append(str(e))

        try:
            checks.tail(complete_left)
        except TypeError as e:
            messages.append(str(e))

        try:
            checks.tail(complete_right)
        except TypeError as e:
            messages.append(str(e))

        try:
            checks.is_pmf(is_pmf)
        except TypeError as e:
            messages.append(str(e))

        if not messages:
            return object.__new__(cls)

        logging.critical(messages)
        raise ValueError('; '.join(messages))

    def __init__(
        self,
        support: Iterable[Any],
        prob: Iterable[float],
        is_pmf: bool = True,
        complete_left: bool = True,
        complete_right: bool = True,
        max_tol: float = 1e-12,
    ) -> None:
        """Initialize a validated random variable and cached cumulative probabilities."""
        self.support = support
        self.__tol = max_tol
        self.__is_pmf = is_pmf
        self.prob = prob
        self.__warning = checks.is_sum_probs_tol(self.prob, max_tol)
        if self.is_pmf:
            self.__cum_prob = self.from_pmf_to_cdf(self.prob)
        else:
            self.__cum_prob = np.array(prob)
        self.complete_left = complete_left
        self.complete_right = complete_right
        if self.__warning:
            logging.warning(self.__warning)

    def __str__(self) -> str:
        msg = 'A discrete Point Mass Function: ' + self.__repr__()
        # return super().__str__()
        return msg

    def __repr__(self) -> str:
        msg = "{}({}, {}, {}, {}, {}, {})".format(self.__class__.__name__, self.__support, self.__prob,
                                                  self.__is_pmf, self.complete_left, self.complete_right, self.tol)
        # return super().__repr__()
        return msg

    @property
    def warning(self) -> str:
        """Return warning text when probabilities do not sum to one within tolerance."""
        return self.__warning

    @property
    def support(self) -> np.ndarray:
        """Return validated support values."""
        return self.__support

    @support.setter
    def support(self, s: Iterable[Any]) -> None:
        s = checks.support(s)
        try:
            p = self.prob
            try:
                checks.comp_supp_prob(s, p)
                self.__support = s
            except (ValueError, TypeError) as e:
                print(e)
        except AttributeError as e:
            self.__support = s

    @property
    def is_pmf(self) -> bool:
        """Whether input probabilities represent PMF values."""
        return self.__is_pmf

    @property
    def prob(self) -> Any:
        """Return validated PMF values."""
        return self.__prob

    @prob.setter
    def prob(self, p: Any) -> None:
        if not self.is_pmf:
            p = self.from_cdf_to_pmf(p)
        checks.support(p)
        try:
            checks.prob(p, self.tol)
        except(ValueError, TypeError) as e:
            print(e)
            return
        try:
            s = self.support
            try:
                checks.comp_supp_prob(s, p)
                self.__prob = p
            except (ValueError, TypeError) as e:
                print(e)
        except AttributeError as e:
            self.__prob = p

    @property
    def cum_prob(self) -> Any:
        """Return cumulative probabilities."""
        return self.__cum_prob

    @property
    def tol(self) -> float:
        """Return tolerance used in probability sum checks."""
        return self.__tol

    @property
    def complete_left(self) -> bool:
        """Whether the left tail is complete."""
        return self.__complete_left

    @complete_left.setter
    def complete_left(self, t: bool) -> None:
        try:
            checks.tail(t)
            self.__complete_left = t
        except TypeError as e:
            print(e)

    @property
    def complete_right(self) -> bool:
        """Whether the right tail is complete."""
        return self.__complete_right

    @complete_right.setter
    def complete_right(self, t: bool) -> None:
        try:
            checks.tail(t)
            self.__complete_right = t
        except TypeError as e:
            print(e)

    @staticmethod
    def from_pmf_to_cdf(probs: Iterable[float]) -> np.ndarray:
        """Convert PMF values into CDF values.

        Parameters
        ----------
        probs : iterable of float
            Point-mass probabilities.

        Returns
        -------
        numpy.ndarray
            Cumulative probabilities.
        """
        probs = np.array(probs)
        return np.cumsum(probs)

    @staticmethod
    def from_cdf_to_pmf(cum_probs: Iterable[float]) -> np.ndarray:
        """Convert CDF values into PMF values.

        Parameters
        ----------
        cum_probs : iterable of float
            Cumulative probabilities.

        Returns
        -------
        numpy.ndarray
            Point-mass probabilities.
        """
        cum_probs = np.array(cum_probs)
        return np.append(cum_probs[0], cum_probs[1:] - cum_probs[:-1])

    def plot_cdf(
        self,
        rv_name: str = 'X',
        graph_name: str = '',
        left_points: Dict[str, Any] = dict(),
        right_points: Dict[str, Any] = dict(),
        hlines: Dict[str, Any] = dict(),
        left_line_complete: Dict[str, Any] = dict(),
        right_line_complete: Dict[str, Any] = dict(),
        left_line_incomplete: Dict[str, Any] = dict(),
        right_line_incomplete: Dict[str, Any] = dict(),
        grid: Dict[str, Any] = dict(),
        x_y_ticks: int = 10,
        save: bool = True,
    ) -> Tuple[Any, Any]:
        """Plot the cumulative distribution function.

        Parameters
        ----------
        rv_name : str, default='X'
            Variable name used in the plot title.
        graph_name : str, default=''
            Prefix used when saving the output image.
        left_points, right_points, hlines, left_line_complete, right_line_complete, left_line_incomplete, right_line_incomplete, grid : dict
            Matplotlib style dictionaries for corresponding elements.
        x_y_ticks : int, default=10
            Maximum number of support values to auto-apply as ticks.
        save : bool, default=True
            Whether to save the generated plot as a PNG file.

        Returns
        -------
        tuple
            Matplotlib ``(figure, axes)``.
        """
        increment = np.average(np.diff(self.__support))
        ext_support = np.append(self.__support, self.__support[-1] + increment)
        ext_support = np.insert(ext_support, 0, self.__support[0] - increment)
        ext_probabilities = np.insert(self.__cum_prob, 0, 0)

        fig, ax = plt.subplots()
        if 'markerfacecolor' not in left_points:
            left_points['markerfacecolor'] = 'black'
        if 'markeredgecolor' not in left_points:
            left_points['markeredgecolor'] = 'black'
        if 'marker' not in left_points:
            left_points['marker'] = 'o'

        if 'markerfacecolor' not in right_points:
            right_points['markerfacecolor'] = 'white'
        if 'markeredgecolor' not in right_points:
            right_points['markeredgecolor'] = 'black'
        if 'marker' not in right_points:
            right_points['marker'] = 'o'

        if 'linestyle' not in left_line_complete:
            left_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in left_line_complete:
            left_line_complete['linewidth'] = 2
        if 'color' not in left_line_complete:
            left_line_complete['color'] = 'k'

        if 'linestyle' not in right_line_complete:
            right_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in right_line_complete:
            right_line_complete['linewidth'] = 2
        if 'color' not in right_line_complete:
            right_line_complete['color'] = 'k'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if 'linewidth' not in hlines:
            hlines['linewidth'] = 2
        if 'color' not in hlines:
            hlines['color'] = 'k'

        if 'which' not in grid:
            grid['which'] = 'both'
        if 'axis' not in grid:
            grid['axis'] = 'both'
        if 'color' not in grid:
            grid['color'] = 'grey'
        if 'linestyle' not in grid:
            grid['linestyle'] = '-'
        if 'linewidth' not in grid:
            grid['linewidth'] = .1

        ax.plot(ext_support[1], ext_probabilities[0], **right_points)
        if self.complete_left:
            ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], **left_line_complete)
        else:
            ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], **left_line_incomplete)
        if self.complete_right:
            ax.hlines(y=1, xmin=ext_support[ext_support.size - 2], xmax=ext_support[ext_support.size - 1],
                      **right_line_complete)
        else:
            ax.hlines(y=ext_probabilities[-1], xmin=ext_support[ext_support.size - 2],
                      xmax=ext_support[ext_support.size - 1], **right_line_incomplete)
        for x in range(1, ext_support.size - 2):
            ax.plot(ext_support[x], ext_probabilities[x], **left_points)
            ax.plot(ext_support[x + 1], ext_probabilities[x], **right_points)
            ax.hlines(y=ext_probabilities[x], xmin=ext_support[x], xmax=ext_support[x + 1], **hlines)
        plt.plot(ext_support[ext_support.size - 2], ext_probabilities[ext_support.size - 2], **left_points)
        plt.title('Cumulative Distribution Function for ' + rv_name.upper())
        plt.xlabel('x')
        plt.ylabel('F(x)')

        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__support)
            ax.set_yticks(self.__cum_prob)
        if grid:
            plt.grid(visible=True, **grid)
        if systems.is_windows():
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
            plt.tight_layout()

        if save:
            file_name = graph_name + '_cdf_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        # plt.show()
        return fig, ax

    def plot_pmf(
        self,
        rv_name: str = 'X',
        graph_name: str = '',
        points: Dict[str, Any] = dict(),
        left_line_incomplete: Dict[str, Any] = dict(),
        right_line_incomplete: Dict[str, Any] = dict(),
        grid: Optional[Dict[str, Any]] = dict(),
        x_y_ticks: int = 10,
        save: bool = True,
    ) -> Tuple[Any, Any]:
        """Plot the probability mass function.

        Parameters
        ----------
        rv_name : str, default='X'
            Variable name used in the plot title.
        graph_name : str, default=''
            Prefix used when saving the output image.
        points, left_line_incomplete, right_line_incomplete, grid : dict
            Matplotlib style dictionaries for corresponding elements.
        x_y_ticks : int, default=10
            Maximum number of support values to auto-apply as ticks.
        save : bool, default=True
            Whether to save the generated plot as a PNG file.

        Returns
        -------
        tuple
            Matplotlib ``(figure, axes)``.
        """

        fig, ax = plt.subplots()
        if 'color' not in points:
            points['color'] = 'black'
        if 'marker' not in points:
            points['marker'] = 'o'
        if 'linestyle' not in points:
            points['linestyle'] = '--'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if grid is not None:
            if 'which' not in grid:
                grid['which'] = 'both'
            if 'axis' not in grid:
                grid['axis'] = 'both'
            if 'color' not in grid:
                grid['color'] = 'grey'
            if 'linestyle' not in grid:
                grid['linestyle'] = '-'
            if 'linewidth' not in grid:
                grid['linewidth'] = .1

        # plt.bar(self.__support, self.__prob, width=.1, color='k')
        plt.plot(self.support, self.__prob, **points)  # 'ko--'
        plt.title('Probability Mass Function for ' + rv_name.upper())
        plt.xlabel('x')
        plt.ylabel('P(X=x)')
        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__support)
            ax.set_yticks(self.__prob)
        if not self.__complete_left:
            increment = np.average(np.diff(self.__support))
            ax.hlines(y=self.__prob[0], xmin=self.__support[0] - increment,
                      xmax=self.__support[0], **left_line_incomplete)
        if not self.__complete_right:
            increment = np.average(np.diff(self.__support))
            ax.hlines(y=self.__prob[-1], xmin=self.__support[len(self.__support) - 1],
                      xmax=self.__support[len(self.__support) - 1] + increment,
                      **right_line_incomplete)
        if grid:
            plt.grid(visible=True, **grid)

        if systems.is_windows():
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
            plt.tight_layout()

        if save:
            file_name = graph_name + '_pmf_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        # plt.show()
        return fig, ax

    def plot_quantile(
        self,
        rv_name: str = 'X',
        graph_name: str = '',
        left_points: Dict[str, Any] = dict(),
        right_points: Dict[str, Any] = dict(),
        hlines: Dict[str, Any] = dict(),
        left_line_complete: Dict[str, Any] = dict(),
        right_line_complete: Dict[str, Any] = dict(),
        left_line_incomplete: Dict[str, Any] = dict(),
        right_line_incomplete: Dict[str, Any] = dict(),
        grid: Dict[str, Any] = dict(),
        x_y_ticks: int = 10,
        save: bool = True,
    ) -> Tuple[Any, Any]:
        """Plot the quantile function.

        Parameters
        ----------
        rv_name : str, default='X'
            Variable name used in the plot title.
        graph_name : str, default=''
            Prefix used when saving the output image.
        left_points, right_points, hlines, left_line_complete, right_line_complete, left_line_incomplete, right_line_incomplete, grid : dict
            Matplotlib style dictionaries for corresponding elements.
        x_y_ticks : int, default=10
            Maximum number of support values to auto-apply as ticks.
        save : bool, default=True
            Whether to save the generated plot as a PNG file.

        Returns
        -------
        tuple
            Matplotlib ``(figure, axes)``.
        """
        increment = np.average(np.diff(self.__cum_prob))
        # ext_probabilities = np.append(self.__cum_prob, self.__cum_prob[-1] + increment)
        ext_probabilities = np.insert(self.__cum_prob, 0, self.__cum_prob[0] - increment)
        ext_support = np.insert(self.__support, 0, self.__support[0])

        fig, ax = plt.subplots()
        if 'markerfacecolor' not in left_points:
            left_points['markerfacecolor'] = 'white'
        if 'markeredgecolor' not in left_points:
            left_points['markeredgecolor'] = 'black'
        if 'marker' not in left_points:
            left_points['marker'] = 'o'

        if 'markerfacecolor' not in right_points:
            right_points['markerfacecolor'] = 'black'
        if 'markeredgecolor' not in right_points:
            right_points['markeredgecolor'] = 'black'
        if 'marker' not in right_points:
            right_points['marker'] = 'o'

        if 'linestyle' not in left_line_complete:
            left_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in left_line_complete:
            left_line_complete['linewidth'] = 2
        if 'color' not in left_line_complete:
            left_line_complete['color'] = 'k'

        if 'linestyle' not in right_line_complete:
            right_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in right_line_complete:
            right_line_complete['linewidth'] = 2
        if 'color' not in right_line_complete:
            right_line_complete['color'] = 'k'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if 'linewidth' not in hlines:
            hlines['linewidth'] = 2
        if 'color' not in hlines:
            hlines['color'] = 'k'

        if 'which' not in grid:
            grid['which'] = 'both'
        if 'axis' not in grid:
            grid['axis'] = 'both'
        if 'color' not in grid:
            grid['color'] = 'grey'
        if 'linestyle' not in grid:
            grid['linestyle'] = '-'
        if 'linewidth' not in grid:
            grid['linewidth'] = .1

        ax.plot(ext_probabilities[1], ext_support[0], **right_points)
        if self.complete_left:
            ax.hlines(y=ext_support[0], xmin=ext_probabilities[0], xmax=ext_probabilities[1], **left_line_complete)
        else:
            ax.hlines(y=ext_support[0], xmin=ext_probabilities[0], xmax=ext_probabilities[1], **left_line_incomplete)
        if self.complete_right:
            ax.hlines(y=ext_support[-1], xmin=ext_probabilities[ext_probabilities.size - 2],
                      xmax=ext_probabilities[ext_probabilities.size - 1] + increment, **right_line_complete)
        else:
            ax.hlines(y=ext_support[-1], xmin=ext_probabilities[ext_probabilities.size - 2],
                      xmax=ext_probabilities[ext_probabilities.size - 1] + increment, **right_line_incomplete)
        for x in range(1, ext_probabilities.size - 2):
            ax.plot(ext_probabilities[x], ext_support[x + 1], **left_points)
            ax.plot(ext_probabilities[x + 1], ext_support[x + 1], **right_points)
            ax.hlines(y=ext_support[x + 1], xmin=ext_probabilities[x], xmax=ext_probabilities[x + 1], **hlines)
        plt.plot(ext_probabilities[ext_probabilities.size - 2], ext_support[ext_probabilities.size - 1], **left_points)
        plt.title('Quantile Function for ' + rv_name.upper())
        plt.xlabel('p')
        plt.ylabel('$F\\overleftarrow{(p)}$')

        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__cum_prob)
            ax.set_yticks(self.__support)
        if grid:
            plt.grid(visible=True, **grid)
        if systems.is_windows():
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
            plt.tight_layout()

        if save:
            file_name = graph_name + '_quantile_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        # plt.show()
        return fig, ax
