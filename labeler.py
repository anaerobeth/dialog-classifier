import glob
import re
import csv
import logging
import threading
from multiprocessing import Process, Queue


class AutoLabeler(object):
    """Assigns labels to sentences in a text file

    1 for dialog sentences, 0 for regular sentences

    :param text_file: source text file
    """

    def __init__(self, text_file):
        self.text_file = text_file
        self.data = []

    def run(self):
        with open(text_file, 'r') as f:
            logging.info('Reading', text_file)
            for line in f:
                self.assign_label(line)
        return self.data

    def assign_label(self, line):
        match = re.search('"(.*)"', line)
        if match:
            match = match.group(1)
            rest = line.replace(match, '')
            if rest and len(match) * 2 > len(rest):
                # Remove inner quotes and label as 1 for dialog
                self.data.append([match.replace('"', '' ), 1])
            else:
                if len(rest) > 2:
                    # Label as 0 for non-dialog
                    self.data.append([rest, 0])
        else:
            if len(line) > 2:
                self.data.append([line.rstrip(), 0])


def ingest(queue, text_file):
    data = AutoLabeler(text_file).run()
    queue.put(data)


if __name__ == '__main__':
    queue = Queue()
    text_files = glob.glob("*.txt")
    output = 'data.csv'
    procs = []
    results = []

    try:
        for text_file in text_files:
            proc = Process(target=ingest, args=(queue, text_file))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        while not queue.empty():
            results.append(queue.get())

        queue.close()
        queue.join_thread()

        with open(output, 'w') as f:
            flat_results = [item for sublist in results for item in sublist]
            writer = csv.writer(f)
            for line in flat_results:
                writer.writerow(line)
            logging.info('Writing data to', output)
    except:
        print('Ingestion Failed') 

