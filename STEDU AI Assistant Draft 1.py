#Imports google gemini into code


from google import genai

#KEY:
# - This key does have some limits to how much it can generate, and usually wed set it up so that its not hardcoded but then its not possible to share it
client = genai.Client(api_key="AIzaSyCDSu64FdW0_AK2HFYP1wJf4FRcn-KZv7Y")

# input:
incomingMessage = client.files.upload(file="test_email.txt")
def ParentResponse(incomingMessage):
    """Function that will read over an incoming message from a parent and generate a response"""
    #response:
    # - uses google geminis libraries to generate a response
    response = client.models.generate_content(  
    model="gemini-2.5-flash", 
    contents = ["Generate a response to the following email from a parent", incomingMessage]
    )
    return response.text

print(ParentResponse(incomingMessage))