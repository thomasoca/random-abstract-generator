import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import tensorflow as tf
from tensorflow import keras

load_model = tf.keras.models.load_model('data/title.h5', compile=False)
text = open('data/titles.txt', 'r').read()
vocab = sorted(set(text))
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)
def generate_text(model, start_string):
  # Number of characters to generate
  num_generate = 200
  min_generate = 50

  # Converting our start string to numbers (vectorizing)
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # Empty string to store our results
  text_generated = []

  temperature = 0.5

  step = 0
  model.reset_states()
  while step < num_generate:
      predictions = model(input_eval)
      predictions = tf.squeeze(predictions, 0)
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
      if idx2char[predicted_id] == '\n' and step > min_generate:
        text_generated.append(idx2char[predicted_id])
        break
      elif idx2char[predicted_id] == '\n' and step < min_generate:
        text_generated.append(' ')
        input_eval = tf.expand_dims([predicted_id], 0)
        step += 1
      else:
        text_generated.append(idx2char[predicted_id])
        input_eval = tf.expand_dims([predicted_id], 0)
        step += 1   
  return (start_string + ''.join(text_generated))

txt = (generate_text(load_model, start_string=u"Carbon"))
print(txt)
print(len(txt))