import streamlit as st
from transformers import pipeline




st.set_page_config(page_title="Emotion prediction")
st.write("# Hi, Dear merchant👋")
st.markdown(
    """
    Want to gain insights about the emotion trend of your customers? 
    Just input a customer's comment into the box(in English format).
    """
)
st.title('Emotion prediction')
content = st.text_area("Please enter a customer's English comment (only one comment can be predicted at a time)", key = 0)



if st.button('Run', key=1):
    l = []
    with st.spinner('The system is loading and inferring model, please wait...'):
        @st.cache(hash_funcs={"MyUnhashableClass": lambda _: None}, allow_output_mutation=True)
        def load_model():
            classifier = pipeline("sentiment-analysis")
            return classifier

        model = load_model()
    l.append(content)
    r = model(l)
    st.write('The predicted emotion is', r[0]['label'])
    st.success('Model loading and inference successful!')

