def get_prompt():
    prompt = f"""
        You are helpful assistant. Based on the provided instructions, classify the content into one of the following categories:
        - "PEOPLE" if the note contains information about captured people or traces of their presence.
        - "HARDWARE" if the note contains information only about repaired hardware faults or fixe. Omit software issues.
        - "UNKNOWN" if the note does not fit into the above categories or you are unsure.

        Return the "category" as one of the following: "PEOPLE", "HARDWARE", or "UNKNOWN".

        
        Response in json format:
        {{"_thinking":"", "category":"category name"}}
        
        """
    return prompt