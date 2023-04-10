import pandas as pd
# import numpy as np
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

import plotly.express as px

st.set_page_config(
    page_title="Car Recommendation App",
    layout = "centered"

)
header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

with st.sidebar:
    st.sidebar.write("")

def pipe_reset_index(df, from_1=False):
    if from_1:
        df.index = list(range(1, len(df) + 1))
    else:
        df.index = list(range(len(df)))
    return df

def pipe_rank_index(d_top):
    d_top['Rank'] = [i + 1 for i in range(len(d_top))]
    d_top.set_index('Rank', inplace=True)
    # d_top.index = [i + 1 for i in range(len(d_top))]
    return d_top

def dict_pseudo_rating(df,delta =2):
    Indratings = pd.DataFrame(df.groupby(['Car Brand','Model'])['Rating'].count())
    Indratings['Model'] = pd.DataFrame(df.groupby(['Car Brand'])['Model'].count())
    Indratings['No. of ratings'] = pd.DataFrame(df.groupby(['Car Brand','Model'])['Rating'].count())
    Indratings['Rating'] = (Indratings['Rating']*Indratings['No. of ratings'])/(Indratings['No. of ratings']+delta)
    return Indratings.drop('Model',axis=1).reset_index().rename(columns = {'Rating': 'Pseudo_Rating'})




with header:
    st.title('Car Recommendation System')
    # st.text('Recommending cars on basis of user inputs and filters')

with dataset:
    st.header('Web-scrapped Dataset Overview')
    st.write('**_This is a treemap describing our dataset that contains 187 car models from 37 different'
             ' brands which are all produced after 2021_**')

    df = pd.read_csv('dfApril_01Sentiment.csv').drop(['Unnamed: 0'], axis=1)
    # st.write(df.head(5))
    model_count = pd.DataFrame(df.groupby(['Car Brand'])['Model'].unique())
    model_count['No.of cars'] = pd.DataFrame(df.groupby(['Car Brand'])['Model'].nunique())
    model_count['% of Cars'] = round(((model_count['No.of cars']*100)/model_count['No.of cars'].sum()),1)

    model_count = (model_count
                   .reset_index()
                   .sort_values('No.of cars', ascending=False)
                   .pipe(pipe_reset_index, from_1=True)
                   )

    fig = px.treemap(model_count, path=['Car Brand'], values='No.of cars', hover_data=['% of Cars'],color ='% of Cars')

    fig.update_layout(margin=dict(t=12, l=10, r=10, b=25))
    # fig.update_layout(margin_t= 12,margin_b=15 )
    st.plotly_chart(fig)


    # fig1, ax1 = plt.subplots()
    # ax1.pie(model_count['No.of cars'] ,labels = model_count['Car_Brand'])
    #
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #
    # st.pyplot(fig1)
    # st.bar_chart(x=df['Car Brand'], y=model_count['No.of cars'])

# with features:
      #st.header('Buyers Choice!')

    # Define a list of image URLs

    # st.image(image, use_column_width=True)


    # Load the image
    # image = 'https://media.ed.edmunds-media.com/acura/mdx/2023/oem/2023_acura_mdx_4dr-suv_sh-awd_fq_oem_1_815.jpg'
    #
    # # Display the image using the show_image function
    # st.image(image)

    # Loop through the URLs and display each image


    # def softmax(x):  ## for buyers choice
    #     """Compute softmax values for each sets of scores in x."""
    #     return np.exp(x) / np.sum(np.exp(x), axis=0)
    #
    #
    # drec['Probability'] = softmax(drec['Score'] * 10)
    # car = list(drec['Car Brand'] + ' ' + drec['Model'])
    # carprob = list(drec['Probability'])
    #
    # np.random.choice(car, 1, p=carprob)

