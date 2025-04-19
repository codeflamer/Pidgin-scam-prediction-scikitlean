import gradio as gr
import utils as utils

from utils import normalize_text,preserve_pidgin,remove_contact_info,lemmatize,highlight_scam_terms

utils.load_model()
new_model = utils.model__ or None

def predict_scam(text):
    if new_model is None:
        return "Error: Model not loaded"
    response = new_model.predict([text])
    if response == 1:
        return "Omo them wan scam you o"
    return "Chillax everywhere cool"

# Create the interface
with gr.Blocks() as iface:
    gr.Markdown("# Nigerian Pidgin Scam Prediction",elem_classes='item-center')
    gr.Markdown("This app helps predict if a message/text is a scam or a harmless message",elem_classes='item-center')
    
    with gr.Row():
        text_input = gr.Textbox(label="Enter your text", placeholder="Type your message here...")
    with gr.Row():
        output = gr.Textbox(label="Prediction Result")
    
    predict_btn = gr.Button("Predict")
    predict_btn.click(fn=predict_scam, inputs=text_input, outputs=output)

iface.css = """
    .item-center{
        text-align:center;
        color:red;
    }
"""

if __name__ == "__main__":
    iface.launch()   