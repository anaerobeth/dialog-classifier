import glob
import re
import csv
import logging


class AutoLabeler(object):
    """Assigns labels to sentences in text files

    1 for dialog sentences, 0 for regular sentences

    :param text_files: list of source files
    :param output: name of output file
    """

    def __init__(self, text_files, output):
        self.text_files = text_files
        self.output = output
        self.data = []

    def run(self):
        for text_file in self.text_files:
            with open(text_file, 'r') as f:
                logging.info('Reading', text_file)
                for line in f:
                    self.assign_label(line)
        self.write_to_csv()

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

    def write_to_csv(self):
        with open(self.output, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
            logging.info('Writing data to', self.output)


if __name__ == '__main__':
    text_files = glob.glob("*.txt")
    labeler = AutoLabeler(text_files, 'data.csv')
    labeler.run()
