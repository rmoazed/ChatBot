#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import openai
import os


#this is relevant
from openai import OpenAI
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  
)


# In[59]:


import os
from flask import Flask, request, redirect
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a greeting and prompt for input."""
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/gather', speechModel = 'experimental_conversations')
    gather.say("Hello! Thank you for calling Stoked Pizza, the best pizzeria on the planet. Please ask me all about the menu, I love talking about it!", voice = 'Google.en-US-Neural2-I')

    resp.append(gather)
    
    return str(resp)

@app.route("/gather", methods=['GET', 'POST'])
def gather():
    df = pd.read_csv('results-2024-05-29T155224.csv')
    context = df.nlargest(1,'score').iloc[0]['text']
    """Process the speech input from the user and respond with OpenAI."""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        content = request.values['SpeechResult']
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:ai-lean::9TvnXq0q",
            messages= [{"role":"system","content":f"you are a helpful assistant that is extremely enthusiastic about pizza. You use lots of descriptive adjectives. You use the {context} to answer questions. Stoked Pizza is located in Washington Square, Brookline. Brookline is in Massachusetts. If a customer asks to place an order say you can't take their order at this time but they can call 617-879-0707 to place it right away. There is indoor and outdoor seating available. If you sit outside you have a lovely view of Washington Sqaure and the green line train zipping by. Inside the pizzeria it is a cozy atmosphere perfect for gathering with friends."},
                       {"role":"user","content":content}],
            max_tokens=150
        )
        ai_response = response.choices[0].message.content
        resp.say(ai_response, voice = 'Google.en-US-Neural2-I')
        gather = Gather(input='speech', action='/gather', speechModel = 'experimental_conversations')
        resp.append(gather)
        

        resp.redirect('/')

        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


# In[57]:




# In[ ]:




