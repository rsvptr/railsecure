# modules/cybersecurity_quiz_module.py
# This module implements the Cybersecurity Knowledge Quiz feature.
# It generates multiple-choice questions using an LLM, displays them with interactive
# radio buttons, and provides instant feedback upon submission by comparing user answers
# to the correct answers provided by the LLM during question generation.

import streamlit as st
import re # Regular expressions for parsing the LLM's structured output
from utils.helpers import create_llm_messages # Helper to structure LLM prompts

# --- LLM Interaction for Quiz Question Generation ---

def _generate_quiz_questions_gpt(openai_client, num_questions=3):
    """
    Generates a specified number of multiple-choice quiz questions using an OpenAI model.

    The prompt instructs the LLM to provide questions, four options (A, B, C, D),
    the correct answer letter, and an explanation for each question, all in a
    strictly defined format to facilitate parsing.

    Args:
        openai_client (openai.OpenAI): The initialized OpenAI client.
        num_questions (int): The number of quiz questions to generate.

    Returns:
        str or None: A string containing the structured quiz data if successful,
                     otherwise None. Displays an error in Streamlit on failure.
    """
    # System prompt defining the AI's role and the precise output format required.
    # This detailed formatting instruction is crucial for reliable parsing.
    system_prompt = (
        f"You are a cybersecurity quiz master for Iarnród Éireann. "
        f"Your primary goal is to generate {num_questions} distinct multiple-choice quiz questions. These questions should be relevant to cybersecurity compliance (such as NIS2, GDPR, the Irish Data Protection Act 2018), Operational Technology (OT) security within the rail sector, or general cybersecurity best practices pertinent to Iarnród Éireann staff. "
        "For each question you generate, you must provide: the question text, four plausible options labeled A, B, C, and D, the single letter of the correct answer, and a brief, clear explanation for why that answer is correct. "
        "Adhere strictly to the following format for EACH question. Use '---END_QUESTION---' as a precise separator after each complete question block (including its explanation):\n"
        "Question: <Full Question Text Here>\n"
        "A: <Text for Option A>\n"
        "B: <Text for Option B>\n"
        "C: <Text for Option C>\n"
        "D: <Text for Option D>\n"
        "Correct Answer: <Single Correct Option Letter, e.g., A or B or C or D>\n"
        "Explanation: <Brief and clear explanation for why the correct answer is indeed correct. This explanation should be concise and directly relate to the question and correct option.>\n"
        "---END_QUESTION---\n"
        "Ensure all options (A, B, C, D) are distinct and plausible to make the quiz challenging but fair. Your entire response must consist only of these structured question blocks. Do not add any preamble or extra commentary."
    )
    user_prompt = f"Generate exactly {num_questions} cybersecurity quiz questions now, following all formatting instructions precisely."

    try:
        # API call to OpenAI to generate quiz questions
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Specify the model
            messages=create_llm_messages(system_prompt, user_prompt),
            temperature=0.75, # A balance for varied yet relevant questions
            max_tokens=300 * num_questions # Estimate token usage per question
        )
        # Return the AI's response text
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Handle errors during API call
        st.error(f"An error occurred while generating quiz questions: {e}")
        return None

# --- Parsing Function for Quiz Data ---

