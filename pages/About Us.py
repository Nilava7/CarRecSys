import streamlit as st


header = st.container()
proj = st.container()

with header:
    st.header('About Us')
    st.subheader("Project Overview :blue_car: :oncoming_automobile: :red_car:")
    st.write('**_This project was carried out as part of the TechLabs “Digital Shaper Program” in Aachen (WS 2022)_**')
    st.write('---')
    st.write(
        """
        To succeed in the dynamic automotive environment and maximize revenue, companies must continuously optimize their product mix and adapt to changing market trends. The challenge is to develop recommendations for the automotive product mix based on collected customer opinions that meet both current and future customer requirements.

By focusing on customer needs and expectations and continuously seeking opportunities to optimize their product range, companies can be successful in this fast-paced industry and maximize their profits. To achieve this, a collection of customer data and an understanding of customer voices in the automotive industry are required.

We scrapped information from the website https://www.edmunds.com/ and thus created our own dataset. This method allowed us to extract relevant information about vehicles and customer opinions directly from a trusted source.

With the collected and analyzed data, we were finally able to develop recommendations for the automotive product mix. These recommendations were based on the needs and desires of customers identified through the analysis of customer opinions. The final product was a sophisticated car recommendation system that used machine-learning algorithms to suggest the best cars for individual users. 

The system took into account the user's budget, preferred car type, and features, as well as some custom filters, to provide personalized recommendations. To provide the best recommendation, we focused on identifying the vehicle models and features that were most popular with customers and achieved the highest customer satisfaction and coupled them with our custom user specific filters.

The car recommendation system could save consumers time, reduce the stress of decision-making, and ultimately provide a better car-buying experience.
        """
    )

    st.subheader("Get to know the TEAM:beers:")
    st.write("---")
    st.write(""" We are a group of 3 students along with our mentor, who worked on this data science project hosted by TechLabs Aachen.

Our team consists of three students, each with unique skills and expertise. **:blue[Melek]**:male-technologist:, an Electrical & Information Technology student, was responsible for developing the algorithms and code for the web scrapper and contributed to the development of the filters. **:blue[Hidhr]**:male-office-worker:, who is pursuing his Masters in Data Science provided insights into consumer behavior and preferences and thereby developed the algorithms required for sentiment analysis using Natural Language processing. Finally, **:blue[Nilava]**:male-construction-worker:, who is pursuing his Masters in Electrical Engineering, analyzed and interpreted the data collected from various sources, including car dealerships, online reviews, and developed the algorithms for filters, and designed the webpage. 

Our mentor, **:blue[Phanindra]**:technologist:, a data scientist with years of experience, provided guidance and direction throughout the project. Together, the team worked tirelessly to collect and analyze data, build algorithms, and develop a user-friendly interface for the recommendation system.

In conclusion, the data science project hosted by **:red[TechLabs Aachen]** was a testament to the power of collaboration and innovation. The team's efforts resulted in a sophisticated car recommendation system that could benefit car buyers worldwide.

For more info follow TechLabs Aachen: 

- https://www.linkedin.com/company/techlabs-aachen/
- https://www.instagram.com/techlabs.aachen/
- https://techlabs.org/location/aachen
 """)

st.image('techLabImage.jpg',width=10*10)

