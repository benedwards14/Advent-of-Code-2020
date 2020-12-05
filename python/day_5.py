import utils

def get_seat_id(ref: str):
    binary_num = "".join(
        "1" if c in ["B", "R"] else "0" for c in ref
    )
    return int(binary_num, base=2)

if __name__ == "__main__":
    ticketed_seat_ids = {
        get_seat_id(seat_ref) for seat_ref in utils.get_data(5).splitlines()
    }
    all_seat_ids = set(
        range(min(ticketed_seat_ids), max(ticketed_seat_ids) + 1)
    )

    assert max(ticketed_seat_ids) == 861
    assert all_seat_ids - ticketed_seat_ids == {633}