def parse_quiz_data(raw_quiz_text):
    """
    Parses the raw structured text output from the LLM into a list of question objects.

    Each question object is a dictionary containing:
    - 'text': The question text (str).
    - 'options': A dictionary of options, e.g., {"A": "Option A", "B": "Option B", ...}.
    - 'correct_answer': The letter of the correct option (str, e.g., "A").
    - 'explanation': The explanation for the correct answer (str).

    Args:
        raw_quiz_text (str): The raw string output from the LLM, expected to follow
                             the format defined in `_generate_quiz_questions_gpt`.

    Returns:
        list: A list of parsed question dictionaries. Returns an empty list if
              parsing fails or no valid questions are found.
    """
    parsed_questions = []
    if not raw_quiz_text: # Handle empty input
        st.warning("Received no data to parse for quiz questions.")
        return parsed_questions

    # Split the raw text into blocks, each representing a single question
    question_blocks = raw_quiz_text.strip().split("---END_QUESTION---")
    
    for i, block_content in enumerate(question_blocks):
        block_content = block_content.strip()
        if not block_content: # Skip any empty blocks resulting from split
            continue

        # Initialize dictionary to hold data for the current question
        current_question_data = {"text": None, "options": {}, "correct_answer": None, "explanation": None}
        lines = block_content.split('\n') # Split the block into individual lines
        
        # Process each line to extract question parts
        for line in lines:
            line = line.strip()
            if not line: continue # Skip empty lines within a block

            try: # Use try-except for robustness in splitting lines
                if line.lower().startswith("question:"):
                    current_question_data["text"] = line.split(":", 1)[1].strip()
                elif line.lower().startswith("a:"):
                    current_question_data["options"]["A"] = line.split(":", 1)[1].strip()
                elif line.lower().startswith("b:"):
                    current_question_data["options"]["B"] = line.split(":", 1)[1].strip()
                elif line.lower().startswith("c:"):
                    current_question_data["options"]["C"] = line.split(":", 1)[1].strip()
                elif line.lower().startswith("d:"):
                    current_question_data["options"]["D"] = line.split(":", 1)[1].strip()
                elif line.lower().startswith("correct answer:"):
                    ans_text = line.split(":", 1)[1].strip()
                    # Ensure the extracted answer is a single valid letter
                    if ans_text and ans_text[0].upper() in "ABCD":
                        current_question_data["correct_answer"] = ans_text[0].upper()
                elif line.lower().startswith("explanation:"):
                    current_question_data["explanation"] = line.split(":", 1)[1].strip()
            except IndexError: # Catch error if a line doesn't contain ":" for splitting
                st.warning(f"Skipping malformed line in question block #{i+1}: '{line}'")
                continue
        
        # Validate if all parts of the question were successfully parsed
        if (current_question_data["text"] and 
            len(current_question_data["options"]) == 4 and # Ensure all 4 options are present
            all(opt_key in current_question_data["options"] for opt_key in "ABCD") and
            current_question_data["correct_answer"] and 
            current_question_data["explanation"]):
            parsed_questions.append(current_question_data)
        else:
            # Log or warn about incompletely parsed questions, useful for debugging LLM format adherence
            # st.warning(f"Could not fully parse question block #{i+1}. Data: {current_question_data}. Preview: {block_content[:100]}")
            pass # Optionally, silently skip malformed blocks in production

    if not parsed_questions and raw_quiz_text: # If input was given but no questions were parsed
        st.error("No valid questions could be parsed from the AI's response. The format might have been incorrect. Please try generating again.")
            
    return parsed_questions

# --- Main Display Function for the Module ---

