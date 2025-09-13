# Efficient-Batch-Processed-Q-A-with-Gemini-Context-Caching-RAG

This is an offline-ready local demo of the batch prediction + context caching pipeline from the GSoC DeepMind Challenge [Q4](https://gist.github.com/dynamicwebpaige/92f7739ad69d2863ac7e2032fe52fbad#4-batch-prediction-with-long-context-and-context-caching-code-sample):

### This repo demonstrates batch prediction with Gemini APIs, leveraging long context and context caching for efficiently answering questions about a single video. It addresses a common use case of extracting information from large content sources.

**Scenario:** Extracting information from a video lecture/documentary by asking multiple, potentially interconnected, questions.

**Code Sample Features:**

**Batch Prediction:** Design and optimization for submitting a batch of questions. This should minimize API calls and improve efficiency. Consider using techniques like dividing the questions into smaller batches to avoid exceeding API limits. 📦
**Long Context Handling:** Demonstrate use of Gemini's long context capabilities. Show how to provide the entire video transcript (or relevant segments) as context. Consider strategies for handling transcripts that exceed the maximum context length. 📏
**Context Caching:** Implement context caching to store and reuse previous interactions. This can significantly reduce the amount of data sent to the API and improve response times, especially for interconnected questions. Use a suitable caching mechanism (e.g., in-memory cache, persistent storage). 💾
**Interconnected Questions:** Handle questions that build upon previous answers. The code should maintain the conversation history and use it to provide more accurate and relevant responses. 🔗
**Output Formatting:** Clear and user-friendly output. Present the answers in a structured format, possibly with links to the relevant timestamps in the video. ✨
**Code Documentation:** Detailed comments, setup instructions, and usage guidelines. Explain the different components of the code and how they work together. Include instructions on how to obtain and configure an API key. Provide example questions and expected outputs. 📖
**Error Handling:** Implement robust error handling to gracefully handle API errors, network issues, and invalid inputs.


A work in progress code implementation from the submitted [proposal](https://github.com/Shifat7/Efficient-Batch-Processed-Q-A-with-Gemini-Context-Caching-RAG/blob/main/gsoc%20proposal.pdf)

## How to Run

```bash
poetry install
poetry run python src
```
