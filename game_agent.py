"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

INF = float("inf")


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def distance(pos1, pos2):
    return (abs(pos1[0]-pos2[0]), abs(pos1[1]-pos2[1]))


def player_distance(game, player):
    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))
    return distance(player_location, opponent_location)


def manhatten_distance_to_center(game, player):
    player_location = game.get_player_location(player)
    center = (game.width // 2, game.height // 2)
    dist = distance(player_location, center)
    return max(0.001, float(dist[0] + dist[1]))


def start_position_center(game, player, second_move="orthogonal"):
    assert game.move_count < 2

    center = (game.width // 2, game.height // 2)
    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))
    blank_spaces = game.get_blank_spaces()
    move_count = game.move_count

    if (second_move=="one_move_away" and game.move_count == 1) or center in blank_spaces:
        return 1000.0 if player_location == center else -1000.0
    else:
        assert oppponent_location is not None
        if second_move == "one_move_away":
            dist = player_distance(game, player)
            return 1000.0 if max(dist) == 2 and min(dist==1) else -1000.0
        else:
            if second_move == "orthogonal":
                next_fields = ((2,3),(4,3),(3,2),(3,4))
            elif second_move == "diagonal":
                next_fields = ((2,2),(4,4),(2,4),(4,2))
            else:
                assert(False)

            return 1000.0 if player_location in next_fields else -1000.0


def player_moves(game, player):
    return game.get_legal_moves(player)


def opponent_moves(game, player):
    return game.get_legal_moves(game.get_opponent(player))


def move_difference(game, player):
    return float(len(player_moves(game, player)) - len(opponent_moves(game, player)))


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_winner(player):
        return INF
    elif game.is_loser(player):
        return -INF

    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    distance = max(abs(player_location[0]-opponent_location[0]), abs(player_location[1]-opponent_location[1]))

    return float(len(player_moves) - len(opponent_moves)) * 1.0 / distance


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

#    if game.move_count < 2:
#        return start_position_center(game, player,second_move="orthogonal")

    if game.is_winner(player):
        return INF
    elif game.is_loser(player):
        return -INF

    return 1.0 / manhatten_distance_to_center(game,player)


    # # TODO: finish this function!
    # if game.is_winner(player):
    #     return INF
    # elif game.is_loser(player):
    #     return -INF
    #
    # return float(game.height * game.width - game.move_count)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return INF
    elif game.is_loser(player):
        return -INF

    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    return float(len(player_moves) - 2.0 * len(opponent_moves))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def __min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        min_score = float("inf")
        for m in game.get_legal_moves():
            new_game = game.forecast_move(m)
            min_score = min(min_score, self.__max_value(new_game, depth-1))

        return min_score


    def __max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        max_score = float("-inf")
        for m in game.get_legal_moves():
            new_game = game.forecast_move(m)
            max_score = max(max_score, self.__min_value(new_game, depth-1))

        return max_score





    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        max_score = float("-inf")
        best_move = (-1,-1)
        for m in game.get_legal_moves():
            new_game = game.forecast_move(m)
            u = self.__min_value(new_game, depth-1)
            if u >= max_score:
                max_score = u
                best_move = m

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def __min_value(self, game, alpha, beta, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return self.score(game, self), (-1,-1)
        elif depth == 0:
            best_move = legal_moves[0]
            return self.score(game, self), best_move

        min_value = INF
        best_move = (-1,-1)
        for move in legal_moves:
            if best_move == (-1,-1):
                best_move = move
            new_game = game.forecast_move(move)
            current_value, _ = self.__max_value(new_game, alpha, beta, depth-1)

            if current_value <= min_value:
                min_value = current_value
                best_move = move

            if min_value <= alpha:
                return min_value, best_move

            beta = min(beta, min_value)

        return min_value, best_move


    def __max_value(self, game, alpha, beta, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return self.score(game, self), (-1,-1)
        elif depth == 0:
            best_move = legal_moves[0]
            return self.score(game, self), best_move

        max_value = -INF
        best_move = (-1,1)
        for move in legal_moves:
            if best_move == (-1,-1):
                best_move = move
            new_game = game.forecast_move(move)
            current_value, _ = self.__min_value(new_game, alpha, beta, depth-1)

            if current_value >= max_value:
                max_value = current_value
                best_move = move

            if max_value >= beta:
                return max_value, best_move

            alpha = max(alpha, max_value)

        return max_value, best_move


    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        best_score = -INF

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        best_move = legal_moves[0]
        depth = 0
        while True:
            try:
                best_move = self.alphabeta(game, depth)
            except SearchTimeout:
                return best_move
                break

            depth += 1

        return best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        # TODO: finish this function!
        _, best_move = self.__max_value(game, -INF, INF, depth)

        return best_move
