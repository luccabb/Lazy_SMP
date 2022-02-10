from multiprocessing import Manager, Pool, cpu_count
from typing import List, Tuple

from chess import Board, Move

from l1p_alpha_beta import Layer1ParallelAlphaBeta


class Layer2ParallelAlphaBeta(Layer1ParallelAlphaBeta):
        
    def generate_board_and_moves(self, board_list: List[Tuple[Board, Move]]) -> List[Tuple[Board, Move]]: 
        boards_and_moves = []
        og_board, og_move = board_list

        if not og_board.legal_moves:
            boards_and_moves.append((og_board, og_move))

        for move in og_board.legal_moves:
            boards_and_moves.append((og_board, move))
        return boards_and_moves
    

    def search_move(self, board: Board, depth: int, null_move: bool) -> str:
        START_LAYER = 2

        # creating pool of processes
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)

        board_list = [(board, None)]
        for _ in range(START_LAYER):
            arguments = [[(board, move)] for board, move in board_list]
            board_list = pool.starmap(self.generate_board_and_moves, arguments)
            board_list = [board_move for board_move in sum(board_list, [])]

        manager = Manager()
        # create shared hash table
        shared_hash_table = manager.dict()
        arguments = [(board, move, depth-START_LAYER, null_move, shared_hash_table)
            for board, move in board_list]

        parallel_layer_result = pool.starmap(self.get_black_pieces_best_move, arguments)

        parallel_layer_result.sort(key = lambda a: a[1])
        # sorting output and getting best move
        best_move = parallel_layer_result[0][2]

        return best_move
