import pickle


def write_file_and_metadata():
    print("Input file name:")
    file_name = input()

    with open(file_name, "w") as file:
        lines_count = 0
        user_input = input()
        while user_input != "quit":
            lines_count += 1
            file.write(user_input + "\n")
            user_input = input()
    if lines_count != 0:
        metadata = {"filename": file_name, "number of lines": lines_count}

        with open("metadata.pkl", "wb") as pkl_file:
            pickle.dump(metadata, pkl_file)


def upload_file_and_metadata():
    with open("metadata.pkl", "rb") as pkl_file:
        metadata = pickle.load(pkl_file)
    with open(metadata["filename"], "r") as file:
        lines = file.readlines()
    print(f"File name: {metadata['filename']}\nNumber of lines: {metadata['number of lines']}")
    print("Lines:\n" + "".join(lines))
