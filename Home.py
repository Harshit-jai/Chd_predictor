def main():
    import streamlit as st
    import pickle
    import helper
    import pandas as pd
    import time
    my_data = {}
    descriptions = {}
    data = {}

    # Full forms and descriptions of each point
    descriptions = {
        'Name': "Full name of the patient",
        'Sex': "Sex of the patient",
        'chest_pain': """ 
        - **Typical chest pain** feels like pressure or squeezing in the center of the chest, often worsening with activity or stress. It might spread to the neck, jaw, arms, or back and can be relieved by rest or medication. \n 
        - **Atypical chest pain**, on the other hand, can be sharp, stabbing, or burning, and can occur anywhere in the chest. It's not always related to physical exertion and may be triggered by movements, breathing, or eating. Atypical pain can be relieved by antacids or changing positions and is less likely to spread to other parts of the body.""",
        
        'EF-TTE': "Ejection Fraction from Transthoracic Echocardiogram (% range: 0-100)",
        'Age': "Age of the patient (years)",
        'Region RWMA': "RWMA (Regional Wall Motion Abnormality) refers to impaired movement of a specific area of the heart's wall, often detected by echocardiography, indicating potential heart disease or damage.",
        'HTN': "Hypertension",
        'BP': "Blood Pressure (mm Hg range: 80-200)",
        'ESR': "Erythrocyte Sedimentation Rate (mm/hr range: 0-100)",
        'FBS': "Fasting Blood Sugar (mg/dL range: 70-130)",
        'Nonanginal': "Nonanginal chest pain, which doctors may also call noncardiac chest pain, refers to pain a person without heart disease may feel behind the breast bone (0: No, 1: Yes)",
        'DM': "Diabetes Mellitus is a condition that happens when your blood sugar (glucose) is too high",
        'Tinversion': "T wave inversion in ECG",
        'K': "Potassium level in blood (mEq/L range: 3.5-5.5)",
        'TG': "Triglycerides (mg/dL range: 0-150)",
        'Na': "Sodium level in blood (mEq/L range: 135-145)",
        'Length': "Height of the patient (cm range: 50-250)",
        'Weight': "Weight of the patient (kg range: 10-200)",
        'Lymph': "Lymphocyte count (cells/uL range: 1000-4000)",
        'PLT': "Platelet count (cells/uL range: 150,000-450,000)",
        'Dyspnea': "Shortness of breath",
        'BMI': "Body Mass Index (kg/m² range: 10-50)"
    }

    # Function to calculate BMI


    # Setting the title
    st.header("Coronary Artery Disease Prediction")

    # st.markdown("<h1 style='font-size: 36px;'>Medical Information </h1>", unsafe_allow_html=True)
    st.write("To streamline the process, we are collecting only the essential information needed for our model to operate effectively, as gathering all 55 features might be too cumbersome for users. If you can provide the required information, please do so. If some data is unavailable, you can select 'NA' or leave numerical inputs blank. We will use average values based on our training data to handle missing information and ensure accurate predictions.")
    st.write('**We do not save your data, to ensure 100% privacy**')
    # Creating the form

    with st.form(key='medical_info_form'):
        name = st.text_input("**Name:**", help=descriptions['Name'])
        my_data['Sex'] =st.selectbox("**Sex:**", ["Male","Female"], help=descriptions['Sex'])
        my_data['Age'] = st.number_input("**Age (years):**", min_value=12, max_value=120, help=descriptions['Age'])
        my_data['Weight'] = st.number_input("**Weight (kg):**", min_value=15.0, max_value=250.0, step=0.5 ,help=descriptions['Weight'])
        my_data['Length'] = st.number_input("**Height (Length) (cm):**", min_value=50.0, max_value=250.0, step = 0.5, help=descriptions['Length'])
        chest_pain = st.selectbox("**Chest Pain:**", ["Typical", "Atypical","None"], help=descriptions["chest_pain"])
        smoker = st.selectbox("**Smoking**", ["Never", "Currently active","in the past"], help=descriptions["chest_pain"])
        # my_data['Atypical'] = st.selectbox("**Atypical Chest Pain:**", ["NA","No", "Yes"], help=descriptions['Atypical'])
        my_data['Region RWMA'] =st.selectbox("**RWMA:**", ["NA","0 (Normal)", "1 (Hypokinesis)", "2 (Akinesis)", "3 (Dyskinesis)", "4 (Aneurysmal)"], help=descriptions['Region RWMA'])
        my_data['HTN'] = st.selectbox("**Hypertension (HTN):**", ["NA","No", "Yes"], help=descriptions['HTN'])
        my_data['Nonanginal'] = st.selectbox("**Nonanginal Chest Pain:**", ["NA","No", "Yes"], help=descriptions['Nonanginal'])
        my_data['DM'] = st.selectbox("**Diabetes Mellitus (DM):**", ["NA","No", "Yes"], help=descriptions['DM'])
        my_data['Tinversion'] = st.selectbox("**T wave Inversion (Tinversion):**", ["NA","No", "Yes"], help=descriptions['Tinversion'])
        my_data['Dyspnea'] = st.selectbox("**Dyspnea (Shortness of Breath):**", ["NA","No", "Yes"], help=descriptions['Dyspnea'])
        my_data['EF-TTE'] = st.text_input("**EF-TTE (%):**", help=descriptions['EF-TTE'])
        my_data['BP'] = st.text_input("**Blood Pressure (BP) (mm Hg):**",  help=descriptions['BP'])
        my_data['ESR'] = st.text_input("**Erythrocyte Sedimentation Rate (ESR) (mm/hr):**", help=descriptions['ESR'])
        my_data['FBS'] = st.text_input("**Fasting Blood Sugar (FBS) (mg/dL):**", help=descriptions['FBS'])
        my_data['K'] = st.text_input("**Potassium Level (K) (mEq/L):**",  help=descriptions['K'])
        my_data['TG'] = st.text_input("**Triglycerides (TG) (mg/dL):**", help=descriptions['TG'])
        my_data['Na'] = st.text_input("**Sodium Level (Na) (mEq/L):**",  help=descriptions['Na'])
        my_data['Lymph'] = st.text_input("**Lymphocyte Count (cells/uL):**",  help=descriptions['Lymph'])
        my_data['PLT'] = st.text_input("**Platelet Count (PLT) (cells/uL) _Scale: 100 = 100,000_:**",  help=descriptions['PLT'])
        
        # Automatically calculate BMI
        BMI = helper.calculate_bmi(my_data['Weight'], my_data['Length'])
        my_data['Obesity'] = int(BMI>25)
        my_data['BMI'] = BMI
        
        # st.write(f"**Body Mass Index (BMI):** {bmi_value:.2f} kg/m²")
        my_data['Typical Chest Pain'] =  int(chest_pain == 'Typical')
        my_data['Atypical'] =  int(chest_pain == 'Atypical')
        my_data['Current Smoker'] = int(smoker == 'Currently active')
        my_data['EX-Smoker'] = int(smoker == 'in the past')
        

        # Submit button
        submit_button = st.form_submit_button(label='Submit')

    # Handling form submission
    if submit_button:
        file_path = 'defaults.pkl'

    # Load the pickle file
        data = {}
        with open(file_path, 'rb') as file:
            defaults = pickle.load(file)
        for i,j in defaults.items():
            if i not in my_data or my_data[i] == '' or my_data[i] == None or  my_data[i] == 'NA':
                data[i] = j

            else:
                if i == 'Region RWMA':
                    data[i] = int(my_data[i][0])
                else:
                    data[i] = my_data[i]
       
        
        data = pd.DataFrame(data,index = [0])
        # st.dataframe(data)
        

        is_at_risk = helper.predict(data)[0]
        
        progress_placeholder = st.empty()
        progress_bar = progress_placeholder.progress(0)
        
        # Simulate progress
        for percent_complete in range(0, 101, 10):
            time.sleep(0.1)  # Simulate time delay
            progress_bar.progress(percent_complete)
        
        # Clear the progress bar once it's done
        progress_placeholder.empty()
        if is_at_risk:
            st.error(f"Dear {name}, You are at risk of coronary heart disease (CHD).")
            st.info("We recommend that you visit a doctor for a thorough evaluation and appropriate guidance.")
        else:
            st.success(f"Dear {name}, You are not currently at risk of coronary heart disease (CHD).")
            st.info("Maintain a healthy lifestyle and regular check-ups to stay healthy.")

        # st.dataframe(helper.preprocess(data))

if __name__ == '__main__':
    main()