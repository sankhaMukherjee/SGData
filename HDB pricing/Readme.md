

# HDB pricing index

This is a set of programs useful for exploration of the housing data. The `src` folder contains several programs that can be used for studying the data. The *data* part is not present, and must be downloaded from the following site. 

    https://data.gov.sg/dataset/resale-flat-prices. 

Please note the information about liabilities of using the License section.

# Synopsis

There are several sets of programs that do different things. These can broadly be classified into several different categories. 

**Data Simplification** 

<p style="color:indianred"> This section is not done yet ... Write programs to complete it soon. Now I am using ad-hoc iPython commands to create these. </p>

These sets of programs will 

1. Combine the two different files into a single file, so that it is easy to read at a later stage, 
2. Create files that contain the *unique values* for the `flat_model`, `flat_type` and `town` parameters so that they can be looked up easily
3. Parameters for geocoding. A set of geocodes have already been provided in the data section for the different addresses. If some new addresses are found, then they may be added into the addresses present. 

If you have an updated file for Housing Prices, it may be advantageous to run the code in the file: 

    src/updateInformation.py 
    
Before commencing on other data tasks.

<p style="color:indianred"> Need to finish this </p>

# Code Example

<p style="color:indianred"> Need to finish this </p>

# Motivation

There are a couple of reasons why I wanted to do this:

**My own forays into programming**

I am creating these set of programs for my own education. I want to be able to easily interface between PlotlyJS, AngularJS and a RESTful application which is provided by a Python backend. This gives me a chance to learn about both servers and clients simultaneously. 

**Write maintainable code**

Being from an engineering background, it is way to easy to get done with bad, unmaintainable code. This project will force me to write code that is *half-decent*. Otherwise I will forever be locked in the mire of bad coding practices.

# Installation

Just download a copy and start working. Remember that these use Python and some ancillary libraries. Some of these the generally need to be installed are as follows:

**Python Libraries**

 - Pandas
 - Bottle
 - googlemaps

**Javascript Libraries** (mostly already supplied in the source):

 - AngularJS
 - PlotlyJS

# API Reference

<p style="color:indianred"> Need to finish this </p>

# Tests

Currently there are no tests to perform. I shall eventually get to the point where I shall include tests. 

# Contributors

Sankha S. Mukherjee. 

Constructive criticism is more than welcome. Please write to me directly at *sankha.mukherjee* [at] *gmail* 

# License

 - BSD License
 - These things are provided as-is. 

**License from the Singapore Government**

 - The data is obtained from [data.gov.sg](data.gov.sg).
 - All modifications to the data are performed by the programs supplied, and should not be attributed to the Singapore government or its Statuatory Boards. 
 - "The datasets provided by the Singapore Government and its Statutory Boards via Data.gov.sg are governed by the Terms of Use available at https://data.gov.sg/terms. To the fullest extent permitted by law, the Singapore Government and its Statutory Boards are not liable for any damage or loss of any kind caused directly or indirectly by the use of the datasets or any derived analyses or applications."
 - If you use these programs, and associated data, you **must** (I cannot stress this enough) abide by the terms and conditions stipulated in the website below:
    [Terms of Use](https://data.gov.sg/terms) of the data as stated from the Singapore Government. Please go through this before using the data.


