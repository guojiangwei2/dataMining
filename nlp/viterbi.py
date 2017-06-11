# -*- coding: utf-8 -*-

import numpy as np

"""
% T: array of observations, length `t`
% S: array of states, length `m` (start and end states omitted for clarity)
% V: observations, length `n`
% A(m, m): state transition probability distribution
% B(m, n): observation probability distribution
"""

def viterbi_obs(T, S, A, B):
    """ viterbi function to calculate observation probability
    :parameter T: array of observations, length `t`
    :parameter S: array of states, length `m`
    :parameter A: state transtion probability distribution, m * m
    :parameter B: observation probability distribution, prior probability, m * n
    """
    V = np.zeros(t, m)

    # iterate through each time step
    for i in range(t):
        # iterate through each states, length `m`
        for s in S:
            # calculate the sum of probabilities of having been in every state before,
            # times the state-transition probability
            for s_p in S:
                V[i, s] += V[i-1, s_p] * A[s_p, s]
            # finally multiply that by the probability of seeing the current observation given this state
            V[i, s] *= B[s, T[i]]
    return V


def viterbi_decode(T, S, A, B):
    """user viterbi to decode a series of observations to the most likely series of states
    :parameter T: array of obervations, length `t`
    :parameter S: array of states, length `m`
    :parameter A: state transtion probability distribution, m * m
    :parameter B: observation probability distribution, prior probability, m * n
    """
    t, m = len(T), len(S)
    # initialize the probabilities
    V = np.zeros(t, m)
    # store the back-references to figure out the actural path to get there
    p = np.zeros(t, m)

    # iterate through each time step
    for i in range(t):
        # and consider each state
        for j in range(m):
            s = S[j]
            # get array of probabilities of having been in each previous step,
            # multiplied by probability of transitioning to the current state
            X = np.zeros(m)
            for k in range(m):
                X[k] = V[i-1, k] * A[k, j]
            V[i, s] = np.max(X) * B[s, T[i]]
            P[i, s] = np.argmax(X)

    # build the output sequence by tracing the backpointers of the highest prbabilities at each step
    OS = np.zeros(t)
    OS[t-1] = P[t, np.argmax(V[t])]
    for i in range(1, t)[::-1]:
        OS[i] = P[i, np.argmax(V[i])]

    return [S[idx] for idx in OS]
