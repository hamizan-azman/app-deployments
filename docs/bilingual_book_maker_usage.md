# bilingual_book_maker -- Usage Documentation

## Overview
CLI tool to translate EPUB/TXT/MD/SRT/PDF files and produce bilingual outputs using OpenAI and other providers.

## Quick Start
```
# Pull from Docker Hub (recommended)
docker pull hoomzoom/bilingual_book_maker

# Or build from source
docker build -t bilingual_book_maker .

docker run --rm \
  -e OPENAI_API_KEY=your-api-key \
  --mount type=bind,source=/path/to/books,target=/app/test_books \
  hoomzoom/bilingual_book_maker \
  --book_name /app/test_books/animal_farm.epub \
  --test
```

## Base URL
N/A. This is a CLI tool.

## Core Features
- Translate EPUB/TXT/MD/SRT/PDF and generate bilingual outputs
- Supports multiple translation providers and models
- Resume, batch, and parallel processing options

## API Endpoints

### Translate Book
- **Command:** `python3 make_book.py --book_name <file> [options]`
- **Method:** CLI
- **Description:** Translates an input file and outputs bilingual or translated-only results.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --openai_key ${OPENAI_API_KEY} --test`
- **Response:** Writes output files next to the input file.
- **Tested:** Yes

### Show Help
- **Command:** `python3 make_book.py --help`
- **Method:** CLI
- **Description:** Show CLI options.
- **Request:** `python3 make_book.py --help`
- **Response:** Prints help.
- **Tested:** Yes

### Use Installed CLI
- **Command:** `bbook --book_name <file> [options]`
- **Method:** CLI
- **Description:** Same as `make_book.py`, but from the packaged CLI.
- **Request:** `bbook --book_name test_books/animal_farm.epub --openai_key ${OPENAI_API_KEY} --test`
- **Response:** Writes output files next to the input file.
- **Tested:** Yes (via make_book.py entrypoint with TXT file)

### Provider Selection
- **Command:** `--model <provider>`
- **Method:** CLI
- **Description:** Selects translation backend.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --model deepl --deepl_key ${DEEPL_KEY}`
- **Response:** Writes output files.
- **Tested:** No (non-OpenAI providers not tested)

Supported providers include:
- `openai`, `chatgptapi`, `gpt4`, `gpt4omini`, `gpt4o`, `gpt5mini`, `o1preview`, `o1`, `o1mini`, `o3mini`
- `google`, `gemini`, `geminipro`
- `deepl`, `deeplfree`
- `claude`, `claude-3-5-sonnet-latest`, `claude-3-5-sonnet-20241022`, `claude-3-5-sonnet-20240620`, `claude-3-5-haiku-latest`, `claude-3-5-haiku-20241022`
- `caiyun`, `tencentransmart`, `customapi`, `xai`, `groq`, `qwen`, `qwen-mt-turbo`, `qwen-mt-plus`

### Use Ollama
- **Command:** `--ollama_model <model_name>`
- **Method:** CLI
- **Description:** Uses a local Ollama model. Optionally set `--api_base`.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --ollama_model llama3`
- **Response:** Writes output files.
- **Tested:** No (requires Ollama)

### Limit Translation for Testing
- **Command:** `--test --test_num <n>`
- **Method:** CLI
- **Description:** Translates only the first N paragraphs.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --test --test_num 1 --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes partial output.
- **Tested:** Yes

### Resume Interrupted Run
- **Command:** `--resume`
- **Method:** CLI
- **Description:** Resume from a previous interrupted run.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --model google --resume`
- **Response:** Continues translation.
- **Tested:** Yes

### Proxy
- **Command:** `--proxy <url>`
- **Method:** CLI
- **Description:** Sets HTTP/HTTPS proxy for requests.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --proxy http://127.0.0.1:7890 --openai_key ${OPENAI_API_KEY}`
- **Response:** Uses proxy.
- **Tested:** No

### Control EPUB File Selection
- **Command:** `--exclude_filelist <comma_list>` / `--only_filelist <comma_list>`
- **Method:** CLI
- **Description:** Exclude or include specific EPUB files.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --exclude_filelist 'nav.xhtml,cover.xhtml' --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Control HTML Tags
- **Command:** `--translate-tags <comma_list>` / `--exclude_translate-tags <comma_list>`
- **Method:** CLI
- **Description:** Translate selected HTML tags.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --translate-tags p,blockquote --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Allow Navigable Strings
- **Command:** `--allow_navigable_strings`
- **Method:** CLI
- **Description:** Translate strings outside common HTML tags.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --allow_navigable_strings --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Prompt Customization
- **Command:** `--prompt <string|file>`
- **Method:** CLI
- **Description:** Customize prompt with template string, JSON, or PromptDown markdown.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --prompt prompt_template_sample.txt --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes (txt and json templates)