with model_training:
    st.header('User Filters :gear:')
    sel_col, disp_col = st.columns(2)
    df = pd.read_csv('dfApril_01Sentiment.csv').drop(['Unnamed: 0'], axis=1)
    pr = dict_pseudo_rating(df,delta =2)
    di = pd.read_csv('CI.csv').drop(['Unnamed: 0'], axis=1)
    temp_options = range(11)
    car_price= sel_col.slider('**Select Price Range**',max_value = 350000, value = [25000,75000],step = 5000)

    weightMC = disp_col.select_slider("**Sensitivity to fuel efficiency**", options=temp_options, value=5)
    hp = int(disp_col.text_input('**Enter max preferred horsepower**', '350'))
    seat_max = [2,  4,  5,  6, 7,  8,  9,  12][::-1]
    seats = sel_col.selectbox('**Maximum No. of seats**',options=seat_max)

    weightP = disp_col.select_slider("**Sensitivity to Horsepower**", options=temp_options, value=5)
    # weightPM = sel_col.select_slider("Sensitivity to Price/Mileage", options =temp_options, value=8)
    weightR = sel_col.select_slider("**Sensitivity to User Ratings**", options=temp_options, value=7)
    weightPP = disp_col.select_slider("**Sensitivity to Horsepower/Price**", options=temp_options, value=6)


    min_price = car_price[0]
    max_price = car_price[1]

    # st.write(min_price)
    # st.write(max_price)

    hp_min = 0
    hp_max = hp

    seat_min = 2
    seat_max = seats

    dn = (df.copy()
    [df['Price'] >= min_price]
    [df['Price'] <= max_price]

    [df['Horsepower'] >= hp_min]
    [df['Horsepower'] <= hp_max]

    [df['Seats'] >= seat_min]
    [df['Seats'] <= seat_max]
    .drop_duplicates()
    )

    dk = dn.groupby(['Car Brand','Model','Engine Type']).mean().reset_index()

    # temp_options = range(11)
    #
    # weightMC = disp_col.select_slider("sensitivity to fuel efficiency", options =temp_options, value=5)
    # weightP = sel_col.select_slider("sensitivity to Horsepower", options =temp_options, value=5)
    # # weightPM = sel_col.select_slider("sensitivity to Price/Mileage", options =temp_options, value=8)
    # weightPP = sel_col.select_slider("sensitivity to Horsepower/Price", options =temp_options, value=6)
    # weightR = sel_col.select_slider("sensitivity to User Ratings", options =temp_options, value=7)

    dk['Mileage/Capacity'] = (dk['Mileage(miles)'] / dk['Fuel tank capacity(gal)']) + 0.01
    # dk['Price/Mileage'] = (dk['Price'] / (np.isfinite(dk['Mileage(miles)']))) + 0.01
    dk['Horsepower/Price'] = (dk['Horsepower']/dk['Price']) + 0.01

    scaler = MinMaxScaler()
    try:
        dk['Mileage/Capacity'] = scaler.fit_transform(dk[['Mileage/Capacity']]) * 5  # scaling everything between 0-5
        # dk['Price/Mileage'] = scaler.fit_transform(dk[['Price/Mileage']]) * 5
        dk['Horsepower/Price'] = scaler.fit_transform(dk[['Horsepower/Price']]) * 5
        dk['HP_eff'] = scaler.fit_transform(dk[['Horsepower']]) * 5

        dk['Score'] = ((weightMC / 10) * (dk['Mileage/Capacity']) + (weightP / 10) * (dk['HP_eff']) +
                       (weightPP / 10) * (dk['Horsepower/Price']) + (weightR / 10) * (dk['Rating']) + 0.7 * dk[
                           'Sentiment']) / 5

        dk = dk.sort_values('Score', ascending=False)
        dk.index = list(range(len(dk)))

        drec = dk.drop_duplicates().iloc[0:10]
        dfin = pd.merge(drec[['Car Brand', 'Model']], dn)
        drec = pd.merge(drec,di)

        d_top = {
            'Car Brand': drec['Car Brand'],
            'Model': drec['Model'],
            'Car_name': drec['Car'],
            'Engine Type': drec['Engine Type'],   # engine type
            'Price': drec['Price'].astype('int'),
            'Horsepower': drec['Horsepower'].astype('int'),
            'Mileage(miles)': drec['Mileage(miles)'].astype('int'),
            'Seats': drec['Seats'].astype('int'),
            'Score(out of 5)': round(drec['Score'],2),
            'Image_url': drec['Image_url']

        }
        d_top=pd.DataFrame(d_top)


        d_top['Score(out of 5)'] = scaler.fit_transform(d_top[['Score(out of 5)']]) * 5
        d_top['Score(out of 5)'] =  d_top['Score(out of 5)'].apply(lambda x: round(x,2))

        pr = pr[pr['Car Brand'].isin(d_top['Car Brand'].unique())]
        pr = pr[pr['Model'].isin(d_top['Model'].unique())]

        # d_top = pd.merge(d_top.pipe(pipe_reset_index), pr.pipe(pipe_reset_index)).drop('Ratings', axis=1).rename(
        #     columns={'Pseudo_Rating': 'Ratings'})

        # d_top['Rank'] = [i + 1 for i in range(len(d_top))]
        # d_top.set_index('Rank', inplace=True)
        # d_top.index = [i + 1 for i in range(len(d_top))]
        st.subheader('Top Recommendations')
        st.write(d_top.drop(['Image_url','Car_name'],axis=1)
                 .drop_duplicates()
                 .head(5)
                 .pipe(pipe_reset_index,from_1=True)
                 .pipe(pipe_rank_index)
                 .rename(columns = {'Price': 'Price(USD)'})
                 )

        d_top['Car_name'] = d_top['Car Brand'] + '   '+ d_top['Model']

        DropdownCar = st.selectbox('**Select Car**', options=d_top['Car_name'].iloc[0:8].unique())
        cn = DropdownCar.split('   ')[0]
        mn = DropdownCar.split('   ')[1]
        dz = d_top[d_top['Car Brand'] == cn][d_top['Model'] == mn].sort_values('Score(out of 5)', ascending=False).pipe(pipe_reset_index)
        dnn = dn[dn['Car Brand'] == cn][dn['Model'] == mn].pipe(pipe_reset_index)

        dnn['Price'] = dnn['Price'].astype('int')
        dnn['Horsepower'] = dnn['Horsepower'].astype('int')
        dnn['Mileage(miles)'] = dnn['Mileage(miles)'].astype('int')

        # st.write(dnn.head(5))
        # st.write(dz.head(5))
        dz = pd.merge(dz.drop(['Price','Horsepower','Mileage(miles)'],axis = 1), dnn)
        # st.write(dz.head(5))
        image = dz['Image_url'].iloc[0]

        col1, col2 = st.columns([3,1])
        carname = cn+' ' + mn
        headimage = f"**Our Recommendation**: **:red[{carname}]**"


        col1.subheader(headimage)
        # st.write('#')
        col1.image(image,width=22*22)

        S_5,S_4,S_3,S_2,S_1=  dz[['5 Stars','4 Stars','3 Stars','2 Stars','1 Star']].iloc[0]
        star_index = ['5 Stars','4 Stars','3 Stars','2 Stars','1 Star']

        fig = px.bar(x=star_index, y=[S_5,S_4,S_3,S_2,S_1],height=15*15,width=15*15)
        col2.subheader('**Rating Distribution**')
        fig.update_xaxes(title='Star Rating')
        fig.update_yaxes(title=' % Of Users',range = [0,100])

        col2.plotly_chart(fig)

        price = dz['Price'].iloc[0]
        col2.subheader('Price: ' + '$'+f'{price:,}')
        ratings = dz['Average rating'].iloc[0]
        col2.write('**Average rating:** ' + f'**{ratings}**' + ':star:')
        pros = dz['Pros'].iloc[0]
        cons =dz['Cons'].iloc[0]
        neg_com = dz['Comments'].iloc[-1]
        pos_com = dz['Comments'].iloc[0]
        st.subheader('Pros 	:thumbsup:')
        st.write(pros)
        st.subheader('Cons 	:thumbsdown:')
        st.write(cons)
        st.subheader('Reviews :newspaper:')
        st.write(pos_com)
        st.write(neg_com)


        # shorty = pyshorteners.Shortener()
        st.subheader("Buy it in Germany: ")



        car_DE_URL = 'https://www.autoscout24.com/lst/' + cn.lower() + '/' + mn.lower() #+ '?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=1&powertype=kw&search_id=1eucj4ea093&sort=price&ustate=N%2CU'
        # car_DE_URL= shorty.tinyurl.short(car_DE_URL)
        st.write(car_DE_URL.replace(' ', ""))

        st.subheader("Buy it in USA:")
        car_US_URL = 'https://www.truecar.com/new-cars-for-sale/listings/' + cn.lower() + '/' + mn.lower()
        # car_US_URL = shorty.tinyurl.short(car_US_URL)
        st.write(car_US_URL.replace(' ',""))

        st.subheader("Buy it in India:")
        car_IND_URL = 'https://www.cardekho.com/' + cn.lower() + '/' + mn.lower()
        # car_IND_URL = shorty.tinyurl.short(car_IND_URL)
        st.write(car_IND_URL.replace(' ',""))

    except ValueError:
        st.error('No cars found!!!', icon="🚨")
