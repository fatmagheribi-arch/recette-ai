import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Generateur de Recettes IA", page_icon="🍽️")
st.title("🍽️ Generateur de Recettes avec IA")
st.write("Entre tes ingredients et l'IA te genere une recette complete !")

with st.form("recette_form"):
    ingredients = st.text_area(
        "Tes ingredients (separes par des virgules)",
        placeholder="ex: tomates, oeufs, fromage, basilic",
        height=100
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        personnes = st.selectbox("Nombre de personnes", [1, 2, 3, 4, 5, 6])
    with col2:
        regime = st.selectbox("Regime", ["Aucun", "Vegetarien", "Vegan", "Sans gluten"])
    with col3:
        cuisine = st.selectbox("Cuisine", ["Libre", "Francaise", "Italienne", "Asiatique", "Maghrebine"])
    submitted = st.form_submit_button("Generer la recette", use_container_width=True)

if submitted:
    if not ingredients.strip():
        st.error("Merci d'entrer au moins un ingredient !")
    else:
        with st.spinner("L'IA prepare ta recette..."):
            prompt = (
                "Tu es un chef cuisinier expert. Genere une recette complete en francais.\n"
                "Ingredients : " + str(ingredients) + "\n"
                "Personnes : " + str(personnes) + "\n"
                "Regime : " + str(regime) + "\n"
                "Cuisine : " + str(cuisine) + "\n\n"
                "Format:\n"
                "## Nom de la recette\n"
                "Temps de preparation : X minutes\n"
                "Temps de cuisson : X minutes\n"
                "Difficulte : Facile / Moyen / Difficile\n\n"
                "## Ingredients\n"
                "## Etapes\n"
                "## Conseil du chef"
            )
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024,
            )
            recette = response.choices[0].message.content
            st.success("Recette generee !")
            st.markdown(recette)
            st.download_button(
                label="Telecharger la recette",
                data=recette.encode("utf-8"),
                file_name="recette.txt",
                mime="text/plain"
            )