![logo](https://github.com/data-silence/banks-clients/blob/master/img/bgr.png?raw=true)

![Fastapi](https://img.shields.io/badge/Fastapi-black?style=flat-square&logo=fastapi) ![Pydantic](https://img.shields.io/badge/Pydantic-black?style=flat-square&logo=Pydantic) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-black?style=flat-square&logo=PostgreSQL) ![Streamlit](https://img.shields.io/badge/Streamlit-black?style=flat-square&logo=Streamlit) ![sklearn](https://img.shields.io/badge/sklearn-black?style=flat-square&logo=sklearn)

# Table of contents

* [About](#about)
* [Problem statement](#problem-statement)
* [Cod structure](#cod-structure)
* [Buildings app](#building-app-on-your-own)
* [License](#license)
* [Contacts](#contacts)



## About


The project is designed to demonstrate some skills in ML: conducting Exploratory Data Analysis, building predictive machine learning models, formalizing the results of the research in the form of a web service using Streamlit and FastApi frameworks and remote PostgreSQL database.     

It has created as part of the ["Linear models and their presentation"](https://stepik.org/course/177215/syllabus) course offered by [AI Education](https://stepik.org/course/177213) on Stepik education platform.

It is devoted to analytical research of bank users, as well as prediction of their behavior using machine learning methods with visualization of the obtained results in the form of WEB application. 

You can use the app just visit https://bank-clients-fastapi.streamlit.app/


## Problem statement



One way to increase the efficiency of a bank's interaction with customers is to send an offer of a new service not to all customers, but only to some customers who are selected on the principle of the highest propensity to respond to the offer.

The main task of the project was to propose an algorithm that would output a customer's propensity to respond positively or negatively to the bank's offer. It is assumed that, having obtained such estimates for some set of customers, the bank will make an offer only to those from whom a positive response is expected.

A set of data on clients of one micro-credit organization was offered as input data, with which it was necessary to work:
- merge the data into single tables without duplicates and put them into a database:
- conduct EDA and make a number of visualizations to demonstrate the key characteristics of this bank's clients;
- build a series of linear models to solve the problem;
- create an api for a web application using the Fast API framework and host it on a remote server;
- create an application using Streamlit that visualizes the EDA work performed and demonstrates the work of the obtained models for predicting customer behavior.



## Cod structure

The project consists of three parts:
1. **Research** (notebooks folder). Here you can find notebooks with EDA about bank customers, and experiments on training predictive models of bank customer behavior.
2. **Backend** as FastAPI app (backend folder). Here you can find designing endpoints and trained models
3. **Frontend** as Streamlit app (frontend folder). Here lies the design of the application interface: the function to plot, visualize, and interface interaction with models and user selection


## Building app on your own

1. Create clients db using [clinic_test.sql](clinic_test.sql) script
2. Change db connection settings using your new db connections params 
3. Deploy backend Fast API server with [requirements-backend.txt](requirements-backend.txt): ```pip install -r requirements-backend.txt``` and run it with ```uvicorn backend.main:app --host 0.0.0.0 --port 1000```. Host and port number depends of your host settings, change them if necessary.
4. Change ```api_url``` in backend\scripts.py and frontend\scripts.py with your new backend url.
5. Deploy frontend streamlit application using [requirements.txt](requirements.txt) and run ```streamlit run .\frontend\app.py```

_Important_: The described installation is valid when the application is deployed from the root directory of the repository. That is, the backend and frontend folders must be inside the root directory. If you prefer to change the repository structure or install backend and frontend from directories with the same name, you will need to change the relative import paths and application startup options.  

## License
This project is licensed under the MIT license. For more information, see the LICENSE file.

## Contacts
For any questions you may have, please contact us by enjoy@data-silence.com or telegram @data-silence