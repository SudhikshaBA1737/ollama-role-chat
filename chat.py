import time
try:
    import ollama
except ImportError:
    print("The 'ollama' library is not installed. Please install it using 'pip install ollama'")
    exit(1)

def print_menu(roles):
    print("\n" + "="*30)
    print("         ROLE MENU")
    print("="*30)
    for idx, role in enumerate(roles.keys(), 1):
        print(f" {idx}. {role}")
    print("-" * 30)
    print(" Commands:")
    print(" - Type 'quit' to exit.")
    print(" - Type 'switch' during chat to return here.")
    print(" - Type 'roles' to add a custom role.")
    print("="*30)

def main():
    model_name = 'llama3.2' # Built-in default. Keep in mind you need to have this model pulled.
    
    roles = {
        "Python Tutor": "You are an expert Python tutor. Explain concepts clearly and concisely with code examples.",
        "Fitness Coach": "You are a motivating fitness coach. Provide workout advice and diet tips based on user goals.",
        "Travel Guide": "You are a knowledgeable travel guide. Give recommendations for places to visit, eat, and stay."
    }

    print("Welcome to Role-Based Chat with Ollama!")
    print(f"Make sure you have pulled the model! (Run 'ollama pull {model_name}' in your terminal if needed)")
    
    current_role_name = None
    messages = []
    
    while True:
        if current_role_name is None:
            print_menu(roles)
            choice = input("\nSelect a role by number, or type a command: ").strip().lower()
            
            if choice == 'quit':
                print("Goodbye!")
                break
            elif choice == 'roles':
                print("\n--- Add Custom Role ---")
                new_role_name = input("Enter the name for the new role: ").strip()
                new_role_prompt = input("Enter the system prompt for this role: ").strip()
                if new_role_name and new_role_prompt:
                    roles[new_role_name] = new_role_prompt
                    print(f"\n=> Role '{new_role_name}' added successfully!")
                else:
                    print("\n=> Invalid input. Name and prompt cannot be empty.")
                continue
            elif choice == 'switch':
                print("You are already at the menu.")
                continue
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(roles):
                    current_role_name = list(roles.keys())[idx - 1]
                    # Start fresh conversation for the new role with system prompt
                    messages = [{"role": "system", "content": roles[current_role_name]}]
                    print(f"\n=> Switched to role: {current_role_name}. You can start chatting!")
                else:
                    print("=> Invalid option number.")
                continue
            else:
                print("=> Invalid input. Please try again.")
                continue
        
        user_input = input(f"\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'switch':
            current_role_name = None
            continue
        elif not user_input:
            continue
            
        messages.append({"role": "user", "content": user_input})
        
        print(f"\n{current_role_name}: ", end="", flush=True)
        
        try:
            start_time = time.time()
            response = ollama.chat(
                model=model_name,
                messages=messages,
                stream=True
            )
            
            assistant_response = ""
            for chunk in response:
                content = chunk.get('message', {}).get('content', '')
                print(content, end="", flush=True)
                assistant_response += content
                
            print() # newline after response completes
            end_time = time.time()
            time_taken = end_time - start_time
            
            print(f"\n[Response time: {time_taken:.2f} seconds]")
            
            messages.append({"role": "assistant", "content": assistant_response})
            
        except ollama.ResponseError as e:
            if "not found" in str(e).lower():
                print(f"\n[Error: Model '{model_name}' not found. Please run 'ollama pull {model_name}' or change the model_name in the script.]")
            else:
                print(f"\n[Ollama API Error: {e}]")
            messages.pop() # remove user message since it failed
        except Exception as e:
            print(f"\n[Error connecting to Ollama: {e}]")
            print("[Ensure Ollama is installed and running]")
            messages.pop() # remove user message since it failed

if __name__ == "__main__":
    main()