### Token Accumulation
- **Command:** `--accumulated_num <n>`
- **Method:** CLI
- **Description:** Controls accumulated token threshold before translation.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --accumulated_num 1600 --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Translation Style
- **Command:** `--translation_style <css>`
- **Method:** CLI
- **Description:** Apply CSS styling to translated text.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --translation_style "color: #808080; font-style: italic;" --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Batch Size (TXT)
- **Command:** `--batch_size <n>`
- **Method:** CLI
- **Description:** Aggregate lines for TXT translation.
- **Request:** `python3 make_book.py --book_name test_books/the_little_prince.txt --batch_size 20 --test --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Retranslate
- **Command:** `--retranslate <bilingual_epub> <file_in_epub> <start_str> <end_str>`
- **Method:** CLI
- **Description:** Retranslate a specific range from a bilingual EPUB.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --retranslate test_books/animal_farm_bilingual.epub index_split_002.html 'in spite of the present book shortage which' 'This kind of thing is not a good symptom. Obviously' --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes updated output files.
- **Tested:** Failed (see Notes)

### Single Translation Output
- **Command:** `--single_translate`
- **Method:** CLI
- **Description:** Output translated text only, no bilingual format.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --single_translate --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes translated-only output.
- **Tested:** Yes

### Context Mode
- **Command:** `--use_context --context_paragraph_limit <n>`
- **Method:** CLI
- **Description:** Adds a rolling summary for consistency.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --use_context --context_paragraph_limit 3 --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Temperature
- **Command:** `--temperature <float>`
- **Method:** CLI
- **Description:** Sets model temperature.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --temperature 0.7 --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Source Language
- **Command:** `--source_lang <lang>`
- **Method:** CLI
- **Description:** Set source language for models like Qwen.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --model qwen-mt-plus --source_lang English --qwen_key ${QWEN_KEY}`
- **Response:** Writes output files.
- **Tested:** No

### Block Size
- **Command:** `--block_size <n> --single_translate`
- **Method:** CLI
- **Description:** Merge paragraphs into larger blocks. Must be used with `--single_translate`.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --block_size 5 --single_translate --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Model List
- **Command:** `--model openai --model_list <list>`
- **Method:** CLI
- **Description:** Specify exact OpenAI model aliases.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --model openai --model_list gpt-4-1106-preview,gpt-3.5-turbo-0125 --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Batch API
- **Command:** `--batch` / `--batch-use`
- **Method:** CLI
- **Description:** Use ChatGPT batch API to pre-generate and then apply translations.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --batch --openai_key ${OPENAI_API_KEY}`
- **Response:** Creates batch translations and outputs files.
- **Tested:** No

### Request Interval
- **Command:** `--interval <seconds>`
- **Method:** CLI
- **Description:** Request interval for Gemini models.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --model gemini --interval 0.1 --gemini_key ${GEMINI_KEY}`
- **Response:** Writes output files.
- **Tested:** No

### Parallel Workers
- **Command:** `--parallel-workers <n>`
- **Method:** CLI
- **Description:** Parallel EPUB chapter processing.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --parallel-workers 4 --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** Yes

### Kobo Import
- **Command:** `--book_from kobo --device_path <path>`
- **Method:** CLI
- **Description:** Load a book from a Kobo device.
- **Request:** `python3 make_book.py --book_from kobo --device_path /tmp/kobo --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** No

### Azure OpenAI
- **Command:** `--api_base <url> --deployment_id <id>`
- **Method:** CLI
- **Description:** Use Azure OpenAI endpoints.
- **Request:** `python3 make_book.py --book_name test_books/animal_farm.epub --api_base https://example-endpoint.openai.azure.com --deployment_id deployment-name --openai_key ${OPENAI_API_KEY}`
- **Response:** Writes output files.
- **Tested:** No

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | No | None | OpenAI API key (legacy support). |
| `BBM_OPENAI_API_KEY` | No | None | Preferred OpenAI API key variable. |
| `BBM_CAIYUN_API_KEY` | No | None | Caiyun key. |
| `BBM_DEEPL_API_KEY` | No | None | DeepL key. |
| `BBM_CLAUDE_API_KEY` | No | None | Claude key. |
| `BBM_CUSTOM_API` | No | None | Custom translation API token. |
| `BBM_GOOGLE_GEMINI_KEY` | No | None | Gemini key. |
| `BBM_GROQ_API_KEY` | No | None | Groq key. |
| `BBM_XAI_API_KEY` | No | None | xAI key. |
| `BBM_QWEN_API_KEY` | No | None | Qwen key. |
| `BBM_CHATGPTAPI_USER_MSG_TEMPLATE` | No | None | Override user prompt template. |
| `BBM_CHATGPTAPI_SYS_MSG` | No | None | Override system prompt template. |
| `http_proxy` | No | None | HTTP proxy (set via `--proxy`). |
| `https_proxy` | No | None | HTTPS proxy (set via `--proxy`). |

## Notes
- PDF support requires PyMuPDF (included in the Docker image).
- Output filenames end with `_bilingual.*` for bilingual results, or `*_bilingual_temp.*` on interruption.
- The container needs internet access to reach the configured provider.
- Retranslate failed in testing with `ValueError: Element has no parent, so 'after' has no meaning.`

## Changes from Original
**Category: Dependencies only.** Source code untouched.

- `PyMuPDF==1.24.2` added (not in original requirements.txt). The code imports `fitz` at module load time -- this was a missing dependency in the original repo.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed — all minimum versions resolved successfully.
