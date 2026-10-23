import gradio as gr


def greet(name: str) -> str:
    name = name.strip() if name else "World"
    return f"Hello, {name}!"


demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Name", placeholder="Enter your name"),
    outputs=gr.Textbox(label="Greeting"),
    title="Basic Gradio Demo",
    description="A minimal Gradio app for the huggingface-sync-action project.",
)


if __name__ == "__main__":
    demo.launch()
