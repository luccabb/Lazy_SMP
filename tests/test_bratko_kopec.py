import unittest
import chess
import main
import lazy_smp

POSITIONS = [
    ("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1", [chess.Move.from_uci("d6d1")]),
    ("3r1k2/4npp1/1ppr3p/p6P/P2PPPP1/1NR5/5K2/2R5 w - - 0 1", [chess.Move.from_uci("d6d5")]),
    ("2q1rr1k/3bbnnp/p2p1pp1/2pPp3/PpP1P1P1/1P2BNNP/2BQ1PRK/7R b - - 0 1", [chess.Move.from_uci("f6f5")]),
    ("rnbqkb1r/p3pppp/1p6/2ppP3/3N4/2P5/PPP1QPPP/R1B1KB1R w KQkq - 0 1", [chess.Move.from_uci("e5e6")]),
    ("r1b2rk1/2q1b1pp/p2ppn2/1p6/3QP3/1BN1B3/PPP3PP/R4RK1 w - - 0 1", [chess.Move.from_uci("a2a4")]),
    ("2r3k1/pppR1pp1/4p3/4P1P1/5P2/1P4K1/P1P5/8 w - - 0 1", [chess.Move.from_uci("g5g6")]),
    ("1nk1r1r1/pp2n1pp/4p3/q2pPp1N/b1pP1P2/B1P2R2/2P1B1PP/R2Q2K1 w - - 0 1", [chess.Move.from_uci("h5f6")]),
    ("4b3/p3kp2/6p1/3pP2p/2pP1P2/4K1P1/P3N2P/8 w - - 0 1", [chess.Move.from_uci("f4f5")]),
    ("2kr1bnr/pbpq4/2n1pp2/3p3p/3P1P1B/2N2N1Q/PPP3PP/2KR1B1R w - - 0 1", [chess.Move.from_uci("f4f5")]),
    ("3rr1k1/pp3pp1/1qn2np1/8/3p4/PP1R1P2/2P1NQPP/R1B3K1 b - - 0 1", [chess.Move.from_uci("c6e5")]),
    ("2r1nrk1/p2q1ppp/bp1p4/n1pPp3/P1P1P3/2PBB1N1/4QPPP/R4RK1 w - - 0 1", [chess.Move.from_uci("f2f4")]),
    ("r3r1k1/ppqb1ppp/8/4p1NQ/8/2P5/PP3PPP/R3R1K1 b - - 0 1", [chess.Move.from_uci("d7f5")]),
    ("r2q1rk1/4bppp/p2p4/2pP4/3pP3/3Q4/PP1B1PPP/R3R1K1 w - - 0 1", [chess.Move.from_uci("b2b4")]),
    ("rnb2r1k/pp2p2p/2pp2p1/q2P1p2/8/1Pb2NP1/PB2PPBP/R2Q1RK1 w - - 0 1", [chess.Move.from_uci("d1d2"), chess.Move.from_uci("d1e1")]),
    ("2r3k1/1p2q1pp/2b1pr2/p1pp4/6Q1/1P1PP1R1/P1PN2PP/5RK1 w - - 0 1", [chess.Move.from_uci("g4g7")]),
    ("r1bqkb1r/4npp1/p1p4p/1p1pP1B1/8/1B6/PPPN1PPP/R2Q1RK1 w kq - 0 1", [chess.Move.from_uci("d2e4")]),
    ("r2q1rk1/1ppnbppp/p2p1nb1/3Pp3/2P1P1P1/2N2N1P/PPB1QP2/R1B2RK1 b - - 0 1", [chess.Move.from_uci("h7h5")]),
    ("r1bq1rk1/pp2ppbp/2np2p1/2n5/P3PP2/N1P2N2/1PB3PP/R1B1QRK1 b - - 0 1", [chess.Move.from_uci("c5b3")]),
    ("3rr3/2pq2pk/p2p1pnp/8/2QBPP2/1P6/P5PP/4RRK1 b - - 0 1", [chess.Move.from_uci("e8e4")]),
    ("r4k2/pb2bp1r/1p1qp2p/3pNp2/3P1P2/2N3P1/PPP1Q2P/2KRR3 w - - 0 1", [chess.Move.from_uci("g3g4")]),
    ("3rn2k/ppb2rpp/2ppqp2/5N2/2P1P3/1P5Q/PB3PPP/3RR1K1 w - - 0 1", [chess.Move.from_uci("f5h6")]),
    ("2r2rk1/1bqnbpp1/1p1ppn1p/pP6/N1P1P3/P2B1N1P/1B2QPP1/R2R2K1 b - - 0 1", [chess.Move.from_uci("b7e4")]),
    ("r1bqk2r/pp2bppp/2p5/3pP3/P2Q1P2/2N1B3/1PP3PP/R4RK1 b kq - 0 1", [chess.Move.from_uci("f7f6")]),
    ("r2qnrnk/p2b2b1/1p1p2pp/2pPpp2/1PP1P3/PRNBB3/3QNPPP/5RK1 w - - 0 1", [chess.Move.from_uci("f2f4")]),
]

class TestChessFunctions(unittest.TestCase):
    def test_negamax(self):
        """
        Engine version: parallel alpha beta, null_move, psqt (with tapered evaluation).
        Results for Bratko-Kopec test cases:

        depth | null_move | score | time
        6 | true | 4 | 2074.589 s
        6 | false | 6 | 3594.249 s
        5 | true | 3 | 361.940 s
        5 | false | 3 | 542.893 s
        4 | true | 1 | 47.956 s
        4 | false | 1 | 53.158 s
        3 | true | 3 | 7.496 s
        3 | false |  3 | 7.614 s

        Engine version: Lazy SMP, negamax, null_move, psqt (with tapered evaluation).
        Results for Bratko-Kopec test cases:

        depth | null_move | score | time
        # 6 | true | 4 | 2074.589 s
        6 | false | 8 | 18935.249 s
        5 | true | 3 | 2119.793 s
        5 | false | 3 | 2920.879 s
        4 | true | 2 | 318.830 s
        4 | false | 1 | 333.154 s
        3 | true | 3 | 44.176 s
        3 | false |  3 | 51.164 s
        """

        correct = 0
        i = 0
        for position, moves in POSITIONS:

            board = chess.Board(position)
            player = -1 if board.turn else 1
            result = lazy_smp.lazy_smp(board, 6, player, False)
            print(str(i)+':', result.uci())
            if result in moves:
                correct += 1
            i += 1
        
        print("Correct Moves: {} of {}".format(correct, len(POSITIONS)))


if __name__ == '__main__':
    unittest.main()

    