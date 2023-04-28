# YAML Translator

This project uses the Google Translate API to automatically translate the content of a YAML file from one language to another. 

## Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/your-repository.git
```

2. Navigate to the project directory.

```bash
cd your-repository
```

3. Install the required Python packages.

```bash
pip install -r requirements.txt
```

## Usage

Run the script `translate_yaml.py` with the following command-line arguments:

- `-i` or `--input`: The path to the input YAML file.
- `-o` or `--output`: The path to the output YAML file.
- `-s` or `--source`: The source language (e.g., 'en' for English).
- `-t` or `--target`: The target language (e.g., 'ko' for Korean).
- `-w` or `--workers`: The number of worker threads to use for parallel processing.

```bash
python translate_yaml.py -i input.yml -o output.yml -s en -t ko -w 5
```

In the above example, the script will translate the content of `input.yml` from English to Korean and save the result in `output.yml`. It will use 5 worker threads for parallel processing.

## Supported Languages

The supported languages are those supported by the Google Translate API. For a full list of supported languages, refer to the [Google Translate API documentation](https://cloud.google.com/translate/docs/languages).

## Note

Due to the limitations of the free tier of the Google Translate API, there may be a delay in the translation process if the number of requests exceeds the limit.

## License

[This project is licensed under the terms of the MIT license.](./LICENSE)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms.
