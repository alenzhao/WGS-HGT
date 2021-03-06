"""
Prototype selection

Given a set of n elements (S) and their pairwise distances in terms of a
skbio distance matrix (DM) and a given number (k << n), find the sub-set (s)
consisting of exactly k elements, such that s best represents the full set S.

Here, we define "best represents" as maximizing the sum of distances between
all points, i.e. sum {over a,b in S} DM[a,b]. This is our objective function.

This problem is known to be NP-hard [1], thus we need to resort to heuristics.
This module implements several heuristics, whose quality can be measured by
the objective function for each problem instance, since there is no global
winner. Currently implemented are:
 - prototype_selection_constructive_maxdist
For completeness, the exact but exponential algorithm is implemented, too.
  "prototype_selection_exhaustive"

[1] Gamez, J. Esteban, François Modave, and Olga Kosheleva.
    "Selecting the most representative sample is NP-hard:
     Need for expert (fuzzy) knowledge."
    Fuzzy Systems, 2008. FUZZ-IEEE 2008.
"""

# needed for signature type annotations, but only works for python >= 3.5
# from typing import Sequence, Tuple
from itertools import combinations

import numpy as np
import scipy as sp
from skbio.stats.distance import DistanceMatrix


def distance_sum(elements, dm):
    '''Compute the sum of pairwise distances for the given elements according to
    the given distance matrix.

    Parameters
    ----------
    elements: sequence of str
        List or elements for which the sum of distances is computed.
    dm: skbio.stats.distance.DistanceMatrix
        Pairwise distance matrix.

    Returns
    -------
    float:
        The sum of all pairwise distances of dm for IDs in elements.

    Notes
    -----
    function signature with type annotation for future use with python >= 3.5
    def distance_sum(elements: Sequence[str], dm: DistanceMatrix) -> float:
    '''

    return np.tril(dm.filter(elements).data).sum()


def prototype_selection_exhaustive(dm, num_prototypes,
                                   max_combinations_to_test=200000):
    '''Select k prototypes for given distance matrix

    Parameters
    ----------
    dm: skbio.stats.distance.DistanceMatrix
        Pairwise distances for all elements in the full set S.
    num_prototypes: int
        Number of prototypes to select for distance matrix.
        Must be >= 2, since a single prototype is useless.
        Must be smaller than the number of elements in the distance matrix,
        otherwise no reduction is necessary.
    max_combinations_to_test: int
        The maximal number of combinations to test. If exceeding, the function
        declines execution.

    Returns
    -------
    list of str
        A sequence holding selected prototypes, i.e. a sub-set of the
        elements in the distance matrix.

    Raises
    ------
    RuntimeError
        Combinatorics explode even for small instances. To save the user from
        waiting (almost) forever, this function declines execution if the
        number of combinations to test are too high,
        i.e. > max_combinations_to_test
    ValueError
        The number of prototypes to be found should be at least 2 and at most
        one element smaller than elements in the distance matrix. Otherwise, a
        ValueError is raised.

    Notes
    -----
    This is the reference implementation for an exact algorithm for the
    prototype selection problem. It has an exponential runtime and will only
    operate on small instances (< max_combinations_to_test).
    Idea: test all (n over k) combinations of selecting k elements from n with-
          out replacement. Compute the objective for each such combination and
          report the combination with maximal value.

    function signature with type annotation for future use with python >= 3.5:
    def prototype_selection_exhaustive(dm: DistanceMatrix, num_prototypes: int,
    max_combinations_to_test: int=200000) -> List[str]:
    '''
    if num_prototypes < 2:
        raise ValueError(("'num_prototypes' must be >= 2, since a single "
                          "prototype is useless."))
    if num_prototypes >= len(dm.ids):
        raise ValueError(("'num_prototypes' must be smaller than the number of"
                          " elements in the distance matrix, otherwise no "
                          "reduction is necessary."))

    num_combinations = sp.special.binom(len(dm.ids), num_prototypes)
    if num_combinations >= max_combinations_to_test:
        raise RuntimeError(("Cowardly refuse to test %i combinations. Use a "
                            "heuristic implementation for instances with more "
                            "than %i combinations instead!")
                           % (num_combinations, max_combinations_to_test))

    max_dist, max_set = -1 * np.infty, None
    for s in set(combinations(dm.ids, num_prototypes)):
        d = distance_sum(s, dm)
        if d > max_dist:
            max_dist, max_set = d, s
    return list(max_set)


def prototype_selection_constructive_maxdist(dm, num_prototypes):
    '''Heuristically select k prototypes for given distance matrix.

       Prototype selection is NP-hard. This is an implementation of a greedy
       correctness heuristic: Greedily grow the set of prototypes by adding the
       element with the largest sum of distances to the non-prototype elements.
       Start with the two elements that are globally most distant from each
       other. The set of prototypes is then constructively grown by adding the
       element showing largest sum of distances to all non-prototype elements
       in the distance matrix in each iteration.

    Parameters
    ----------
    dm: skbio.stats.distance.DistanceMatrix
        Pairwise distances for all elements in the full set S.
    num_prototypes: int
        Number of prototypes to select for distance matrix.
        Must be >= 2, since a single prototype is useless.
        Must be smaller than the number of elements in the distance matrix,
        otherwise no reduction is necessary.

    Returns
    -------
    list of str
        A sequence holding selected prototypes, i.e. a sub-set of the
        elements in the distance matrix.

    Raises
    ------
    ValueError
        The number of prototypes to be found should be at least 2 and at most
        one element smaller than elements in the distance matrix. Otherwise, a
        ValueError is raised.

    Notes
    -----
    Timing: %timeit -n 100 prototype_selection_constructive_maxdist(dm, 100)
            100 loops, best of 3: 1.43 s per loop
            where the dm holds 27,398 elements
    function signature with type annotation for future use with python >= 3.5:
    def prototype_selection_constructive_maxdist(dm: DistanceMatrix,
    num_prototypes: int) -> List[str]:
    '''
    if num_prototypes < 2:
        raise ValueError(("'num_prototypes' must be >= 2, since a single "
                          "prototype is useless."))
    if num_prototypes >= len(dm.ids):
        raise ValueError(("'num_prototypes' must be smaller than the number of"
                          " elements in the distance matrix, otherwise no "
                          "reduction is necessary."))

    # initially mark all elements as uncovered, i.e. as not being a prototype
    uncovered = np.asarray([np.True_] * dm.shape[0])

    # the first two prototypes are those elements that have the globally
    # maximal distance in the distance matrix. Mark those two elements as
    # being covered, i.e. prototypes
    distance = dm.data.max()
    res_set = list(np.unravel_index(dm.data.argmax(), dm.data.shape))
    uncovered[res_set] = np.False_
    # counts the number of already found prototypes
    num_found_prototypes = len(res_set)

    # repeat until enough prototypes have been selected:
    #  the new prototype is the element that has maximal distance sum to all
    #  non-prototype elements in the distance matrix.
    while num_found_prototypes < num_prototypes:
        max_elm_idx = (dm.data[res_set, :].sum(axis=0) * uncovered).argmax()
        uncovered[max_elm_idx] = np.False_
        num_found_prototypes += 1
        res_set.append(max_elm_idx)

    # return the ids of the selected prototype elements
    return [dm.ids[idx] for idx, x in enumerate(uncovered) if not x]
