   # SmartBasket - Weekly Grocery Price Optimizer

   SmartBasket is an AI-powered tool designed to help Stockholm residents optimize their grocery shopping by comparing prices across different stores.

   ## Features (MVP)
   - Price comparison across major grocery chains in Sweden. (e.g., ICA, Coop, Willys, Lidl, City Gross).
   - Weekly cost-effective shopping list suggestions.

   ## Setup

   1. Clone the repository:
      ```bash
      git clone https://github.com/LeonByte/SmartBasket.git
      cd SmartBasket
      ```

   2. Install dependencies using Poetry:

      ```bash
      poetry install
      ```

   3. Activate the virtual environment (multiple options)

      ```bash
      poetry env activate  # Shows the activation command, which you then need to run
      ```

      ```bash
      source $(poetry env info --path)/bin/activate
      ```
      #### OR

      ```bash
      source /path/to/your/virtualenv/bin/activate  # Use the full path shown by 'poetry env activate'
      ```     

   ## License

   This project is licensed under All Rights Reserved. See the [LICENSE](./LICENSE) file for details.
