import streamlit as st
from PIL import Image
from deepface import DeepFace
import google.generativeai as genai

# Configure the Google Generative AI API
genai.configure(api_key="AIzaSyDR3z9bQuZBbRkY6wJLBgdW3nx2T5VekQs")
generation_config = {
  "temperature": 1.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
 
)

# Function to generate motivational quotes using Google LLM API
def generate_quotes(age, gender, emotion):
    # Start a chat session with Google LLM
    chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "\"Provide 4 thoughtful, motivational, or relevant quotes for a person based on the following characteristics:Age: {21}Gender: {male}Emotion: {sad}The quotes should resonate with the person's current emotional state and be appropriate for their age and gender. Please ensure that the quotes reflect empathy, encouragement, and positivity.\"\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1. On Resilience:\n\"Strength grows in moments when you think you can’t go on, but you keep going anyway.\"\n2. On Overcoming Challenges:\n\"The struggle you're in today is developing the strength you need for tomorrow.\"\n3. On Finding Hope:\n\"Even the darkest night will end, and the sun will rise.\"\n4. On Taking Small Steps:\n\"You don’t have to see the whole staircase, just take the first step.\"\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "\"Provide 4 thoughtful, motivational, or relevant quotes for a person based on the following characteristics:Age: {21}Gender: {female}Emotion: {sad}The quotes should resonate with the person's current emotional state and be appropriate for their age and gender. Please ensure that the quotes reflect empathy, encouragement, and positivity.\"\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1. On Self-Compassion:  \"It's okay not to be okay.  Allow yourself to feel what you feel, and be kind to yourself in the process.\" \n\n2. On Healing: \"The wound is the place where the Light enters you.\" \n\n3. On Inner Strength:  \"You are stronger than you think.  Even in this moment of sadness, you possess a resilience you may not even realize. Trust in your ability to overcome this.\"  \n\n4. On Moving Forward: \"One day you will tell your story of how you overcame what you’re going through now, and it will become part of someone else’s survival guide.\" \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "\"Provide 4 thoughtful, motivational, or relevant quotes for a person based on the following characteristics:Age: {21}Gender: {male}Emotion: {sad}The quotes should resonate with the person's current emotional state and be appropriate for their age and gender. Please ensure that the quotes reflect empathy, encouragement, and positivity.\"",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1. On Feeling Your Feelings: \"It's okay to feel sad, man.  Don't try to bottle it up.  Let yourself process it, and know that it won't last forever.\"\n\n2. On Finding Strength: \"The oak fought the wind and was broken, the willow bent when it must and survived.\"  This reminds us that sometimes adapting and accepting our vulnerability is a form of strength.\n\n3. On the Future: \"Storms don't last forever.  You've weathered tough times before, and you'll get through this too.  Brighter days are ahead.\"\n\n4. On Taking Action: \"Even small steps forward can make a big difference. What's one thing you can do today, no matter how small, that will make you feel even a little bit better?\"\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "\"Provide 4 thoughtful, motivational, or relevant quotes for a person based on the following characteristics:Age: {21}Gender: {male}Emotion: {fear}The quotes should resonate with the person's current emotional state and be appropriate for their age and gender. Please ensure that the quotes posses empathy, encouragement, and positivity.\"",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1. On Courage: \"Courage isn't the absence of fear, it's feeling the fear and doing it anyway.\"  \n\n2. On Growth:  \"Everything you want is on the other side of fear.\" \n\n3. On Perspective:  \"What if I fall? Oh, but my darling, what if you fly?\" \n\n4. On Self-Trust: \"You are braver than you believe, stronger than you seem, and smarter than you think.\"\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "\"Provide 4 thoughtful, motivational, or relevant quotes for a person based on the following characteristics:Age: {21}Gender: {male}Emotion: {fear}The quotes should resonate with the person's current emotional state and be appropriate for their age and gender. Please ensure that the quotes reflect empathy, encouragement, and positivity.\"",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1. On Acknowledging Fear: \"It's okay to be afraid. Fear is a natural human response.  Acknowledging it is the first step to overcoming it.\"\n\n2. On Facing Fear:  \"Fear is a liar. It tells you you're not strong enough, smart enough, or brave enough.  Prove it wrong.\"\n\n3. On The Power of Action: \"Action is the antidote to fear. One small step can often break the paralysis of fear and get you moving forward.\"\n\n4. On Finding Support:  \"You don't have to face your fears alone.  Talking to someone you trust can help you gain perspective and find the courage you need.\" \n",
      ],
    },
  ]
)

    # Send message and receive quotes
    response = chat_session.send_message(
        f"Provide 4 thoughtful, motivational, or relevant quotes for a person based on the following characteristics:Age:{age}Gender:{gender}Emotion: {emotion}The quotes should resonate with the person's current emotional state and be appropriate for their age and gender. Please ensure that the quotes reflect empathy, encouragement, and positivity.Only Quotes no need of explanation"
    )

    return response.text

# Set up Streamlit
st.title("Real-time Motivational Quote Generator")
st.write("This app captures your image, detects your age, gender, and emotion, and provides personalized motivational quotes.")

# Stream from the camera and capture image
img_file = st.camera_input("Take a picture")

if img_file:
    # Convert the image to a format suitable for DeepFace
    img = Image.open(img_file)
    img.save("temp_image.jpg")

    # Analyze the image
    attributes = DeepFace.analyze(img_path="temp_image.jpg", actions=['age', 'gender', 'emotion'])

    # Since the result is a list, access the first item (index 0) before retrieving the details
    if isinstance(attributes, list):
        attributes = attributes[0]  # Access the first dictionary in the list

    # Extract relevant attributes
    age = attributes['age']
    gender = attributes['dominant_gender']
    emotion = attributes['dominant_emotion']

    # Now you can use these attributes for further processing
    st.write(f"Age: {age}, Gender: {gender}, Emotion: {emotion}")

    # Generate motivational quotes based on the attributes
    quotes = generate_quotes(age, gender, emotion)

    # Display the generated quotes
    st.write("Here are your personalized motivational quotes:")
    st.write(quotes)
