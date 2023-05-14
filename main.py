import os
import json
import time
from src.helper import parse_arguments
from src.transcript_manager import download_and_process_transcript
from src.transcript_processor import TranscriptProcessor
from src.markai import process_with_ai

def main():
    # Parse command line arguments
    args = parse_arguments()

    # Download and process transcript
    transcript_list, downloader = download_and_process_transcript(args)
    if transcript_list is None:
        print("Transcript download failed.")
        return

    # Save transcript to output file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(transcript_list, f)
    print(f"Transcript saved in {args.output}.")

    # Process transcript
    if args.format or args.use_ai:
        with open(args.output, 'r', encoding='utf-8') as f:
            raw_transcript = json.load(f)

        processor = TranscriptProcessor(raw_transcript, args.language)
        formatted_transcript = processor.format_transcript()  # Define formatted_transcript outside the if blocks

        if args.format:
            output_file = os.path.splitext(args.output)[0] + '.txt'
            # if output_file exists, ask if user wants to overwrite it
            if os.path.exists(output_file):
                overwrite = input(f"File {output_file} already exists. Overwrite? (y/n) ")
                if overwrite.lower() != 'y':
                    # generate another file name with number suffix
                    output_file = os.path.splitext(args.output)[0] + '_1.txt'

            with open(output_file, 'w', encoding='utf-8') as f:
                for line in formatted_transcript:
                    f.write(f"{line}\n")
            print(f"Processed transcript saved in {output_file}.")
            
        if args.use_ai:
            output_file_ai = process_with_ai(args, formatted_transcript)
            print(f"AI processed transcript saved in {output_file_ai}.")

if __name__ == '__main__':
    main()
