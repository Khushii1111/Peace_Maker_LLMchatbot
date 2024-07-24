import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    if system_message is None:
        system_message = "I'm here to help you unwind. Let's take a deep breath together."
    else:
        system_message = "You are a good stress reliefer. your approach is to encourage letting go of overthinking, steering away from negative thoughts, and providing practical steps to manage stress effectively. Feel free to share what's on your mind, or would you like to try a quick relaxation exercise together."

    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response

demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="Remember to breathe deeply. Avoid fixating on unhelpful thoughts.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)"),
    ],
    examples=[
        ["I feel stressed with work."],
        ["How can I incorporate mindfulness into my daily routine to reduce stress?"],
        ["How do you recommend I handle recurring negative thoughts that contribute to my stress?"]
    ],
    title="Peace_maker"
)

if __name__ == "__main__":
    demo.launch()