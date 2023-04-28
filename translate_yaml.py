#####################################################################################################################
# Author: NeoMindStd                                                                                                #
#   suppported by chat gpt (gpt-4)                                                                                  #
#                                                                                                                   #
# If there are too many requests from the same IP in a short period of time,                                        #
# you may receive a 429 error code when requesting a translation for a while. In that case, please take a break.    #
#####################################################################################################################

import argparse
from googletrans import Translator
from ruamel.yaml import YAML
from concurrent.futures import ThreadPoolExecutor
import re

translator = Translator(service_urls=['translate.google.com'])
translator.raise_Exception = True

def translate_text(key, text, target, source):
    # Find all tokens that match the criteria
    tokens = re.findall(r'&.*?%|#.*?%|-.*?%|&.*$', text)

    # Replace the tokens with placeholders in the original text
    for i, token in enumerate(tokens):
        text = text.replace(token, f'Placeholder{i}', 1)

    # Translate the text with the placeholders
    try:
        result = translator.translate(text, dest=target, src=source)
        translated_text = result.text
    except Exception as e:
        print(f"Error translating key: {key}, text: {text}. Error: {e}")
        translated_text = text

    # Replace the placeholders with the original tokens in the translated text
    for i, token in enumerate(tokens):
        translated_text = translated_text.replace(f'Placeholder{i}', token, 1)

    return key, translated_text.replace('\n', ' ')


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
            elif isinstance(value, str):
                futures.append(executor.submit(translate_text, key, value, target_lang, source_lang))

        for future in futures:
            result = future.result()
            if result:
                key, value = result
                translated_content[key] = value

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
