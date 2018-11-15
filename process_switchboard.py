import os
from swda import CorpusReader
from swda_utilities import *

# Processed data directory
data_dir = 'swda_data/'

# Corpus object for iterating over the whole corpus in .csv format
corpus = CorpusReader('raw_swda_data/')

# File for all the utterances in the corpus
all_text_file = "all_swda_text.txt"
# Remove old file if it exists
if os.path.exists(data_dir + all_text_file):
    os.remove(data_dir + all_text_file)

# Load training, test, validation and development splits
train_split = read_file(data_dir + 'train_split.txt')
test_split = read_file(data_dir + 'test_split.txt')
val_split = read_file(data_dir + 'val_split.txt')
dev_split = read_file(data_dir + 'dev_split.txt')

# Excluded dialogue act tags i.e. x = Non-verbal
excluded_tags = ['x']
# Excluded characters for ignoring i.e. <laughter>
excluded_chars = {'<', '>', '(', ')', '-', '#'}

# Process each transcript
for transcript in corpus.iter_transcripts(display_progress=False):

    # Process the utterances and create a dialogue object
    dialogue = process_transcript(transcript, excluded_tags, excluded_chars)

    # Write all utterances to file
    with open(data_dir + all_text_file, 'a+') as file:
        for utterance in dialogue.utterances:
            file.write(utterance.speaker + "|" + utterance.text + "|" + utterance.da_label + "\n")

    # Determine which set this dialogue belongs to (training, test or evaluation)
    set_dir = ''
    if dialogue.conversation_num in train_split:
        set_dir = data_dir + 'train/'
    elif dialogue.conversation_num in test_split:
        set_dir = data_dir + 'test/'
    elif dialogue.conversation_num in val_split:
        set_dir = data_dir + 'val/'

    # Create the directory if is doesn't exist yet
    if not os.path.exists(set_dir):
        os.makedirs(set_dir)

    # Write dialogue to train, test or validation folders
    with open(set_dir + dialogue.conversation_num + ".txt", 'w+') as file:
        for utterance in dialogue.utterances:
            file.write(utterance.speaker + "|" + utterance.text + "|" + utterance.da_label + "\n")

    # If it is also in the development set write it there too
    if dialogue.conversation_num in dev_split:

        set_dir = data_dir + 'dev/'

        # Create the directory if is doesn't exist yet
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)

        with open(set_dir + dialogue.conversation_num + ".txt", 'w+') as file:
            for utterance in dialogue.utterances:
                file.write(utterance.speaker + "|" + utterance.text + "|" + utterance.da_label + "\n")