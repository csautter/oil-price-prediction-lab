# Oil Price Prediction - an educational project for learning and practicing Python, Data Science, and Machine Learning
This project was created to learn and practice Python, Data Science, and Machine Learning. It is not intended for production use or real-world applications.
The focus is on educational purposes, exploring various libraries, tools, and techniques in the Python ecosystem.
Prediction of oil prices is a complex task that involves various factors, including historical data, market trends, geopolitical events, and economic indicators.
This project aims to build a foundation for understanding how to approach such problems using Python and its libraries but does not guarantee accurate predictions or insights into real-world oil price movements.
But the project is a great opportunity to see how challenging it can be to make accurate predictions in a complex domain like oil prices.
## Features
To get an accurate prediction of oil prices, you need to consider various factors that can influence the market. Here are some key features that can be used in a model to predict oil prices:
1. Historical Price Data: This includes daily, weekly, or monthly prices of oil over a specific period.
2. Supply and Demand: Factors such as production levels, inventory data, and consumption rates can influence price movements.
3. Economic Indicators: Economic growth, unemployment rates, GDP, and other macroeconomic metrics can impact oil demand.
4. Political Events: Political instability in oil-producing countries, sanctions, geopolitical tensions, and policy decisions can affect oil prices.
5. Weather Conditions: Extreme weather can disrupt production, transportation, and consumption of oil.
6. Currency Exchange Rates: Since oil is traded in US dollars, fluctuations in exchange rates can impact international oil prices.
7. Technological Advances: New technologies in oil extraction and processing can influence supply and costs.
8. Trade Data: Trading activities, including futures and options trading, can provide insights into future price movements.
9. Market Sentiment: Sentiment indicators such as investor confidence, analyst opinions, and media reports can influence short-term price movements.
10. Seasonal Patterns: Oil prices can follow seasonal patterns influenced by seasonal changes in consumption and supply.

*In this project, just a few of these features are used to demonstrate how to build a model for prediction.*
## Install
This project is developed and tested on Windows in a WSL2 environment with Ubuntu 20.04.
WSL2 is a great way to run Linux on Windows. But be aware that some features may not work as expected, and you may need to adjust the configuration to suit your needs.
WSL2 environments are sometimes complex to set up, especially when it comes to installing CUDA and other ML tools depending on GPU Hardware.
Check also other public available installation guides for WSL2, CUDA if you run into issues.
### Install Miniconda
````bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# check the hash
sha256sum ~/miniconda3/miniconda.sh # compare with https://docs.anaconda.com/miniconda/
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
mkdir -p ~/bin
cd ~
ln -s ~/miniconda3/bin/conda conda
````

### create conda environment
````bash
conda create --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge
````
### install conda packages
````bash
conda install --name oil-price-prediction --file requirements-dev-conda.txt --channel default --channel conda-forge
````
### install pip packages
````bash
conda activate oil-price-prediction
pip install -r requirements-dev-pip.txt
````

### create requirements.txt
````bash
conda list -e > requirements.txt
````

### Start development environment
Run the following command in WSL2 to enable the conda environment:
````bash
source /opt/conda/etc/profile.d/conda.sh
conda activate oil-price-prediction
````
Start Jupyter Lab:
````bash
jupyter lab
````

### Install CUDA Toolkit for WSL Ubuntu
* CUDA Toolkit: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network
* cuDNN: https://developer.nvidia.com/rdp/cudnn-download

Install the matching version from:
https://www.tensorflow.org/install/source#gpu

### Install Tensorflow
https://www.tensorflow.org/install
https://www.tensorflow.org/install/pip#windows-wsl2

### create .env file
Copy the example .env file to create your own configuration:
````bash
cp .env.example .env
````
Edit the `.env` file to set your environment variables, such API keys, etc. Create accounts on the respective platforms to obtain the necessary keys.