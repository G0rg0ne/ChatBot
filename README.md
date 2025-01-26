Using [Ollama](https://ollama.ai/) to downlaod models:

``` cmd
D:OllamaSetup.exe /DIR="D:\Ollama_models"
```

``` powershell
ollama pull llama3
```
Note : You can setup the model's location by editing your OS environment variable.

You can run LangFlow with the following command : 
langflow run --port 7860 --host 0.0.0.0