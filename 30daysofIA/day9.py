"""  Day 9
Understanding Session State
For today's challenge, our goal is to solve the Amnesia Problem in 
Streamlit apps. 
We need to understand why standard variables reset on every interaction 
and how to use Session State to preserve data. Once that's done, we will
have a counter that actually remembers its value as you click buttons. """

import streamlit as st
st.title(":material/memory: Understanding Session State")
st.warning("**Instructions:** Tente clicar nos botões de + e - para ver a diferença")
col1,col2=st.columns(2)
with col1:
    st.header(":material/cancel: Standard Variable")
    st.write("This resets on every click.")

    count_wrong = 0
    subcol_left, subcol_right = st. columns(2)
    
    with subcol_left:
        if st.button(":material/add:", key="std_plus"):
            count_wrong += 1

    with subcol_right:
        if st.button(":material/remove:", key="std_minus"):
            count_wrong -= 1
    
    st.metric("Standard Count", count_wrong)
    st.caption("Nunca vai passar de 1 ou de -1 porque o 'count_wrong' reseta pra zero antes da matématica acontecer (a página recarrega)")
    
with col2:
    st.header(":material/check_circle: Session State")
    st.write("Essa memória persiste.")

    if "counter" not in st.session_state:
        st.session_state.counter = 0
        
    subcol_left_2, subcol_right_2 = st. columns(2)
    
    with subcol_left_2:
        if st.button(":material/add:", key="state_plus"):
            st.session_state.counter+=1
        
    with subcol_right_2:
        if st.button(":material/remove:", key="state_minus"):
            st.session_state.counter-=1
            
    st.metric("State Count", st.session_state.counter)
    st.caption("Aqui funciona porque apenas setamos o contador para zero se a session_state não existir.")
        

st.divider()
st.caption("Day 9: Understanding Session State | 30 Days of AI")