############################################################
############################################################
#
# Assign03 for CS525, Spring, 2026
# It is due the 10th of February, 2026
# Note that the due time is always 11:59pm of
# the due date unless specified otherwise.
#
############################################################
############################################################

def lambda_normalize(tm0):
    """
    HX: 10 points
    datatype term =
      | TMvar of strn
      | TMlam of (strn, term)
      | TMapp of (term, term)
    Given a term [tm0], [lambda_normalize] applies the
    leftmost evaluation strategy to normalize it.
    Note that normalization needs to be performed under
    'lambda' as well.
    """
    raise NotImplementedError

############################################################

def ipred_in_lambda():
    """
    HX: 10 points
    This one is what we often call "eat-your-own-dog-food"
    Please implement the predesessor function on integers
    A 'term' is returned by ipred_in_lambda() representing
    the predesessor function (that works on Church numerals).
    """
    raise NotImplementedError

############################################################

def isqrt_in_lambda():
    """
    HX: 20 points
    This one is what we often call "eat-your-own-dog-food"
    Please implement an integer version of the square root
    funtion. For instance,
    isqrt(0) = 0, isqrt(2) = 1, isqrt(10) = 3, ...
    In general, given n >= 0, isqrt(n) returns the largest
    integer x satisfying x * x <= n. Your implementation
    is expected to be effcient; your code may be tested on
    something input as large as 1000000.
    A 'term' is returned by isqrt_in_lambda() representing
    the isqrt function (that works on Church numerals).
    """
    raise NotImplementedError

############################################################
# end of [HWXI/CS525-2026-Spring/assigns/03/assign03.py]
############################################################
