"""
Personal Notes:
A fitmon is a list containing elements:
    [affinity_left, cuteness_score, affinity_right]

affinity_left: - positive float in the range of 0.1...0.9 inclusive.
                - only the left-most fitmons[0] will have an affinity_left of 0 as there is 
                no fitmon on the left for it to fuse

Same goes for affinity_right but right-most.

When 2 fitmons fuse:
    - The affinity_left will be based on the affinity_left of the left fitmon,
    affinity_left = fitmons[i][0]
    - The cuteness_score is computed using: cuteness_score = fitmons[i][1] * fitmons[i][2] + fitmons[i+1][1] * fitmons[i+1][0]
    - The affinity_right will be based on the affinity_right of the right fitmon,
    affinity_right = fitmons[i+1][2]

"""

    
def fuse_fitmon_pair(fitmon1: list, fitmon2: list):
    """
    Fuses two fitmons to create a new fitmon following a certain formula.
    The formula:
        new_cuteness_score = fitmon1[1] * fitmon1[2] + fitmon2[1] * fitmon2[0]

    :param fitmon1: List of [left affinity (float), cuteness score (int), right affinity (float)]
    :param fitmon2: List of [left affinity (float), cuteness score (int), right affinity (float)]
    :return: List representing the new fused fitmon.

    :Time complexity: O(1) - The calculations and operations done within this function take constant time
    :Space complexity: O(1) - No additional space is needed/used
    :Auxiliary space complexity: O(1) - Only needs to store a float when calculating new cuteness scoer
    """
    new_cuteness_score = fitmon1[1] * fitmon1[2] + fitmon2[1] * fitmon2[0]
    return [fitmon1[0], int(new_cuteness_score), fitmon2[2]]


def fuse(fitmons):
    """
    Finds the maximum cuteness score possible by chain fusing all possibilities of fitmon fusions.
    All fitmon fusions done are only possible when the fitmons in the given list are adjacent.
    This function calculates all possible combinations of fitmon fusions and stores the results in a 2d array to avoid redundant calculations/operations

    Approach Description:
    The function calculates and keeps track of the optimal cuteness scores for each depth of fusions. It keeps track by
    storing each result in a 2D array.

    Example:
    Given input list of length 4 (a, b, c, d):
    For every iteration, fuse all combinations of adjacent fitmons and take the maximum possible combination.
    1st iteration:  We try to get a fusion of length 2 (here it'd be ab, bc, cd)
                     a and b -> ab; b and c -> bc; c and d -> cd
                     we store these within the 2d array.
                    # |a|_|_|_|
                    # |-|b|_|_|
                    # |-|-|c|_|
                    # |-|-|-|d|

    2nd iteration: Now we try to get a higher depht of fusion by incrementing it (3) (here it'd be abc, bcd)
                    So we compare all combinations for example when trying to get ABC:
                    we get max between (AB)C and A(BC) as thats all the possible combinations to make ABC.
                    and we keep going for further combinations.
                    # |a|ab|x |_ |
                    # |-|b |bc|y |
                    # |-|- |c |cd|
                    # |-|- |- |d |

                    x = max((AB)C, A(BC)); y = max(A(BC)); (all combinations possible to make length 3 which are adjacent)

    :param fitmons: List of lists, where each inner list represents a fitmon: [float (left affinity), int (cuteness score), float (right affinity)].
    :return: int representing the maximum cuteness score possible through chain fusions.

    :Time complexity: O(N^3) - The function includes three nested loops that depend on the number of fitmons
    N: number of fitmons in the input list

    :Space complexity: O(N^2) - Uses a 2D array
     
    :Auxiliary space complexity: O(N^2) - Uses a 2D Array
    """
    arr_2d = []
    # Initialize 2D Array    
    # |a|_|_|_|
    # |-|b|_|_|
    # |-|-|c|_|
    # |-|-|-|d|

    for i in range(len(fitmons)):
        arr_2d.append([None for _ in range(len(fitmons))])
        arr_2d[i][i] = fitmons[i]

    for k in range(len(fitmons)-1):
        i = 0 # Reset starting row
        j = k # Shift starting column to the right
        for _ in range(k, len(fitmons) - 1):
            curr_max_cuteness = 0
            x = 1
            for y in range(i, (j+1)):
                new_cuteness_score = arr_2d[i][y][1] * arr_2d[i][y][2] + arr_2d[i+x][j+1][1] * arr_2d[i + x][j+1][0]
                if new_cuteness_score > curr_max_cuteness:
                    curr_max_cuteness = new_cuteness_score
                    arr_2d[i][j+1] = fuse_fitmon_pair(arr_2d[i][y], arr_2d[i + x][j+1])
                    # Row i, column j+1 represents the next coordinates we're going to fill.
                    # |a|i, j+1|_|_|
                    # |-|b     |_|_|
                    # |-|-     |c|_|
                    # |-|-     |-|d|
                    # Goes right-downwardsd diagonally after each iteration
                x += 1
            j += 1
            i += 1

    # Returns the maximum output which is in the top right of the 2D array
    return arr_2d[0][len(fitmons)-1][1]

if __name__ == "__main__":
    fitmons = [
        [0, 29, 0.9],
        [0.9, 91, 0.8],
        [0.8, 48, 0.2],
        [0.2, 322, 0]
    ]

    res = (fuse([[0, 50, 0.6], [0.6, 98, 0.4], [0.4, 54, 0.9], [0.9, 6, 0.3], [0.3, 34, 0.5], [0.5, 66, 0.3]]))

    print(res)


