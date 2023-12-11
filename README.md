# dbt-database

- This is where I will locate my files and tools relating to the generation and development of my Dialectical Behavior Therapy dataset.

## llama.cpp/example/server

This example demonstrates a simple HTTP API server and a simple web front end to interact with llama.cpp.

Command line options:

- `--threads N`, `-t N`: Set the number of threads to use during generation.
- `-tb N, --threads-batch N`: Set the number of threads to use during batch and prompt processing. If not specified, the number of threads will be set to the number of threads used for generation.
- `-m FNAME`, `--model FNAME`: Specify the path to the LLaMA model file (e.g., `models/7B/ggml-model.gguf`).
- `-a ALIAS`, `--alias ALIAS`: Set an alias for the model. The alias will be returned in API responses.
- `-c N`, `--ctx-size N`: Set the size of the prompt context. The default is 512, but LLaMA models were built with a context of 2048, which will provide better results for longer input/inference. The size may differ in other models, for example, baichuan models were build with a context of 4096.
- `-ngl N`, `--n-gpu-layers N`: When compiled with appropriate support (currently CLBlast or cuBLAS), this option allows offloading some layers to the GPU for computation. Generally results in increased performance.
- `-mg i, --main-gpu i`: When using multiple GPUs this option controls which GPU is used for small tensors for which the overhead of splitting the computation across all GPUs is not worthwhile. The GPU in question will use slightly more VRAM to store a scratch buffer for temporary results. By default GPU 0 is used. Requires cuBLAS.
- `-ts SPLIT, --tensor-split SPLIT`: When using multiple GPUs this option controls how large tensors should be split across all GPUs. `SPLIT` is a comma-separated list of non-negative values that assigns the proportion of data that each GPU should get in order. For example, "3,2" will assign 60% of the data to GPU 0 and 40% to GPU 1. By default the data is split in proportion to VRAM but this may not be optimal for performance. Requires cuBLAS.
- `-b N`, `--batch-size N`: Set the batch size for prompt processing. Default: `512`.
- `--memory-f32`: Use 32-bit floats instead of 16-bit floats for memory key+value. Not recommended.
- `--mlock`: Lock the model in memory, preventing it from being swapped out when memory-mapped.
- `--no-mmap`: Do not memory-map the model. By default, models are mapped into memory, which allows the system to load only the necessary parts of the model as needed.
- `--numa`: Attempt optimizations that help on some NUMA systems.
- `--lora FNAME`: Apply a LoRA (Low-Rank Adaptation) adapter to the model (implies --no-mmap). This allows you to adapt the pretrained model to specific tasks or domains.
- `--lora-base FNAME`: Optional model to use as a base for the layers modified by the LoRA adapter. This flag is used in conjunction with the `--lora` flag, and specifies the base model for the adaptation.
- `-to N`, `--timeout N`: Server read/write timeout in seconds. Default `600`.
- `--host`: Set the hostname or ip address to listen. Default `127.0.0.1`.
- `--port`: Set the port to listen. Default: `8080`.
- `--path`: path from which to serve static files (default examples/server/public)
- `--embedding`: Enable embedding extraction, Default: disabled.
- `-np N`, `--parallel N`: Set the number of slots for process requests (default: 1)
- `-cb`, `--cont-batching`: enable continuous batching (a.k.a dynamic batching) (default: disabled)

```powershell
server.exe -m models\7B\ggml-model.gguf -c 2048
```

The above command will start a server that by default listens on `127.0.0.1:8080`.

## API Endpoints

- **POST** `/completion`: Given a `prompt`, it returns the predicted completion.

    *Options:*

    `prompt`: Provide the prompt for this completion as a string or as an array of strings or numbers representing tokens. Internally, the prompt is compared to the previous completion and only the "unseen" suffix is evaluated. If the prompt is a string or an array with the first element given as a string, a `bos` token is inserted in the front like `main` does.

    `temperature`: Adjust the randomness of the generated text (default: 0.8).

    `top_k`: Limit the next token selection to the K most probable tokens (default: 40).

    `top_p`: Limit the next token selection to a subset of tokens with a cumulative probability above a threshold P (default: 0.95).

    `min_p`: The minimum probability for a token to be considered, relative to the probability of the most likely token (default: 0.05).

    `n_predict`: Set the maximum number of tokens to predict when generating text. **Note:** May exceed the set limit slightly if the last token is a partial multibyte character. When 0, no tokens will be generated but the prompt is evaluated into the cache. (default: -1, -1 = infinity).

    `n_keep`: Specify the number of tokens from the prompt to retain when the context size is exceeded and tokens need to be discarded.
    By default, this value is set to 0 (meaning no tokens are kept). Use `-1` to retain all tokens from the prompt.

    `stream`: It allows receiving each predicted token in real-time instead of waiting for the completion to finish. To enable this, set to `true`.

    `stop`: Specify a JSON array of stopping strings.
    These words will not be included in the completion, so make sure to add them to the prompt for the next iteration (default: []).

    `tfs_z`: Enable tail free sampling with parameter z (default: 1.0, 1.0 = disabled).

    `typical_p`: Enable locally typical sampling with parameter p (default: 1.0, 1.0 = disabled).

    `repeat_penalty`: Control the repetition of token sequences in the generated text (default: 1.1).

    `repeat_last_n`: Last n tokens to consider for penalizing repetition (default: 64, 0 = disabled, -1 = ctx-size).

    `penalize_nl`: Penalize newline tokens when applying the repeat penalty (default: true).

    `presence_penalty`: Repeat alpha presence penalty (default: 0.0, 0.0 = disabled).

    `frequency_penalty`: Repeat alpha frequency penalty (default: 0.0, 0.0 = disabled);

    `mirostat`: Enable Mirostat sampling, controlling perplexity during text generation (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0).

    `mirostat_tau`: Set the Mirostat target entropy, parameter tau (default: 5.0).

    `mirostat_eta`: Set the Mirostat learning rate, parameter eta (default: 0.1).

    `grammar`: Set grammar for grammar-based sampling (default: no grammar)

    `seed`: Set the random number generator (RNG) seed (default: -1, -1 = random seed).

    `ignore_eos`: Ignore end of stream token and continue generating (default: false).

    `logit_bias`: Modify the likelihood of a token appearing in the generated text completion. For example, use `"logit_bias": [[15043,1.0]]` to increase the likelihood of the token 'Hello', or `"logit_bias": [[15043,-1.0]]` to decrease its likelihood. Setting the value to false, `"logit_bias": [[15043,false]]` ensures that the token `Hello` is never produced (default: []).

    `n_probs`: If greater than 0, the response also contains the probabilities of top N tokens for each generated token (default: 0)

    *Result JSON:*

    Note: When using streaming mode (`stream`) only `content` and `stop` will be returned until end of completion.

    `content`: Completion result as a string (excluding `stopping_word` if any). In case of streaming mode, will contain the next token as a string.
