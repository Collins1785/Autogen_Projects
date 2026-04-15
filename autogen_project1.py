import streamlit as st
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


# ============================================================
# MODEL CLIENT
# ============================================================
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================================
# AGENTS
# ============================================================
interviewer = AssistantAgent(
    name="interviewer",
    model_client=model_client,
    system_message="You are an interviewer. Ask clear possible interview question for the given role."
)

coach = AssistantAgent(
    name="coach",
    model_client=model_client,
    system_message="You are a coach. Give 3 concise bullet point improvements for the answer."
)

scorer = AssistantAgent(
    name="scorer",
    model_client=model_client,
    system_message="""
    You are a strict evaluator.
    Score the answer from 1 to 10.
    Format:
    Score: X/10
    Reason: ...
    """
)


# ============================================================
# ASYNC-SAFE WRAPPER
# ============================================================
def run_async(coro):
    """Safe async wrapper for Streamlit."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        return asyncio.ensure_future(coro)
    else:
        return loop.run_until_complete(coro)


# ============================================================
# AGENT HELPERS
# ============================================================
def ask_question(role, history):
    """Generate a NEW question avoiding repetition."""
    previous = "\n".join([f"- {item['q']}" for item in history])

    prompt = f"""
    Ask one NEW interview question for the role: {role}.
    Do NOT repeat any previous questions.
    Previous questions:
    {previous if previous else "None"}
    """

    resp = run_async(interviewer.run(task=prompt))
    if asyncio.isfuture(resp):
        resp = asyncio.get_event_loop().run_until_complete(resp)

    return resp.messages[-1].content


def get_feedback(question, answer):
    resp = run_async(coach.run(task=f"Provide feedback for:\nQ: {question}\nA: {answer}"))
    if asyncio.isfuture(resp):
        resp = asyncio.get_event_loop().run_until_complete(resp)
    return resp.messages[-1].content


def get_score(question, answer):
    resp = run_async(scorer.run(task=f"Evaluate:\nQ: {question}\nA: {answer}"))
    if asyncio.isfuture(resp):
        resp = asyncio.get_event_loop().run_until_complete(resp)
    return resp.messages[-1].content


# ============================================================
# STREAMLIT UI
# ============================================================
st.title("💼 AI Interviewer — Smart Interview Practice")


# ============================================================
# SIDEBAR CONTROLS
# ============================================================
st.sidebar.header("⚙️ Interview Settings")

role = st.sidebar.text_input("Job Role", "Software Engineer")

num_questions = st.sidebar.slider("Number of Questions", 1, 5, 3)

if st.sidebar.button("Reset Interview"):
    st.session_state.clear()
    st.rerun()


# ============================================================
# SESSION STATE INIT
# ============================================================
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.history = []
    st.session_state.show_result = False
    st.session_state.role_locked = False


# ============================================================
# START INTERVIEW
# ============================================================
if not st.session_state.role_locked:
    if st.button("Start Interview"):
        if role.strip() == "":
            st.warning("Please enter a role")
        else:
            st.session_state.role = role
            st.session_state.role_locked = True
            st.session_state.question = ask_question(role, st.session_state.history)
            st.rerun()


# ============================================================
# INTERVIEW FLOW
# ============================================================
elif st.session_state.step < num_questions:

    st.write(f"**Role:** {st.session_state.role}")
    st.subheader(f"Question {st.session_state.step + 1} of {num_questions}")
    st.write(st.session_state.question)

    answer = st.text_area("Your Answer", key=f"answer_{st.session_state.step}")

    if not st.session_state.show_result:
        if st.button("Submit Answer"):
            if answer.strip() == "":
                st.warning("Please enter an answer")
            else:
                feedback = get_feedback(st.session_state.question, answer)
                score = get_score(st.session_state.question, answer)

                st.session_state.current_answer = answer
                st.session_state.current_feedback = feedback
                st.session_state.current_score = score

                st.session_state.show_result = True
                st.session_state.saved = False
                st.rerun()

    else:
        st.subheader("📊 Feedback")
        st.write(st.session_state.current_feedback)

        st.subheader("🏆 Score")
        st.write(st.session_state.current_score)

        if not st.session_state.saved:
            st.session_state.history.append({
                "q": st.session_state.question,
                "a": st.session_state.current_answer,
                "f": st.session_state.current_feedback,
                "s": st.session_state.current_score
            })
            st.session_state.saved = True

        if st.button("Next Question"):
            st.session_state.step += 1
            st.session_state.show_result = False

            if st.session_state.step < num_questions:
                st.session_state.question = ask_question(
                    st.session_state.role,
                    st.session_state.history
                )

            st.rerun()


# ============================================================
# FINAL SUMMARY
# ============================================================
else:
    st.success("🎉 Interview Completed!")

    total_score = 0

    for i, item in enumerate(st.session_state.history):
        st.subheader(f"Question {i+1}")
        st.write(item["q"])

        st.write("**Your Answer:**")
        st.write(item["a"])

        st.write("**Feedback:**")
        st.write(item["f"])

        st.write("**Score:**")
        st.write(item["s"])

        try:
            score_value = int(item["s"].split("/")[0].split(":")[-1].strip())
            total_score += score_value
        except:
            pass

    avg_score = total_score / len(st.session_state.history)
    st.subheader(f"🎯 Average Score: {avg_score:.1f}/10")
