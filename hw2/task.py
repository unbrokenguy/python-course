print("Your input:")
user_input = input()


def print_count(func):

    def wrapper(string):
        data = func(string)
        max_v = data[max(data, key=data.get)]
        most_freq_words = {k: v for k, v in data.items() if v == max_v}
        out_str = ' '.join(list(map(lambda k: f'"{k}" with {most_freq_words[k]} entries,', most_freq_words.keys())))
        print(data)
        print(f"Most frequent words in string: {out_str}")

    return wrapper


@print_count
def word_count(string):
    data = {}
    for s in string.split(" "):
        if s in data.keys():
            data[s] += 1
        else:
            data[s] = 1
    return data


word_count(user_input)
