from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
from PIL import Image as image

model = load_model('dt_insurance_charges')


def predict(model,input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df.iloc[0]['prediction_label']
    return predictions

def run():
    image_logo = image.open('logo_diabetes.png')
    image_hospital = image.open('hospital.jpg')

    st.image(image_logo)
    st.sidebar.info("This app is created to predict patient hospital charges.")
    st.sidebar.image(image_hospital)
    add_selectbox = st.sidebar.selectbox('How would you like to predict ?', ("Online", "Batch"))
    st.title("Insurance charges prediction app")

    if add_selectbox == "Online":
        age = st.number_input('Age', min_value=1, max_value=100, value=25)
        sex = st.selectbox('Sex', ['Male', 'Female'])
        bmi = st.number_input('BMI', min_value=10, max_value=50, value=10)
        children =  st.selectbox('children', [0,1,2,3,4,5,6,7,8,9,10])
                                 
        if st.checkbox("Smoker"):
            smoker = 'yes'
        else:
            smoker = 'no'

        region = st.selectbox('Region', ['southwest', 'southeast', 'northwest', 'northeast'])   
        output = ""

        input_dict = {'age': age, 'sex': sex, 'bmi': bmi, 'children': children, 'smoker': smoker, 'region': region}
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model, input_df)
            output  = "${}".format(output)
            st.success('This Output is ${}'.format(output))
    

    if add_selectbox == "Batch":
        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            input_df = pd.read_csv(file_upload)
            predictions_df = predict_model(estimator=model, data=data)
            st.write(predictions_df)
            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')
            csv = convert_df(predictions_df)
            st.download_button(
                label="Download Predictions as CSV",
                data=csv,
                file_name='predictions.csv',
                mime='text/csv',
            )

if __name__ == '__main__':
    run()
