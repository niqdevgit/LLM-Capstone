# AI-Powered IP-XACT Component Generator

## Problem Statement and Solution Approach

### Problem Statement
Chip and hardware design rely on complex, structured data formats like IEEE1685/IP-XACT. Creating valid, reusable IP components manually is a time-consuming and error-prone process. Engineers must ensure that these components comply with strict specifications, which requires extensive domain expertise and verification effort. The lack of automation in this process slows down development cycles and increases the risk of human error.

### Solution Approach
This project aims to automate the generation and validation of IP-XACT components using a fine-tuned Large Language Model (LLM). The approach involves:
1. **Data Collection & Preprocessing** – Gathering a dataset of valid IP-XACT components, ensuring well-structured XML data for training.
2. **Fine-Tuning the LLM** – Training the model on structured XML-based IP-XACT data to learn the format, constraints, and best practices.
3. **Component Generation** – Using the trained model to generate new IP-XACT components that conform to IEEE1685 standards.
4. **Validation with Kactus2** – Automatically checking the generated components for compliance and correctness using Kactus2.
5. **User Interaction** – Allowing users to request components with specific constraints and receiving validated outputs ready for use.

By leveraging AI to generate and validate IP-XACT components, this approach significantly reduces manual effort, improves accuracy, and speeds up the hardware design workflow.

## Detailed Workflow of the Model

1. Model gets prompt
2. Model makes answer
3. Model returns answer

## Challenges Faced & How They Were Solved
### Model selection
I tried many models for IP-XACT creation:
* https://huggingface.co/codemateai/CodeMate-v0.1 but it was too big for google colab. About 7 * 20 gb 
* https://huggingface.co/Salesforce/codet5-small But it did not perform at all, the outputs it gave to basic prompts were nonsense.
* https://huggingface.co/Salesforce/codet5-base Same issues as codet5-small
* https://huggingface.co/Salesforce/codet5-large Same issues as codet5-small
* Deepseek does not have HF template https://huggingface.co/deepseek-ai/DeepSeek-R1
* Failed to load https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct
* model="facebook/bart-large" issue: not understanding context
* model="t5-small" issue: not understanding context
* model gpt2 issue: wild hallusinations
* gpt2-large finaly gave something that was in the right direction. But when i fine-tuned it: CUDA out of memory. Tried to allocate 246.00 MiB. GPU 0 has a total capacity of 14.74 GiB of which 2.12 MiB is free.

gpt2-medium i was able to fine-tune

_Maybe i should have used BERT?_ 🤔
### Other challenges  
* No high-quality data available  
* Not enough understanding of this topic (IP-XACT, Kactus2)  
* HUGE project in just 3 weeks. I would have been better off having a teammate: one focusing purely on fine-tuning the model and another handling documentation, UI, and other tasks.

## Future Improvements

While the current implementation streamlines IP-XACT component generation and validation, several areas can be further optimized:

1. **Model Optimization for Performance** – Fine-tuning with more efficient architectures or quantization techniques (e.g., LoRA, QLoRA) to reduce inference time and resource consumption.
2. **Enhanced Dataset Quality** – Expanding the dataset with more diverse IP-XACT examples, including edge cases, to improve model robustness.
3. **Better User Input Handling** – Implementing a more interactive interface where users can define specific constraints and requirements for component generation.
4. **Integration with Additional EDA Tools** – Extending validation beyond Kactus2 by integrating with other Electronic Design Automation (EDA) tools for broader verification.
5. **Automated Post-Processing** – Refining the output formatting and adding automatic corrections for minor syntax errors before validation.
6. **Extending Beyond IP-XACT** – Exploring how this approach can be generalized to other structured hardware description formats (e.g., SystemVerilog, VHDL) for a wider range of applications.
7. **Continuous Model Improvement via Feedback Loop** – Implementing a feedback system where failed Kactus2 validation results are fed back into the AI model. This allows the model to learn from these failures, improving its ability to generate accurate components over time. This iterative approach would help the model become more robust and better handle edge cases and uncommon validation errors.

These improvements can enhance the usability, efficiency, and applicability of the AI-powered IP-XACT generator, making it a more comprehensive tool for hardware designers.

