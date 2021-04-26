import re
from math import ceil
from multiprocessing import Process
from os import getpid, getppid
from typing import List

CHUNK_COUNT = 3


def trigram_frequency_of_occurrence_calc(data_from_text: List[str]):
    print(f"\nI'm child process. pid: {getpid()}; parent pid: {getppid()}. "
          f"Trigrams and their frequency in below:")

    only_words_text = re.sub("'|\?|\.|\!|\/|\;|\:|\,|\\n|\"|\’|\'|'", '',
                             data_from_text)
    words = only_words_text.split()

    trigram_occurrences = {}
    for idx in range(len(words)):
        try:
            trigram = tuple(word.lower() for word in words[idx:idx+3])
            if trigram_occurrences.get(trigram):
                trigram_occurrences[trigram] += 1
            else:
                trigram_occurrences[trigram] = 1
        except IndexError:
            continue
    count_of_trigrams = sum(trigram_occurrences.values())
    sorted_by_occurrences = sorted(trigram_occurrences.items(),
                                   key=lambda key_val: key_val[1],
                                   reverse=True)

    print()
    print([(trigram, round(occurrences/count_of_trigrams, 5))
           for trigram, occurrences in sorted_by_occurrences])


def separate_text_and_call():
    child_processes = []
    print(f"Main process: pid: {getpid()}")
    filename = "big_input.txt"
    filename = "small_input.txt"
    with open(filename, "r") as f_stream:
        data_from_text = f_stream.read()

    chunk_size = int(ceil(len(data_from_text)/CHUNK_COUNT))
    for i in range(CHUNK_COUNT):

        slicer_item = slice(i * chunk_size, i * chunk_size + chunk_size)
        child = Process(target=trigram_frequency_of_occurrence_calc,
                        args=(data_from_text[slicer_item], ))
        child.start()
        child_processes.append(child)
    [process.join() for process in child_processes]


if __name__ == '__main__':
    separate_text_and_call()
