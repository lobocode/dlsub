import re
import json
import spacy
from tqdm import tqdm
from enelvo import normaliser
import textwrap
import subprocess
import sys


# Now, we can safely load the model
nlp = spacy.load('pt_core_news_sm')

class TranscriptProcessor:
    """
    A class that can process transcripts of YouTube videos.
    """
    def __init__(self, raw_transcript, language):
        self.raw_transcript = raw_transcript
        self.language = language
        
    def check_and_install_spacy_models(models):
        """
        Function to check if spacy models are installed. If not, install them.
        
        Args:
            models (list): A list of spacy model names as strings.
        """
        for model in models:
            try:
                # Try to load the model
                spacy.load(model)
                pass
            except OSError:
                # If model is not installed, install it
                print(f"Model {model} not found. Installing...")
                subprocess.check_call([sys.executable, "-m", "spacy", "download", model])

    # Check and install 'pt_core_news_sm' model
    check_and_install_spacy_models(['pt_core_news_sm'])

    def format_transcript(self):
        """
        Format a transcript by extracting only 'text' values, correcting text using Enelvo,
        and wrapping the text into paragraphs for easy reading using Spacy, with a space between paragraphs.

        Returns:
            List[str]: A list of formatted transcript paragraphs with spaces.
        """
        norm = normaliser.Normaliser()

        corrected_texts = []

        for transcript_item in tqdm(self.raw_transcript, desc="Formatting", unit=" lines"):
            # Extract 'text' value
            text = transcript_item['text']

            # Correct the text using Enelvo
            norm_sentence = norm.normalise(text)
            corrected_texts.append(norm_sentence)

        # Combine all corrected texts into a single string
        full_text = ' '.join(corrected_texts)

        # Split the text into sentences using spacy
        doc = nlp(full_text)
        sentences = [sent.text.strip() for sent in doc.sents]

        paragraph_size = 400  # Change this number to adjust paragraph length
        paragraphs = []
        current_paragraph = ""
        for sentence in sentences:
            if len(current_paragraph) + len(sentence) > paragraph_size:
                # Use textwrap.fill() to break lines at a specified width
                paragraphs.append(textwrap.fill(current_paragraph.strip(), width=paragraph_size))
                current_paragraph = sentence
            else:
                current_paragraph += " " + sentence
        # Append the last paragraph if it's non-empty
        if current_paragraph.strip():
            paragraphs.append(textwrap.fill(current_paragraph.strip(), width=paragraph_size))

        # Add a space between paragraphs and capitalize first letter of each paragraph
        formatted_transcript = []
        for paragraph in paragraphs:
            # Capitalize first letter of each paragraph and append it to formatted_transcript
            capitalized_paragraph = paragraph[0].upper() + paragraph[1:]
            # Append capitalized_paragraph to formatted_transcript
            formatted_transcript.append(capitalized_paragraph)
            # Append an empty string to create a space between paragraphs
            formatted_transcript.append("")
        
        return formatted_transcript

    def format_and_show_progress(self):
        # Call format_transcript() method
        formatted_transcript = self.format_transcript()

        # Calculate the total number of lines
        total_lines = len(formatted_transcript)

        # Iterate through the formatted_transcript and display progress
        for i, line in enumerate(formatted_transcript):
            print(f"\rProcessing line {i + 1}/{total_lines}", end="")

        print("\nFinished processing transcript.")
        return formatted_transcript