def display_cybersecurity_quiz(openai_client):
    """
    Displays the main UI for the Cybersecurity Knowledge Quiz module.
    Allows users to generate a set of questions, answer them using radio buttons
    within a form, and then view their score and detailed feedback.

    Args:
        openai_client (openai.OpenAI or None): The initialized OpenAI client.
                                               If None, question generation will be disabled.
    """
    st.subheader("🧠 Cybersecurity Knowledge Quiz")
    st.write(
        "Test your understanding of key cybersecurity concepts, compliance requirements, and best practices "
        "relevant to Iarnród Éireann. A new set of questions is generated each time!"
    )

    # Slider for user to choose the number of questions for the quiz
    num_questions_to_generate = st.slider(
        "Number of questions for this quiz:", 
        min_value=1, 
        max_value=6, # Max can be adjusted; consider LLM token limits & UI
        value=3,     # Default number of questions
        key="num_quiz_questions_slider" # Unique key for the slider widget
    )

    # Button to generate new quiz questions
    if st.button(f"🎲 Generate {num_questions_to_generate} New Quiz Question(s)", key="generate_quiz_button"):
        if not openai_client: # Check if OpenAI client is available
            st.error("OpenAI client is not available. Cannot generate quiz questions.")
            st.session_state["parsed_quiz_questions"] = None # Clear any old questions
            return
        
        # Show spinner while generating questions
        with st.spinner(f"Generating {num_questions_to_generate} fresh quiz questions... Please wait."):
            raw_questions_data = _generate_quiz_questions_gpt(openai_client, num_questions_to_generate)
            if raw_questions_data: # If data was returned from LLM
                parsed_data = parse_quiz_data(raw_questions_data) # Attempt to parse
                if parsed_data: # If parsing was successful
                    st.session_state["parsed_quiz_questions"] = parsed_data
                else: # Parsing failed
                    st.error("Failed to parse valid quiz questions from the AI's response. The format might have been incorrect or no valid questions were found. Please try generating again.")
                    st.session_state["parsed_quiz_questions"] = None 
            else: # LLM generation failed
                st.error("The AI failed to generate quiz questions. Please try again.")
                st.session_state["parsed_quiz_questions"] = None
            
            # Reset previous evaluation feedback and user selections for the new quiz
            st.session_state["quiz_evaluation_feedback"] = None 
            st.session_state["user_quiz_selections"] = {} 

    # If quiz questions are parsed and available in session state, display them
    if "parsed_quiz_questions" in st.session_state and st.session_state["parsed_quiz_questions"]:
        st.markdown("---") # Visual separator
        st.markdown("#### Quiz Time! Select the best answer for each question.")
        
        parsed_questions = st.session_state["parsed_quiz_questions"]

        # Use a form to collect all answers before submission
        with st.form(key="cybersecurity_quiz_form"):
            user_selections_in_form = {} # Temporary dictionary to hold selections for this form submission
            
            # Iterate through each parsed question to display it
            for i, q_data in enumerate(parsed_questions):
                # Basic check for malformed question data from parser
                if not isinstance(q_data, dict) or not all(k in q_data for k in ["text", "options", "correct_answer", "explanation"]):
                    st.error(f"Skipping display of malformed question #{i+1}.")
                    continue

                st.markdown(f"**Question {i+1}:** {q_data['text']}") # Display question text
                
                # Format options for st.radio: ["A. Option Text A", "B. Option Text B", ...]
                radio_options = [f"{key}. {text}" for key, text in q_data["options"].items()]
                
                # Create a radio button group for the current question's options
                user_choice_for_q = st.radio(
                    label=f"Options for Question {i+1}:", # Label for accessibility, hidden by label_visibility
                    options=radio_options, 
                    key=f"quiz_q_{i}_choice", # Unique key for each radio group
                    label_visibility="collapsed" # Hides the label "Options for Question X:"
                )
                if user_choice_for_q:
                    # Extract the selected option letter (e.g., "A") from the radio button's string value
                    user_selections_in_form[i] = user_choice_for_q.split('.')[0]
            
            # Submit button for the form
            submitted_quiz = st.form_submit_button("✅ Submit All Answers")

            if submitted_quiz:
                # Store the user's final selections in session state
                st.session_state["user_quiz_selections"] = user_selections_in_form 
                
                # --- Perform Local Evaluation (No LLM call needed here) ---
                feedback_html_parts = [] # List to build HTML feedback string
                num_correct = 0
                total_questions = len(parsed_questions)

                # Iterate through questions again to compare user answers with correct answers
                for i, q_data in enumerate(parsed_questions):
                    user_ans_letter = user_selections_in_form.get(i) # User's selected letter for this question
                    correct_ans_letter = q_data["correct_answer"]    # Correct answer letter from parsed data
                    
                    # Get full text for user's answer and correct answer for display
                    user_ans_text = q_data["options"].get(user_ans_letter, "Not answered") if user_ans_letter else "Not answered"
                    correct_ans_full_text = f"{correct_ans_letter}. {q_data['options'].get(correct_ans_letter, 'N/A')}"

                    # Start div for this question's feedback for better styling
                    feedback_html_parts.append(f"<div style='margin-bottom: 20px; padding: 10px; border-left: 5px solid #666; background-color: rgba(255,255,255,0.03); border-radius: 5px;'>")
                    feedback_html_parts.append(f"<p><b>Question {i+1}:</b> {q_data['text']}</p>") # Display question

                    is_correct = (user_ans_letter == correct_ans_letter)
                    if is_correct:
                        num_correct += 1
                        feedback_html_parts.append(f"<p style='color: #4CAF50;'>Your answer: <b>{user_ans_letter}. {user_ans_text} (Correct!)</b> ✅</p>")
                    else:
                        feedback_html_parts.append(f"<p style='color: #F44336;'>Your answer: <b>{user_ans_letter if user_ans_letter else ''}{'. ' + user_ans_text if user_ans_letter else 'No answer selected'} (Incorrect)</b> ❌</p>")
                        feedback_html_parts.append(f"<p>Correct answer: <b>{correct_ans_full_text}</b></p>")
                    
                    # Add the explanation (provided by the LLM during question generation)
                    feedback_html_parts.append(f"<p><i>Explanation:</i> {q_data['explanation']}</p>")
                    feedback_html_parts.append("</div>") # Close div for this question's feedback

                # Calculate score percentage
                score_percentage = (num_correct / total_questions) * 100 if total_questions > 0 else 0
                # Create score header
                score_header = f"<h2>Your Score: {num_correct} out of {total_questions} ({score_percentage:.0f}%)</h2><hr>"
                
                # Store the complete HTML feedback in session state
                st.session_state["quiz_evaluation_feedback"] = score_header + "".join(feedback_html_parts)

    # Display the evaluation feedback if it exists in session state
    if "quiz_evaluation_feedback" in st.session_state and st.session_state["quiz_evaluation_feedback"]:
        st.markdown("---") # Visual separator
        st.markdown(st.session_state["quiz_evaluation_feedback"], unsafe_allow_html=True) # Render HTML
