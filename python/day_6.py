import utils


if __name__ == "__main__":
    answer_groups = [
        [
            set(person_answers)
            for person_answers in group_answers.split()
        ]
        for group_answers in utils.get_data(6).split("\n\n")
    ]

    assert sum(len(set.union(*group)) for group in answer_groups) == 6662
    assert sum(len(set.intersection(*group)) for group in answer_groups) == 3382