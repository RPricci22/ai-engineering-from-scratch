from data_utils import load_and_inspect as lai
from datasets import load_dataset
import time


def Excercise1():
    data = lai("nyu-mll/glue", "mrpc")
    print(data[:5])


def Excercise2():

    start_time = time.time()
    count = 0
    duration = 10  # in seconds

    retrieved_data = []

    ds = load_dataset("allenai/c4", "en", split="train", streaming=True)

    for row in ds:
        count += 1
        if time.time() - start_time > duration:
            break
        retrieved_data.append(row)

    print("Count:", count)
    print("Time elapsed:", time.time() - start_time)
    print("Retrieved data:", retrieved_data[:1])


def Excercise3():
    import os
    from datasets import load_dataset

    dataset = load_dataset(
        "stanfordnlp/imdb", split="train"
    )  # Downloads and loads the IMDB dataset from Hugging Face
    # print(dataset[:2])

    dataset.to_csv("imdb_dataset.csv")
    dataset.to_parquet("imdb_dataset.parquet")
    dataset.to_json("imdb_dataset.json")

    filesizes = []

    print("Files created:")
    for file in ["imdb_dataset.csv", "imdb_dataset.parquet", "imdb_dataset.json"]:
        if os.path.exists(file):
            size = os.path.getsize(file)
            filesizes.append((file, size))
            print(file, "Size:", size)

    print("Filesizes:", filesizes)

    # compare no. of rows in each file including initial dataset
    import pandas as pd

    initial_no_of_rows = len(dataset)
    print("Initial dataset number of rows:", initial_no_of_rows)

    for file in ["imdb_dataset.csv", "imdb_dataset.parquet", "imdb_dataset.json"]:
        if os.path.exists(file):
            if file.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.endswith(".parquet"):
                df = pd.read_parquet(file)
            elif file.endswith(".json"):
                df = pd.read_json(file, lines=True)
            print(
                file,
                "Number of rows:",
                len(df),
                "Matches initial dataset:",
                len(df) == initial_no_of_rows,
            )


def Excercise4():
    from datasets import load_dataset

    dataset = load_dataset(
        "stanfordnlp/imdb", split="train"
    )  # Downloads and loads the IMDB dataset from Hugging Face

    def run_spilt(seeds: list[int]) -> None:
        # Dict to store the first row of each split for each seed
        seed_samples = {}

        for seed in seeds:
            print(f"Running split with seed: {seed}")
            split = dataset.train_test_split(test_size=0.3, seed=seed)
            # Takes the full dataset and divides it into two parts using a random seed (42) for reproducibility.
            # test_size=0.3: Sets aside 30% of the data as the final test set (split["test"])
            # The remaining 70% becomes the working training pool (split["train"]).

            train_val = split["train"].train_test_split(test_size=0.5, seed=seed)
            # Takes that remaining 80% pool (split["train"]) and splits it again.
            # test_size=0.5: Sets aside 50% of the 70% training pool as the validation set (val_ds)
            # The remaining 50% of the 70% pool becomes the final training set (train_ds)

            train_ds = train_val["train"]
            val_ds = train_val["test"]
            test_ds = split["test"]

            print(f"Original dataset size: {len(dataset)}")
            print(f"Train: {len(train_ds)}, Val: {len(val_ds)}, Test: {len(test_ds)}")

            if len(dataset) != len(train_ds) + len(val_ds) + len(test_ds):
                print(
                    "Warning: The sum of train, val, and test sets does not match the original dataset size."
                )
            else:
                print(
                    "The sum of train, val, and test sets matches the original dataset size."
                )

            # store the first row of each split for the current seed
            seed_samples[seed] = {
                "train": train_ds[0],
                "val": val_ds[0],
                "test": test_ds[0],
            }

        # If row items are the same print success message
        for split_name in ["train", "val", "test"]:
            first_rows = [rows[split_name] for rows in seed_samples.values()]
            if all(row == first_rows[0] for row in first_rows):
                print(
                    f"Success: First rows of {split_name} split are the same for all seeds."
                )
            else:
                print(
                    f"Warning: First rows of {split_name} split differ for some seeds."
                )

    run_spilt(seeds=[42, 42])


if __name__ == "__main__":
    # Excercise1()
    # Excercise2()
    # Excercise3()
    Excercise4()
