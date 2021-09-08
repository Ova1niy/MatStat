from GroupedSelection import GroupedSelection


if __name__ == '__main__':
    base = 49
    for i in range(6):
        task_path = 'tasks/19_'
        answer_path = 'answers/19_'
        task = GroupedSelection(task_path + str(base + i), answer_path + str(base + i))

    print("You're amazing! Well done")