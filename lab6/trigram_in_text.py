from collections import OrderedDict
from json import dump
from math import ceil
from os import getpid
from re import findall
from threading import Lock
from threading import Thread, current_thread

RESULT = {}
CHUNK_COUNT = 3
mutex = Lock()


def separate_text_and_call():
    child_processes = []
    print(f"Main process: pid: {getpid()}")
    filename = "big_input.txt"
#    filename = "small_input.txt"
    with open(filename, "r") as f_stream:
        data_from_text = f_stream.read()
    splited_data = data_from_text.split()
    chunk_size = int(ceil(len(splited_data) / CHUNK_COUNT))
    for i in range(CHUNK_COUNT):
        slicer_item = slice(i * chunk_size, i * chunk_size + chunk_size)
        child = Thread(target=trigram_frequency_of_occurrence_calc,
                       args=(splited_data[slicer_item],))
        child.start()
        child_processes.append(child)
    [process.join() for process in child_processes]


def trigram_frequency_of_occurrence_calc(data_from_text: str):
    thread_data = current_thread()
    print(f"\n{thread_data.name} I'm child thread. pid: {getpid()};")

    words = findall(r"[\w']+", ' '.join(data_from_text))
    trigram_occurrences = {}
    for idx in range(len(words)):
        try:
            trigram = ' '.join(word.lower() for word in words[idx:idx + 3]).strip()
            if trigram_occurrences.get(trigram):
                trigram_occurrences[trigram] += 1
            else:
                trigram_occurrences[trigram] = 1
        except IndexError:
            break
    count_of_trigrams = sum(trigram_occurrences.values())

    mutex.acquire()
    _fill_result(trigram_occurrences, count_of_trigrams)
    mutex.release()


def _fill_result(trigram_occurrences: dict, count_in_fragment):
    global RESULT

    if not RESULT:
        RESULT.update(trigram_occurrences)
        RESULT["total_count"] = count_in_fragment
        return

    for key, value in trigram_occurrences.items():
        if key in RESULT:
            RESULT[key] += value
        else:
            RESULT[key] = value
    RESULT["total_count"] += count_in_fragment


def sort_and_write_result():
    sorted_result = OrderedDict(sorted(RESULT.items(), key=lambda key_val: key_val[1], reverse=True))
    count_of_trigrams = sorted_result.pop("total_count")
    for trigram, occurrence in sorted_result.items():
        sorted_result[trigram] = round(occurrence / count_of_trigrams, 5)

    with open("result.json", "w+") as f_stream:
        dump(sorted_result, f_stream, indent=4)


if __name__ == '__main__':
    separate_text_and_call()
    sort_and_write_result()
