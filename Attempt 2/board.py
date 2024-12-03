from copy import deepcopy

class BoardState:
    def __init__(self, count, num_dead_white, num_dead_black, put_out_white, put_out_black):
        self.count = count
        self.num_dead_white = num_dead_white
        self.num_dead_black = num_dead_black
        self.put_out_white = put_out_white
        self.put_out_black = put_out_black

    def get_counts_array(self):
        return deepcopy(self.count)

    def get_count_at(self, position):
        return abs(self.count[position])

    def is_position_white(self, position):
        return self.count[position] > 0

    def is_position_black(self, position):
        return self.count[position] < 0

    def get_num_dead(self, white):
        return self.num_dead_white if white else self.num_dead_black

    def num_put_aside(self, white):
        return self.put_out_white if white else self.put_out_black

    def __str__(self):
        return BoardUtils.get_nice_view_of_board(self)


class BoardUtils:
    BOARD_SIZE = 24
    NUM_PIECES = 15

    @staticmethod
    def get_starting_position_board():
        count = [0] * BoardUtils.BOARD_SIZE
        count[0] = 2
        count[23] = -2
        count[5] = count[12] = -5
        count[18] = count[11] = 5
        count[7] = -3
        count[16] = 3
        return BoardState(count, 0, 0, 0, 0)

    @staticmethod
    def append_stuff(sb, state, from_idx, to_idx):
        for index in range(from_idx, to_idx + 1):
            count = state.get_count_at(index)
            pieces = "--" if count == 0 else f"{count}{'W' if state.is_position_white(index) else 'B'}"
            sb.append(f"{pieces} ")

    @staticmethod
    def append_stuff_reverse(sb, state, from_idx, to_idx):
        for index in range(to_idx, from_idx - 1, -1):
            count = state.get_count_at(index)
            pieces = "--" if count == 0 else f"{count}{'W' if state.is_position_white(index) else 'B'}"
            sb.append(f"{pieces} ")

    @staticmethod
    def get_board_after_moving_single_piece(state, board_index, move_length):
        whites_turn = state.is_position_white(board_index)
        dest_index = board_index + move_length if whites_turn else board_index - move_length
        count = state.get_counts_array()
        num_dead_white, num_dead_black = state.get_num_dead(True), state.get_num_dead(False)

        if whites_turn:
            if count[dest_index] < 0:
                num_dead_black += 1
                count[dest_index] = 0
            count[board_index] -= 1
            count[dest_index] += 1
        else:
            if count[dest_index] > 0:
                num_dead_white += 1
                count[dest_index] = 0
            count[board_index] += 1
            count[dest_index] -= 1

        return BoardState(count, num_dead_white, num_dead_black, state.num_put_aside(True), state.num_put_aside(False))

    @staticmethod
    def get_nice_view_of_board(state):
        sb = []
        BoardUtils.append_stuff_reverse(sb, state, 6, 11)
        sb.append(" | ")
        BoardUtils.append_stuff_reverse(sb, state, 0, 5)
        sb.append("\n")
        for _ in range(3):
            sb.extend(["|| "] * 6)
            sb.append(" | ")
            sb.extend(["|| "] * 6)
            sb.append("\n")
        BoardUtils.append_stuff(sb, state, 12, 17)
        sb.append(" | ")
        BoardUtils.append_stuff(sb, state, 18, 23)
        sb.append("\n")
        return "".join(sb)
