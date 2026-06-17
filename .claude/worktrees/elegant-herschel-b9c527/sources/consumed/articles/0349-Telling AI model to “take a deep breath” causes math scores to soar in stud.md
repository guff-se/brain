---
title: "Telling AI model to “take a deep breath” causes math scores to soar in stud"
kind: article
party: third
source: pocket
source_id: "pocket:0349"
provenance: extracted
url: "https://arstechnica.com/information-technology/2023/09/telling-ai-model-to-take-a-deep-breath-causes-math-scores-to-soar-in-study/"
ingested: 2026-05-13
created: 2023-09-23
tags: []
status: reference
pocket_status: unread
enrichment: original
---

Google DeepMind researchers recently developed a technique to improve math ability in AI language models like ChatGPT by using other AI models to improve prompting—the written instructions that tell the AI model what to do. It found that using human-style encouragement improved math skills dramatically, in line with earlier results.
In a paper called "Large Language Models as Optimizers" listed this month on arXiv, DeepMind scientists introduced Optimization by PROmpting (OPRO), a method to improve the performance of large language models (LLMs) such as OpenAI’s ChatGPT and Google’s PaLM 2. This new approach sidesteps the limitations of traditional math-based optimizers by using natural language to guide LLMs in problem-solving. "Natural language" is a fancy way of saying everyday human speech.
"Instead of formally defining the optimization problem and deriving the update step with a programmed solver," the researchers write, "we describe the optimization problem in natural language, then instruct the LLM to iteratively generate new solutions based on the problem description and the previously found solutions."
Typically, in machine learning, techniques using algorithms such as derivative-based optimizers act as a guide for improving an AI model's performance. Imagine a model's performance as a curve on a graph: The goal is to find the lowest point on this curve because that's where the model makes the fewest mistakes. By using the slope of the curve to make adjustments, the optimizer helps the model get closer and closer to that ideal low point, making it more accurate and efficient at whatever task it's designed to do.
