import sqlite3
import re
from PyPDF2 import PdfReader
import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
import spacy

nlp = spacy.load("fr_core_news_sm")

def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Recommandations de cours et certificats 🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choisissez le nombre de recommandations :', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

connection = sqlite3.connect('resume_parser.db')
cursor = connection.cursor()

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    resume_data2 = (name, email, str(res_score), timestamp, int(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses)
    cursor.execute('''INSERT INTO user_data(Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_Level, Actual_skills, Recommended_skills, Recommended_courses)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', resume_data2)
    connection.commit()

st.set_page_config(
   page_title="Analyseur de CV Intelligent"
)

def run():
    st.title("Analyseur de CV Intelligent à l'aide d'un parseur de CV")
    st.sidebar.markdown("# Choisissez l'utilisateur")
    activities = ["Utilisateur", "Admin"]
    choice = st.sidebar.selectbox("Choisissez une option :", activities)

    if choice == 'Utilisateur':
        pdf_file = st.file_uploader("Choisissez votre CV (format PDF)", type=["pdf"])
        if pdf_file is not None:
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)

            if 'data_inserted' not in st.session_state:
                st.session_state['data_inserted'] = False

            resume_text = pdf_reader(save_image_path)
            doc = nlp(resume_text)

            final_name = None
            name_spacy = next((ent.text for ent in doc.ents if ent.label_ == "PER"), None)
            if name_spacy:
                final_name = name_spacy.strip()
            else:
                lines = resume_text.strip().split('\n')
                for line in lines:
                    clean_line = line.strip()
                    if clean_line:
                        final_name = clean_line
                        break

            if not final_name:
                final_name = "Candidat inconnu"

            email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text)
            email = email_match.group(0) if email_match else "Email non trouvé"
            phone_match = re.search(r"\+?\d[\d\s\-]{7,}", resume_text)
            phone = phone_match.group(0) if phone_match else "Numéro non trouvé"

            skills_list = [
                'python', 'html', 'css', 'flask', 'pytorch', 'machine learning',
                'deep learning', 'data science', 'streamlit', 'nlp', 'speech recognition',
                'chatbot', 'git', 'docker', 'sql', 'tensorflow', 'keras', 'web scraping',
                'networking', 'tcp/ip', 'dns', 'dhcp', 'vpn', 'firewall', 'load balancing',
                'switches', 'routers', 'cisco', 'ccna', 'network security', 'ip addressing',
                'subnetting', 'routing protocols', 'lan', 'wan', 'vlan', 'snmp', 'wireshark',
                'telecommunication', 'gsm', 'lte', '5g', 'rf planning', 'voip', 'satellite systems',
                'fiber optics', 'signal processing', 'modulation', 'antenna theory', 'telecom protocols',
                'bts', 'network optimization', 'qos', 'spectrum analysis', 'mobile networks',
                'linux', 'windows server', 'bash', 'powershell', 'virtualization', 'vmware',
                'hyper-v', 'active directory', 'syslog', 'cloud computing', 'azure', 'aws'
            ]
            skills_found = [token.text for token in doc if token.text.lower() in skills_list]

            reader = PdfReader(save_image_path)
            num_pages = len(reader.pages)

            resume_data = {
                'name': final_name,
                'email': email,
                'mobile_number': phone,
                'skills': list(set(skills_found)),
                'no_of_pages': num_pages
            }

            if resume_data:
                st.header("**Analyse du CV**")
                st.success(f"Bonjour {resume_data['name']}")
                st.text(f"Nom : {resume_data['name']}")
                st.text(f"Email : {resume_data['email']}")
                st.text(f"Contact : {resume_data['mobile_number']}")
                st.text(f"Nombre de pages du CV : {resume_data['no_of_pages']}")

                if resume_data['no_of_pages'] == 1:
                    cand_level = "Débutant"
                    st.info("Vous semblez être débutant.")
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermédiaire"
                    st.info("Vous êtes de niveau intermédiaire.")
                else:
                    cand_level = "Expérimenté"
                    st.info("Vous êtes expérimenté.")

                st.subheader("**Recommandations de compétences 💡**")
                st_tags(label='### Vos compétences détectées',
                        text='Voici vos compétences détectées',
                        value=resume_data['skills'], key='1')

                if not st.session_state['data_inserted']:
                    ts = time.time()
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

                    insert_data(
                        resume_data['name'],
                        resume_data['email'],
                        0,
                        timestamp,
                        resume_data['no_of_pages'],
                        '',
                        cand_level,
                        str(resume_data['skills']),
                        '',
                        ''
                    )
                    st.session_state['data_inserted'] = True

            else:
                st.error("Erreur lors de l'analyse du CV.")

    else:
        st.success("Bienvenue dans l'espace administrateur")
        ad_user = st.text_input("Nom d'utilisateur")
        ad_password = st.text_input("Mot de passe", type='password')
        if st.button('Connexion'):
            if ad_user == 'admin' and ad_password == 'admin':
                st.success("Connexion réussie")
                cursor.execute('SELECT * FROM user_data')
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['ID', 'Nom', 'Email', 'Score CV', 'Horodatage', 'Nombre de pages', 'Domaine prédit', 'Niveau utilisateur', 'Compétences réelles', 'Compétences recommandées', 'Cours recommandés'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'donnees_utilisateur.csv', 'Télécharger le rapport'))
            else:
                st.error("Identifiants incorrects")

run()
