import streamlit as st
import tensorflow as tf


a=tf.constant([1,5],dtype=tf.int64)

st.write('The current movie title is', a)


