#####################################################################################################################
# Author: NeoMindStd                                                                                                #
#   suppported by chat gpt (gpt-4)                                                                                  #
#                                                                                                                   #
# If there are too many requests from the same IP in a short period of time,                                        #
# you may receive a 429 error code when requesting a translation for a while. In that case, please take a break.    #
#####################################################################################################################

import argparse
import re
from googletrans import Translator
from ruamel.yaml import YAML
from concurrent.futures import ThreadPoolExecutor

translator = Translator(service_urls=['translate.google.com'])
translator.raise_Exception = True

PLACEHOLDERS = [
    r"%\w+%",
    r"&\w+",
    r"'[A-Za-z]+'",
]

temp_words = ['SOMETHING', 'SOMEONE', 'PLACEHOLDER']

def translate_text(key, text, target, source):
    placeholders = []
    for ph in PLACEHOLDERS:
        matches = re.findall(ph, text)
        for i, match in enumerate(matches):
            placeholder_id = f"PLACEHOLDER{i}"  # Generate a unique ID for each placeholder
            placeholders.append((placeholder_id, match))
            text = text.replace(match, placeholder_id)

    # Translate the text while ignoring placeholders
    try:
        result = translator.translate(text, dest=target, src=source)
        translated_text = result.text
    except Exception as e:
        print(f"Error translating key: {key}, text: {text}. Error: {e}")
        return text

    # Replace general words back to placeholders
    for i in range(len(placeholders)):
        translated_text = translated_text.replace(temp_words[i % len(temp_words)], placeholders[i][0])

    # Replace placeholders with their original values
    for placeholder_id, original in placeholders:
        pattern = re.compile(placeholder_id, re.IGNORECASE)
        translated_text = pattern.sub(original, translated_text)

    return translated_text.replace('\n', ' ')

def translate_yaml(input_file, output_file, source_lang, target_lang, workers):
    yaml = YAML()
    yaml.preserve_quotes = True
    with open(input_file, 'r', encoding='utf-8') as stream:
        try:
            yaml_content = yaml.load(stream)
        except Exception as exc:
            print(exc)

    translated_content = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for key, value in yaml_content.items():
            if isinstance(value, list):
                for i in range(len(value)):
                    futures.append(executor.submit(translate_text, key, value[i], target_lang, source_lang))
                translated_content[key] = [future.result() for future in futures]
                futures = []
            elif isinstance(value, str):
                futures.append(executor.submit(translate_text, key, value, target_lang, source_lang))
                translated_content[key] = futures[0].result()
                futures = []

    for key in yaml_content.keys():
        if key in translated_content:
            yaml_content[key] = translated_content.get(key)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        yaml.dump(yaml_content, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate YAML file content')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-s', '--source', required=True, help='Source language')
    parser.add_argument('-t', '--target', required=True, help='Target language')
    parser.add_argument('-w', '--workers', type=int, default=1, help='Number of worker threads')
    args = parser.parse_args()

    translate_yaml(args.input, args.output, args.source, args.target, args.workers)
