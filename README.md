# AI_PSYCHIATRIST
__________________________________________________________________________________________________
Model name : meta-llama/Llama-3.2-1B-Instruct
__________________________________________________________________________________________________
Model accsess link: https://llm-explorer.com/list/?4GB
__________________________________________________________________________________________________
Activate the enviorment:	source .venv/bin/activate
__________________________________________________________________________________________________
# Run the Docker container (start the server)
sudo docker run --shm-size=4g \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN} \
  -p 8000:8000 \
  --ipc=host \
  vllm-cpu-env \
  --model meta-llama/Llama-3.2-1B-Instruct \
  --dtype auto \
  --api-key ${API_KEY} \
  --cpu-offload-gb 10 \
  --max-model-len 2048
___________________________________
Run streamlit : streamlit ai_psychaitrist.py
__________________________________________________________________________________________________
Open the website in a web browser
__________________________________________________________________________________________________
