import streamlit as st
import numpy as np
import pandas as pd
import re


st.set_page_config(page_title='Quick Figures')
st.title("Quick Figures")

start_index = 0

def Main():
    
    st.write(" ")
    colTop1, colTop2, colTop3, colTop4 = st.columns(4)

    times_list = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
  

    start_dropbox = colTop1.selectbox("Start Time :  ", times_list)
    end_dropbox = colTop2.selectbox("End Time : ", times_list, index=6)
    
    start_index = times_list.index(start_dropbox) #drop down chosen start time index generator
    end_index = times_list.index(end_dropbox) #drop down chosen end time index generator

    total_items =colTop3.text_input("Total items processed : " ,value=0)
    total_items = re.sub('[^0-9]','', total_items)

    if total_items == "":
        total_items = 0

    total_items = int(total_items)

    people_hours = colTop4.number_input("People used per hour : ", step=1)

 

    st.write("--------------")

    Calculation(times_list, start_index, end_index, people_hours, total_items) #New method declared below


def Calculation(times_list, start_index, end_index, people_hours, total_items):

    duration_length = end_index - start_index

    if(duration_length <=0):
        st.error("Start Time can not start AFTER End Time or be the SAME as End Time.")
    

    
    colMid2, colMid3 = st.columns(2)

    #colMid1.write("Time")
    colMid2.write("Processed")
    colMid3.write("Hours")

    current_hours=[]

    processed_items=[]

    hours_to_percentage=[]

    random_percentage_list=[]

    for i in range(0,duration_length):
        current_hours.append(people_hours) 
        processed_items.append(total_items/(duration_length) * int(current_hours[i]))

    hours_sum = sum(current_hours)

    for i in range(0,duration_length):

            if current_hours[i] <= 0:
                hours_to_percentage.append(0)
            else:
                hours_to_percentage.append(hours_sum/current_hours[i])


    for i in range(0, duration_length):
        #colMid1.text_input("",times_list[i+start_index], disabled=True) 
        
        current_hours[i]=colMid3.text_input(str(times_list[i+start_index])+"-"+str(times_list[i+start_index+1]),people_hours, key=str(times_list[i]))
        #current_hours[i]= re.sub('[^0-9]','', current_hours[i])
        
        if current_hours[i] == "":
            current_hours[i] = 0

        current_hours[i] = float(current_hours[i])
        #hours_to_percentage[i]()

        processed_items[i] = (total_items/(duration_length+1)) * int(current_hours[i])

        #colMid2.text_input("",processed_items[i], key=str(times_list[i]+"t"), disabled=True) 

    random_percentage = np.random.dirichlet(np.ones(duration_length+1),size=1)

    random_percentage = random_percentage.flatten()
    random_percentage = random_percentage.tolist()

    hours_sum = sum(current_hours)

    for i in range(0, duration_length):
        if current_hours[i] <= 0:
            hours_to_percentage[i]=(0)
        else:
            hours_to_percentage[i]=(current_hours[i]/hours_sum)+random_percentage[i]/10   
            
        processed_items[i] = int(total_items*(hours_to_percentage[i]))#random percentage


    sum_of_processed = sum(processed_items)
    difference = sum_of_processed - total_items

    for i in range(0, duration_length):
        if difference > 0:
            if processed_items[i]>=difference:
                processed_items[i]= processed_items[i]-difference
                difference = 0

            else:
                if processed_items[i] > 0:
                    processed_items[i] = (processed_items[i] - difference)*-1
                    sum_of_processed = sum(processed_items)
                    difference = sum_of_processed - total_items
        if processed_items[i] > 0:
            acf =  "  (ACF "+str(int(processed_items[i]/current_hours[i]))+")"
        else:
            acf = ""          
        
        colMid2.text_input(str(times_list[i+start_index])+"-"+str(times_list[i+start_index+1] + acf),processed_items[i], disabled=True) 

    st.write("----")
    st.write("processed items sum: " + str(sum(processed_items)))
    st.write("hourly sum: " + str(hours_sum))
    

if __name__ == '__main__':
	#pass in the username of the account you want to download
	Main()
