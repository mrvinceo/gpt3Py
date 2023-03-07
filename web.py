import gradio as gr
import openai, config
openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": "You are a helpful assistant to students and teachers."}]
def transcribe(audio):
    global messages
    print(audio)

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})
    response =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    system_message = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": system_message})
    
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    
    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()