#Imports google gemini into code
# - It was a bit of a struggle to get this up and running, but the hardest part is installing google-genai
# - I had to use googles official guide, but I ran into the issue of VS wanting to use conda, which genai didnt like
# - if you run into the same issue, try this:
    # - in the terminal, type:
        # - python3 -m venv <enviromnt_name_here> to set up a virtual environment
        # - source venv/bin/activate to activate the environment
        # - pip install -U google-genai to venv
    # and it should work. if not let me know and I can try my best to help

from google import genai

#KEY:
# - This key does have some limits to how much it can generate, and usually wed set it up so that its not hardcoded but then its not possible to share it
client = genai.Client(api_key="AIzaSyCDSu64FdW0_AK2HFYP1wJf4FRcn-KZv7Y")



#input:
# - input from user which the GenAi will then read and generate a unique respons!!! 
userPrompt = input("Please enter some text:")


#response:
# - uses google geminis libraries to generate a response
response = client.models.generate_content(
    model="gemini-2.5-flash", contents = userPrompt
)
print(response.text)

# - NOTE: THIS IS VERY VERY BASIC. Im thinking we can use this for the generation of templates when it comes to parent communications and even the IEP summary!
