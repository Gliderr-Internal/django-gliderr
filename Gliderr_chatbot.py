from openai import OpenAI
import json

class GoalBreakdownAgent:
    """
    A Goal Breakdown Assistant that helps users achieve their goals by breaking them into actionable steps.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.system_prompt = """
        You are a Goal Breakdown Assistant called Gliderr. Your purpose is to help users achieve their goals by breaking them into actionable steps and creating a personalized 7-day plan. Follow these instructions:

        1. **Purpose & Goal Clarification**:
           - Ask the user to define a singular goal (e.g., "I want to create a YouTube channel").
           - If the user provides multiple goals, gently encourage them to focus on just one for now.

        2. **Understanding the User's Schedule**:
           - Ask the user the following questions individually: 
           -Make sure to ask each question separately, get the answer and then go to the next question.
             - How their typical week looks.
             - What days and times they are available.
             - How much time they can allocate each day to their goal.
             - Their time zone (to ensure accurate scheduling).

        3. **Breaking Down the Goal into Actionable Steps**:
           - Once the user's availability is clear:
             - Break the goal into small, realistic tasks.
             - Distribute these tasks over a 7-day period.
             - Ensure tasks fit into the user's available time slots.
             - Adjust the plan if the user has limitations or concerns.

        4. **Personalized Planning & Time-Based Scheduling**:
           - Schedule tasks for specific times based on the user's availability.Include time for the tasks like 10 AM - 11 AM
           - Present the plan in a clear and organized format.
        
        Generate the schedule in 2 formats:
        1. User readable format
        2. Json format

        When generating the schedules follow the below instructions:
        1. User readable format should be generated first
        2. Ask the user to confirm the generated schedule to generate the JSON format
        3. Do not mention to the user that you'll be generating the JSON format. just ask them to confirm the schedule
        3. JSON format should be generated only after the user agrees or accepts the user readable format first. 
        4. JSON format should be generated in the following format (do not show it to the user):
             [
                'day1': {
                     "objective": "Task description",
                     "time": "Time allocated"
                 },
                 'day2':{
                     "objective": "Task description",
                     "time": "Time allocated"
                 },
                 ...
             ]

        Always be polite, empathetic, and supportive. If the user has questions or concerns, address them promptly.
        """
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        self.schedule=[]

        # Configure the OpenAI package to use DeepSeek's API
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        # Replace with DeepSeek's API base URL

    def chat(self, user_input):
        """
        Sends user input to the DeepSeek AI agent and returns the response.
        """
        # Add the user's input to the conversation history
        self.conversation_history.append({"role": "user", "content": user_input})

        try:
            # Send the request to DeepSeek AI
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # Replace with the correct model name for DeepSeek
                messages=self.conversation_history,
                max_tokens=1000,  # Adjust as needed
            )
            

            # Extract the bot's response
            bot_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": bot_response})

            if "[" in bot_response and "]" in bot_response:
                try:
                    # Extract the JSON schedule from the bot's response
                    start_index = bot_response.find("[")
                    end_index = bot_response.rfind("]") + 1
                    json_schedule = bot_response[start_index:end_index]

                    # Parse the JSON schedule
                    self.schedule = json.loads(json_schedule)

                    # Remove the JSON part from the bot's response before displaying it to the user
                    bot_response = "Awesome! Your schedule will be added to the calender"
                    print(self.schedule)
                except json.JSONDecodeError:
                    print("Error: Failed to parse the schedule as JSON.")
            # else:
            #     print("No JSON schedule found in the bot's response.")

            

            return bot_response

        except Exception as e:
            return f"Error: Failed to communicate with DeepSeek AI. {str(e)}"
        
    
      


    def reset_conversation(self):
        """
        Resets the conversation history.
        """
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]


def main():
    """
    Main function to test the Goal Breakdown Agent in the terminal.
    """
    api_key = ""  # Replace with your DeepSeek API key
    agent = GoalBreakdownAgent(api_key)

    print("Gliderr: Hi! I'm here to help you achieve your goals. Let's start by defining your goal.")
    print("Type 'exit' or 'quit' to end the conversation. Type 'reset' to start over.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Gliderr: Goodbye! Good luck with your goal!")
            break

        if user_input.lower() == "reset":
            agent.reset_conversation()
            print("Gliderr: Conversation reset. Let's start over!")
            continue

        bot_response = agent.chat(user_input)
        print(f"Gliderr: {bot_response}")


if __name__ == "__main__":
    main()