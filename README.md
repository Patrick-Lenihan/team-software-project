# team-software-project
Due to recent global geopolitical events, making the most efficient use of a country's energy system has become a topic of increasing relevance. Energy use depends on a variety of environmental factors and decisions that are required to determine how much electricity needs to be generated. Recent technological advances have made it possible to integrate the use of Information Technologies in power systems to effectively create a “Smart Grid”.

A smart grid is an electricity network that allows for the two way flow of electricity and data, using digital communications technology that allow it to detect, react, and pro-act to changes in usage and other issues.

this poject is to build a smart grid controler

Our controller will monitor the usage levels of electricity within the system. It will make requests to power stations when demand is higher than supply. The controller’s main responsibility is to ensure continuous supply to consumers, as well as reducing the amount of fossil fuels being used as much as possible. The system will also communicate information such as pricing and usage information to consumers in order to smooth out the load.


**this project is still in the prototype phase**.

## Directions to use
- Download the code from the main branch
- go to https://www.eirgridgroup.com/ and download the data for a day of ussage(cannot be for the current day).
- rename this file usage.csv
- place this file in the same directory as the downloaded programs
- run *python3 simulation.py* from inside the downloaded directory. 
- change simulation.py to represent the architecture you want.
- run unit tests by running the command python3 -m unittest unitTests.<module_name>_unittest -v 
