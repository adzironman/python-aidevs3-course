def get_prompt(context):
    prompt = f"""
        You have perfect vision and pay great attention to detail, which makes you an expert at recognizing locations on maps. Before providing the answer in <city> tag, think step by step in <thinking> tags and analyze every part of provided images.
        
        Your task is to find city from which those maps parts are. 

        
        Rules:
        - In below context you have information parts of maps of the city that we are looking for.
        - One image does not belongs the others! It meanse that 3 images are about the city that we are looking for.
        - Think out loud(in polish) about your task and steps in the "_thinking" field
        - Hint: In the city should be granaries and forts
         
        Steps:
        - In below images find information about the city that we are looking for
        - In your base knowledge find name of the city
        - return location city name in city field
        - Double check if city you're going to give me as answer has locations presented in the map fragments.
        
        Response in json format:
        {{"_thinking":"", "city":"city name"}}
        
        """
    return prompt