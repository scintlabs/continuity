## classify()

`base/core/classify.py` provides an asynchronous function for short text classification. The function accepts an object or message and sends a request to the configured OpenAI client to generate a short description.

### Inputs
- `obj` – the object or text to classify
- `kind` – either `"parameter"` or `"thread"`
- `val` – optional parameter name used when `kind` is `"parameter"`

### OpenAI request
- Utilizes `OPENAI_CLIENT` from `base.config`
- Calls `responses.create` with model `o4-mini`
- `top_p` and `temperature` are randomized for each call
- The `input` field depends on `kind`:
  - `parameter` – describes a function parameter using the provided `val`
  - `thread` – asks for a concise title and one line description of the conversation

### Return value
Returns the text in `res.output_text` from OpenAI or `None` if no text was generated.
