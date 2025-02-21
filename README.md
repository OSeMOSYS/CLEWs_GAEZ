# GeoCLEWs Agro

This repository introduces **GeoCLEWs Agro**, a complementary extension to **GeoCLEWs v2.0.0** that enhances its foundational functionalities. **GeoCLEWs Agro** builds upon [GeoCLEWs v2.0.0](https://github.com/OSeMOSYS/CLEWs_GAEZ/commit/6e23635efcde224eb54120390ff18ccfe2604b1a) by adding expanded agro-climatic insights and extending data coverage. This version retains all the core features of [GeoCLEWs v2.0.0](https://github.com/OSeMOSYS/CLEWs_GAEZ/commit/6e23635efcde224eb54120390ff18ccfe2604b1a) while offering additional capabilities for users requiring broader agro-climatic analysis.

# Key Features

GeoCLEWs Agro captures additional temporal agro-climatic indicators, offering extended insights into crop-related data.

# New Enhancements

**Expanded Temporal Coverage**: Data outputs now span from **1981 to 2100**, supporting historical, present, and future scenario analysis.

# Data Source

Similar to [GeoCLEWs v2.0.0](https://github.com/OSeMOSYS/CLEWs_GAEZ/commit/6e23635efcde224eb54120390ff18ccfe2604b1a) The agro-climatic data is sourced from **GAEZ**, which leverages its extensive database on global agriculture to generate insights tailored to varying environmental and agricultural conditions.

# Unchanged Functionalities

This version retains the core features from [GeoCLEWs v2.0.0](https://github.com/OSeMOSYS/CLEWs_GAEZ/commit/6e23635efcde224eb54120390ff18ccfe2604b1a) maintaining full compatibility with existing workflows:

- **Crop Identification**: Detects primary and secondary crops using **FAOSTAT** and **GAEZ** datasets, ensuring accurate crop classification.
- **Land Cell Generation**: Develops georeferenced cells adaptable to diverse geographical boundaries, supporting flexible and scalable analysis.
- **Geographical Aggregation**: Simplifies regional aggregation, optimizing **CLEWs** modeling computations for more efficient analysis.
- **Spatial Clustering**: Facilitates the analysis of cross-regional interdependencies, enhancing resource management and decision-making.
- **Cluster Identification and Classification**: Groups and classifies regions based on agro-climatic patterns and suitability, ensuring accurate spatial representation for modelling.
- **Automated Data Extraction and Preprocessing**: This process integrates and processes data from **GAEZ** datasets efficiently, ensuring smooth workflow and accurate inputs for analysis.
- **CLEWs-Compatible Outputs**: Produces outputs that are ready for seamless integration into **CLEWs** modelling frameworks, ensuring consistency with existing workflows.
- **Interactive Outputs**: Provides comprehensive tabular datasets and visualizations for detailed analysis, enabling users to interpret the results effectively.

# Additional Functionalities

- **Expanded Temporal Coverage**: All datasets now have a time frame extending from **1981 to 2100**. This enables analysis across historical, present, and future periods.
- **Forecasting Missing Data**: A forecasting mechanism has been developed to estimate missing data for **low-input (subsistence farming)** systems from **2011 to 2100**. This forecast is based on historical trends from the **GAEZ** portal.
- **Generation of Outputs**: Outputs for **high-input (intensive agriculture)** and **low-input (subsistence farming)** systems are generated from **1981 to 2100**.
- **Categorization by Date Ranges:** Outputs are categorized into the following date ranges:

1. **1981-2010**: Historical Baseline
2. **2011-2040**: Near Future
3. **2041-2070**: Mid-Century
4. **2071-2100**: End of Century

For a detailed overview of features from **Version 2.0.0**, refer to its [documentation](https://github.com/OSeMOSYS/CLEWs_GAEZ/blob/main/README.md).

# Installation and Usage

The **installation** process and **usage instructions** remain unchanged from **Version 2.0.0**. Please refer to the GeoCLEWs v2.0.0 [README](https://github.com/OSeMOSYS/CLEWs_GAEZ/blob/main/README.md).

# Applications

**GeoCLEWs Agro** supports:

- **Long-Term Planning**: Supports proactive strategies for agricultural sustainability by analyzing future projections.
- **Enhanced Decision Making**: Provides precise crop and water data for better local and regional agricultural decisions.
- **Cost Efficiency**: Reduces the need for extensive data collection by forecasting missing data.
- **Adaptation Strategies**: Helps design tailored climate adaptation strategies for different agricultural systems.
- **Scenario Analysis**: Facilitates risk assessments by simulating the impacts of climate and water changes.
- **Policy Support**: Assists in formulating climate-smart policies and water management strategies.
- **Climate-Resilient Policy Development**: Aids in the development of policies that ensure agricultural resilience to climate change.
- **Cross-Regional Resource Management**: Optimizes water and land resource management across regions to improve sustainability.
- **Energy and Food Security**: Supports long-term scenario planning to ensure both energy and food security in changing environments.

# Contributors

[**Ronnice Chepkoech**](https://www.linkedin.com/in/chepkoech-ronnice)\- Developer  
[**Taco Niet**](https://github.com/tniet) - Supervisor

# Acknowledgements

Special thanks to [**Yalda Saedi**](https://github.com/Ysaedi) (the original developer), [**Taco Niet**](https://github.com/tniet) and [**Benard Alunda**](https://www.linkedin.com/in/bernard-alunda-b78148170) (supervisors), and [**Global Affairs Canada**](https://www.international.gc.ca) (funder), as well as all contributors to **GeoCLEWs v2.0.0** for their foundational work.

# Contact

For any inquiries, please contact [**Ronnice Chepkoech**](https://www.linkedin.com/in/chepkoech-ronnice)
