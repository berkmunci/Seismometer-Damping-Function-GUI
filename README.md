# Seismometer Damping Function GUI
## Project Target:
Determination of damping functions with real data.  
## Required Data for satisfy project target: 
Amplitude values of a seismometer.
## Desired Outputs: 
A gui that helps to observe rms values of optimal vs real data with changing Tn and Tao parameters
## Project Phases:
  ##  1) DATA COLLECTION PHASE
  - An private dataset(.dat file) which includes amplitude values of a seismometer is used. 
  ##  2) DATA PREPERATION PHASE
  - Dataset is imported as dataframe and data type is checked for mathematical operations.
  ##  3) DATA PROCESSING AND VISUALIZATION PHASE
GUI structure is created with helping TKinter. RMS calculations and necessary functions are defined. With this gui an user can do followings:
- Initial Tao and Tn values can be entered.
![image](https://user-images.githubusercontent.com/114949587/225319198-18dead7e-6065-4161-a282-e1ba246013c6.png)
- Observaion of error rate by changing parameters with slider by user.
![image](https://user-images.githubusercontent.com/114949587/225319569-327b6ee6-749a-4909-aa99-feb90562482e.png)
- Selected values and function which is dependent to the selected values can be observed and saved.
![image](https://user-images.githubusercontent.com/114949587/225319777-79a8d2a9-a6b4-4b04-858c-0da1035458e1.png)
